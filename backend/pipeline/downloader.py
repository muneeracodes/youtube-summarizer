import yt_dlp
import os

# Dynamically set the FFmpeg directory based on the execution environment.
# Local Windows path is used as a fallback if a global system binary is not found.
_ffmpeg_dir = r"C:\ffmpeg\bin" if os.name == 'nt' else None

def download_audio(url: str, output_dir: str = "audio"):
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(id)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "no_warnings": True,
        
        # 🌟 BYPASS BOT DETECTION ON RENDER
        # Configures client impersonation to spoof standard Safari web traffic patterns
        "extractor_args": {
            "youtube": {
                "player_client": ["web_safari"]
            }
        }
    }

    # Only include the explicit ffmpeg_location parameter if running locally on Windows
    if _ffmpeg_dir and os.path.exists(_ffmpeg_dir):
        ydl_opts["ffmpeg_location"] = _ffmpeg_dir

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        if "entries" in info:
            files, metas = [], []
            for entry in info["entries"]:
                if entry:
                    files.append(f"{output_dir}/{entry['id']}.mp3")
                    metas.append({
                        "title": entry.get("title", "Unknown"),
                        "duration": entry.get("duration", 0),
                        "url": entry.get("webpage_url", url),
                        "thumbnail": entry.get("thumbnail", ""),
                    })
            return files, metas
        else:
            path = f"{output_dir}/{info['id']}.mp3"
            meta = {
                "title": info.get("title", "Unknown"),
                "duration": info.get("duration", 0),
                "url": info.get("webpage_url", url),
                "thumbnail": info.get("thumbnail", ""),
            }
            return path, meta


def is_playlist(url: str) -> bool:
    return "playlist" in url or "list=" in url


def format_duration(seconds: int) -> str:
    if not seconds:
        return "Unknown"
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    if hours:
        return f"{hours}h {mins}m {secs}s"
    return f"{mins}m {secs}s"