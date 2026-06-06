import yt_dlp
import os

# Cross-platform environment resolution for FFmpeg
_ffmpeg_dir = r"C:\ffmpeg\bin" if os.name == 'nt' else None

# Absolute path to cookies.txt — always finds it regardless of where the server is launched from
_cookies_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies.txt")

def get_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    else:
        return url.split("/")[-1].split("?")[0]

def download_audio(url: str, output_dir: str = "audio"):
    os.makedirs(output_dir, exist_ok=True)
    video_id = get_video_id(url)

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
        "extractor_args": {
            "youtube": {
                "player_client": ["ios", "android"],
                "skip": ["dash", "hls"]
            }
        },
        "http_headers": {
            "User-Agent": "com.google.ios.youtube/19.17.2 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X; en_US)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
    }

    # Only add cookiefile if it actually exists — prevents yt-dlp from crashing when file is missing
    if os.path.exists(_cookies_path):
        ydl_opts["cookiefile"] = _cookies_path
        print(f"[Downloader] Using cookies from: {_cookies_path}")
    else:
        print(f"[Downloader] WARNING: cookies.txt not found at {_cookies_path} — proceeding without cookies")

    if _ffmpeg_dir and os.path.exists(_ffmpeg_dir):
        ydl_opts["ffmpeg_location"] = _ffmpeg_dir

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if "entries" in info:
                files, metas = [], []
                for entry in info["entries"]:
                    if entry:
                        files.append(f"{output_dir}/{entry['id']}.mp3")
                        metas.append({
                            "title": entry.get("title", "Unknown Playlist Item"),
                            "duration": entry.get("duration", 0),
                            "url": entry.get("webpage_url", url),
                            "thumbnail": entry.get("thumbnail", ""),
                        })
                return files, metas
            else:
                path = f"{output_dir}/{info['id']}.mp3"
                meta = {
                    "title": info.get("title", "Unknown Video"),
                    "duration": info.get("duration", 0),
                    "url": info.get("webpage_url", url),
                    "thumbnail": info.get("thumbnail", ""),
                }
                return path, meta

    except Exception as e:
        print(f"[Core Guard] yt-dlp completely blocked. Switching to isolated transcript mode: {str(e)}")

        meta = {
            "title": "YouTube Video Resource",
            "duration": 0,
            "url": url,
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        }
        return None, meta


def is_playlist(url: str) -> bool:
    return "playlist" in url or "list=" in url


def format_duration(seconds: int) -> str:
    if not seconds:
        return "Automatic Tracking"
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    if hours:
        return f"{hours}h {mins}m {secs}s"
    return f"{mins}m {secs}s"