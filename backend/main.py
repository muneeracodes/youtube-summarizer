import os
import sys
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi  # BUG 1 FIX: correct import

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.downloader import download_audio, is_playlist, format_duration
from pipeline.transcriber import transcribe, get_transcript_with_timestamps
from pipeline.detector import detect_language
from pipeline.summarizer import summarize

app = FastAPI(title="YouTube Summarizer API", version="2.0.0")

allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    url: str
    summary_type: str = "bullets"
    model_size: str = "base"

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "YouTube Summarizer Engine"}

@app.post("/api/summarize")
async def summarize_video(req: SummarizeRequest):
    try:
        video_url = str(req.url)
        playlist = is_playlist(video_url)

        raw_id = video_url.split("v=")[-1].split("&")[0] if "v=" in video_url else video_url.split("/")[-1]
        video_id = raw_id.split("?")[0].split("&")[0]

        if playlist:
            audio_files, metas = download_audio(video_url)
            results = []

            for audio_path, meta in zip(audio_files, metas):
                if audio_path is None:
                    try:
                        raw_loop_id = meta["url"].split("v=")[-1].split("&")[0] if "v=" in meta["url"] else meta["url"].split("/")[-1]
                        loop_id = raw_loop_id.split("?")[0].split("&")[0]

                        # BUG 2 FIX: same fix applied to playlist fallback
                        api = YouTubeTranscriptApi()
                        transcript_list = api.fetch(loop_id)
                        text_to_summarize = " ".join([snippet.text for snippet in transcript_list])
                        lang = detect_language(text_to_summarize)
                        summary = summarize(text_to_summarize, req.summary_type, lang)
                    except Exception:
                        summary = "Skipped: YouTube blocked the audio stream for this video, and no usable subtitles were found to fall back on."
                        lang = "unknown"
                else:
                    transcript_data = transcribe(audio_path, req.model_size)
                    plain_text = transcript_data["text"]
                    segments = transcript_data["segments"]
                    lang = detect_language(plain_text)
                    text_to_summarize = get_transcript_with_timestamps(segments) if req.summary_type == "timestamps" else plain_text
                    summary = summarize(text_to_summarize, req.summary_type, lang)

                results.append({
                    "title": meta["title"],
                    "duration": format_duration(meta["duration"]),
                    "url": meta["url"],
                    "thumbnail": meta["thumbnail"],
                    "language": lang,
                    "summary": summary,
                })
            return {"type": "playlist", "results": results}

        else:
            audio_path, meta = download_audio(video_url)

            if audio_path is None:
                print(f"[API Guard] Audio stream blocked by YouTube. Activating Transcript Fallback for Video ID: {video_id}")
                try:
                    # BUG 3 FIX: was calling YouTubeTranscriptApi() without importing it properly
                    # AND was using undefined variable `srt` instead of transcript_list
                    api = YouTubeTranscriptApi()
                    transcript_list = api.fetch(video_id)
                    text_to_summarize = " ".join([snippet.text for snippet in transcript_list])  # BUG 4 FIX: was `srt` (undefined)

                    print("[Fallback Router] Successfully extracted clean transcript lines.")

                    lang = detect_language(text_to_summarize)

                    summary_mode = "bullets" if req.summary_type == "timestamps" else req.summary_type
                    summary = summarize(text_to_summarize, summary_mode, lang)

                    if req.summary_type == "timestamps":
                        summary = "(Note: Timestamps unavailable due to stream fallback mode)\n\n" + summary

                    return {
                        "type": "single",
                        "title": meta["title"],
                        "duration": format_duration(meta["duration"]),
                        "url": meta["url"],
                        "thumbnail": meta["thumbnail"],
                        "language": lang,
                        "summary": summary,
                    }

                except Exception as transcript_err:
                    print(f"[Fallback Crash] Complete dead end: {str(transcript_err)}")
                    raise HTTPException(
                        status_code=500,
                        detail="YouTube bot security is blocking this request, and this video does not have any captions or subtitles available to fall back on."
                    )

            transcript_data = transcribe(audio_path, req.model_size)
            plain_text = transcript_data["text"]
            segments = transcript_data["segments"]

            lang = detect_language(plain_text)

            if req.summary_type == "timestamps":
                text_to_summarize = get_transcript_with_timestamps(segments)
            else:
                text_to_summarize = plain_text

            summary = summarize(text_to_summarize, req.summary_type, lang)

            return {
                "type": "single",
                "title": meta["title"],
                "duration": format_duration(meta["duration"]),
                "url": meta["url"],
                "thumbnail": meta["thumbnail"],
                "language": lang,
                "summary": summary,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clear-cache")
def clear_cache():
    cache_dir = "audio"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)
    return {"status": "cleared"}