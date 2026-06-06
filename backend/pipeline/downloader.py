import yt_dlp
import os

# Cross-platform environment resolution for FFmpeg
_ffmpeg_dir = r"C:\ffmpeg\bin" if os.name == 'nt' else None

def download_audio(url: str, output_dir: str = "audio"):
    os.makedirs(output_dir, exist_ok=True)

    # 🌟 ADVANCED PRODUCTION CONFIGURATION FOR YT-DLP
    # Uses iOS mobile app headers to route requests safely past cloud datacenter blocks
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
        
        # Emulate native mobile app behavior to bypass strict datacenter checks
        "extractor_args": {
            "youtube": {
                "player_client": ["ios", "android"],
                "skip": ["dash", "hls"]
            }
        },
        "http_headers": {
            "User-Agent": "com.google.ios.youtube/19.17.2 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X; en_US)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
        }
    }

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
                
    except Exception as e:
        # Fallback Strategy: If video extraction fails due to IP rate limits,
        # extract metadata safely using the lightweight, unblocked flat-playlist parser
        print(f"[Backup System] yt-dlp stream blocked. Activating lightweight meta parser: {str(e)}")
        
        fallback_opts = {
            'extract_flat': True,
            'skip_download': True,
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(fallback_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
            
            meta = {
                "title": info.get("title", "YouTube Video Resource"),
                "duration": info.get("duration", 0),
                "url": url,
                "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                "use_transcript_fallback": True # Signal to pipeline to skip whisper and use subtitles
            }
            return None, meta


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