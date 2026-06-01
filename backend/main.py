from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import shutil

sys.path.append(os.path.dirname(__file__))

from pipeline.downloader import download_audio, is_playlist, format_duration
from pipeline.transcriber import transcribe, get_transcript_with_timestamps
from pipeline.detector import detect_language
from pipeline.summarizer import summarize

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    url: str
    summary_type: str = "bullets"
    model_size: str = "base"

@app.post("/api/summarize")
async def summarize_video(req: SummarizeRequest):
    try:
        playlist = is_playlist(req.url)

        if playlist:
            audio_files, metas = download_audio(req.url)
            results = []
            for audio_path, meta in zip(audio_files, metas):
                transcript_data = transcribe(audio_path, req.model_size)
                plain_text = transcript_data["text"]
                segments = transcript_data["segments"]

                lang = detect_language(plain_text)

                if req.summary_type == "timestamps":
                    text_to_summarize = get_transcript_with_timestamps(segments)
                else:
                    text_to_summarize = plain_text

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
            audio_path, meta = download_audio(req.url)
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