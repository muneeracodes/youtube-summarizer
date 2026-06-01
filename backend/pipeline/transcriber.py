import whisper
import os

_model = None

def load_model(size: str = "base"):
    global _model
    if _model is None:
        _model = whisper.load_model(size)
    return _model

def transcribe(audio_path: str, model_size: str = "base") -> dict:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    model = load_model(model_size)
    result = model.transcribe(audio_path, verbose=False, task="transcribe")
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
            "timestamp": format_timestamp(seg["start"]),
        })
    return {
        "text": result["text"].strip(),
        "language": result["language"],
        "segments": segments,
    }

def format_timestamp(seconds: float) -> str:
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def get_transcript_with_timestamps(segments: list) -> str:
    if not segments:
        return ""
    lines = []
    chunk_text = []
    chunk_start = segments[0]["timestamp"]
    chunk_duration = 0
    for seg in segments:
        chunk_text.append(seg["text"])
        chunk_duration += (seg["end"] - seg["start"])
        if chunk_duration >= 30:
            lines.append(f"[{chunk_start}] {' '.join(chunk_text)}")
            chunk_text = []
            chunk_start = seg["timestamp"]
            chunk_duration = 0
    if chunk_text:
        lines.append(f"[{chunk_start}] {' '.join(chunk_text)}")
    return "\n".join(lines)