import yt_dlp
import os


_ffmpeg_dir = r"C:\ffmpeg\bin"

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
        "ffmpeg_location": _ffmpeg_dir,
        "quiet": True,
        "no_warnings": True,
    }

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