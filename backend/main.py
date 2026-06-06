import os
import sys
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi

# Force Python to recognize the current directory for absolute package imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your pipeline modules safely
from pipeline.downloader import download_audio, is_playlist, format_duration
from pipeline.transcriber import transcribe, get_transcript_with_timestamps
from pipeline.detector import detect_language
from pipeline.summarizer import summarize

app = FastAPI(title="YouTube Summarizer API", version="2.0.0")

# PRODUCTION CORS: Reads allowed origins from environment variable (comma-separated for Vercel/Local)
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
    """Health check endpoint for Render to verify the service container is alive."""
    return {"status": "healthy", "service": "YouTube Summarizer Engine"}

@app.post("/api/summarize")
async def summarize_video(req: SummarizeRequest):
    try:
        video_url = str(req.url)
        playlist = is_playlist(video_url)

        # Extract standard unique video ID for transcript fallback matching
        video_id = video_url.split("v=")[-1].split("&")[0] if "v=" in video_url else video_url.split("/")[-1]

        if playlist:
            audio_files, metas = download_audio(video_url)
            results = []
            
            for audio_path, meta in zip(audio_files, metas):
                if audio_path is None:
                    try:
                        loop_id = meta["url"].split("v=")[-1].split("&")[0] if "v=" in meta["url"] else meta["url"].split("/")[-1]
                        
                        # Step 2 Smart Selection Loop for Playlist items
                        transcript_list = YouTubeTranscriptApi.list_transcripts(loop_id)
                        try:
                            # 1. Try finding manually created English captions
                            srt_obj = transcript_list.find_transcript(['en'])
                        except Exception:
                            try:
                                # 2. Fallback to auto-generated English captions
                                srt_obj = transcript_list.find_generated_transcript(['en'])
                            except Exception:
                                # 3. Fallback to translating whatever language exists straight into English
                                first_available = next(iter(transcript_list._manually_created_transcripts.values() or transcript_list._generated_transcripts.values()))
                                srt_obj = first_available.translate('en')

                        srt = srt_obj.fetch()
                        text_to_summarize = " ".join([item["text"] for item in srt])
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
            
            # 🌟 CORE FAILOVER: Handled cleanly without requiring list_transcripts
            if audio_path is None:
                print(f"[API Guard] Audio stream blocked by YouTube. Activating Transcript Fallback for Video ID: {video_id}")
                try:
                    # Universal, standard extraction method that works across all library versions
                    srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
                    print("[Fallback Router] Successfully extracted English transcript lines.")
                    
                    text_to_summarize = " ".join([item["text"] for item in srt])
                    lang = detect_language(text_to_summarize)
                    
                    # Force downgrade out of timestamp layout because audio segmentation data is missing
                    summary_mode = "bullets" if req.summary_type == "timestamps" else req.summary_type
                    summary = summarize(text_to_summarize, summary_mode, lang)
                    
                    if req.summary_type == "timestamps":
                        summary = "(Note: Timestamps unavailable due to stream fallback integration mode)\n\n" + summary

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
                        detail="YouTube bot security is blocking this request, and this video does not have any English captions or subtitles available to fall back on."
                    )

            # Standard pipeline execution if audio stream downloads successfully
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
        # restored global error handler wrapper
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clear-cache")
def clear_cache():
    cache_dir = "audio"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)
    return {"status": "cleared"}