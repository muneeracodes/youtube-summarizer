import os
import sys
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
        # Convert Pydantic string safely
        video_url = str(req.url)
        playlist = is_playlist(video_url)

        if playlist:
            audio_files, metas = download_audio(video_url)
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
            audio_path, meta = download_audio(video_url)
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
        # Clean description of errors back to frontend
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clear-cache")
def clear_cache():
    cache_dir = "audio"
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)
    return {"status": "cleared"}