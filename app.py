import streamlit as st
import os
import shutil
from pipeline.downloader import download_audio, is_playlist, format_duration
from pipeline.transcriber import transcribe, get_transcript_with_timestamps
from pipeline.detector import get_language_message, get_whisper_language_name
from pipeline.summarizer import summarize, summarize_playlist
 
st.set_page_config(
    page_title="SummarizeAI — YouTube Summarizer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 2rem 2rem 4rem; max-width: 1100px; }
  .hero { text-align: center; padding: 3rem 1rem 2rem; }
  .hero-badge { display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; padding: 4px 14px; border-radius: 20px; margin-bottom: 1rem; }
  .hero-title { font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.15; margin: 0 0 1rem; }
  .hero-sub { font-size: 1.1rem; color: #94a3b8; margin: 0 auto 2.5rem; max-width: 520px; line-height: 1.7; }
  .feature-row { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 2.5rem; }
  .feature-chip { background: #1e293b; border: 1px solid #334155; color: #94a3b8; font-size: 12px; font-weight: 500; padding: 5px 14px; border-radius: 20px; }
  .stTextInput > div > div > input { background: #1e293b !important; border: 1px solid #334155 !important; border-radius: 10px !important; color: #f1f5f9 !important; font-size: 15px !important; padding: 0.75rem 1rem !important; }
  .stTextInput > div > div > input:focus { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important; }
  .stTextInput > div > div > input::placeholder { color: #475569 !important; }
  .stButton > button { background: linear-gradient(135deg, #6366f1, #8b5cf6) !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 0.75rem 2.5rem !important; font-weight: 600 !important; font-size: 15px !important; width: 100% !important; transition: all 0.2s ease !important; }
  .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important; }
  .meta-title { font-size: 16px; font-weight: 600; color: #f1f5f9; margin: 0 0 8px; line-height: 1.4; }
  .meta-detail { font-size: 13px; color: #64748b; margin: 0 0 4px; }
  .meta-link { font-size: 13px; color: #6366f1; text-decoration: none; }
  .lang-badge { display: inline-flex; align-items: center; gap: 6px; background: #1e293b; border: 1px solid #334155; color: #a78bfa; font-size: 13px; font-weight: 500; padding: 6px 14px; border-radius: 8px; margin-bottom: 1.25rem; }
  .summary-header { font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin: 0 0 0.75rem; }
  .summary-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding: 1.75rem 2rem; line-height: 1.85; color: #cbd5e1; font-size: 15px; margin-bottom: 1.25rem; }
  .stDownloadButton > button { background: #1e293b !important; color: #a78bfa !important; border: 1px solid #334155 !important; border-radius: 8px !important; font-weight: 500 !important; font-size: 13px !important; }
  [data-testid="stSidebar"] { background: #0f172a !important; border-right: 1px solid #1e293b !important; }
  .sidebar-section { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #475569; margin: 1.5rem 0 0.75rem; }
  hr { border-color: #1e293b !important; margin: 2rem 0 !important; }
  .footer { text-align: center; color: #334155; font-size: 12px; margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid #1e293b; }
  .footer a { color: #6366f1; text-decoration: none; }
</style>
""", unsafe_allow_html=True)
 
# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Controls")
    st.markdown('<p class="sidebar-section">Summary Style</p>', unsafe_allow_html=True)
    summary_style = st.radio(
        "style",
        options=["bullets", "short", "detailed", "timestamps"],
        format_func=lambda x: {
            "bullets": "🔵  Bullet Points",
            "short":   "⚡  Short (3–5 sentences)",
            "detailed":"📖  Detailed",
            "timestamps": "🕐  Key Moments + Timestamps",
        }[x],
        label_visibility="collapsed",
    )
    st.markdown('<p class="sidebar-section">Transcription Quality</p>', unsafe_allow_html=True)
    whisper_size = st.select_slider(
        "quality", options=["tiny", "base", "small"], value="base",
        label_visibility="collapsed",
    )
    st.caption(f"Model: **{whisper_size}** — {'⚡ fastest' if whisper_size == 'tiny' else '⚖️ balanced' if whisper_size == 'base' else '🎯 most accurate'}")
    st.markdown('<p class="sidebar-section">Options</p>', unsafe_allow_html=True)
    show_transcript = st.checkbox("Show full transcript", value=False)
    st.markdown('<p class="sidebar-section">Cache</p>', unsafe_allow_html=True)
    if st.button("🗑️ Clear audio cache"):
        if os.path.exists("audio"):
            shutil.rmtree("audio")
            os.makedirs("audio")
        st.success("Cleared!")
    st.markdown("---")
    st.markdown("""
    <div style="font-size:12px; color:#475569; line-height:1.8;">
    <b style="color:#64748b;">Supports</b><br>
    ✅ Single videos<br>✅ Full playlists<br>✅ Any language → English<br>✅ Timestamp extraction<br><br>
    <b style="color:#64748b;">Stack</b><br>
    🎙️ OpenAI Whisper<br>🤖 Groq LLaMA 3<br>🎬 yt-dlp + ffmpeg
    </div>""", unsafe_allow_html=True)
 
# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">✦ AI-Powered</div>
  <h1 class="hero-title">YouTube Summarizer</h1>
  <p class="hero-sub">Paste any YouTube URL and get an intelligent summary in seconds. Supports any language, playlists, and timestamped key moments.</p>
</div>
<div class="feature-row">
  <span class="feature-chip">🌐 Auto language detection</span>
  <span class="feature-chip">🕐 Timestamp markers</span>
  <span class="feature-chip">📋 Playlist support</span>
  <span class="feature-chip">⚡ 4 summary styles</span>
  <span class="feature-chip">💾 Download summary</span>
</div>
""", unsafe_allow_html=True)
 
# ── Input ─────────────────────────────────────────────────────────────────────
url = st.text_input("url", placeholder="🔗  Paste YouTube URL here — video or playlist", label_visibility="collapsed")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    go = st.button("✨  Summarize Now", use_container_width=True)
st.markdown("---")
 
# ── Pipeline ──────────────────────────────────────────────────────────────────
if go and url:
    playlist_mode = is_playlist(url)
    try:
        with st.status("⬇️  Downloading audio...", expanded=True) as status:
            st.write("Connecting to YouTube and extracting audio track...")
            audio_path, meta = download_audio(url)
            st.write("✅  Audio extracted successfully")
            status.update(label="✅  Audio ready", state="complete")
 
        if playlist_mode and isinstance(audio_path, list):
            st.info(f"📋  Playlist detected — {len(audio_path)} videos found")
            all_transcripts = []
            progress = st.progress(0, text="Processing videos...")
            for i, (path, m) in enumerate(zip(audio_path, meta)):
                with st.status(f"🎙️  Video {i+1}/{len(audio_path)}: {m['title'][:50]}..."):
                    result = transcribe(path, model_size=whisper_size)
                    lang_name = get_whisper_language_name(result["language"])
                    all_transcripts.append({"title": m["title"], "text": result["text"], "language": lang_name, "segments": result["segments"]})
                progress.progress((i + 1) / len(audio_path), text=f"Processed {i+1}/{len(audio_path)} videos")
            with st.status("🧠  Generating playlist summary..."):
                summary = summarize_playlist(all_transcripts, style=summary_style)
            st.markdown("## 📋  Playlist Summary")
            for m in meta:
                st.markdown(f"**{m['title']}** · _{format_duration(m['duration'])}_")
            st.markdown("---")
            st.markdown(f'<div class="summary-card">{summary}</div>', unsafe_allow_html=True)
            st.download_button("💾  Download summary", data=summary, file_name="playlist_summary.txt", mime="text/plain")
 
        else:
            col_img, col_info = st.columns([1, 3])
            with col_img:
                if meta.get("thumbnail"):
                    st.image(meta["thumbnail"], use_container_width=True)
            with col_info:
                st.markdown(f'<p class="meta-title">{meta["title"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="meta-detail">⏱️ {format_duration(meta["duration"])}</p>', unsafe_allow_html=True)
                st.markdown(f'<a class="meta-link" href="{meta["url"]}" target="_blank">🔗 Open on YouTube ↗</a>', unsafe_allow_html=True)
            st.markdown("---")
 
            with st.status("🎙️  Transcribing audio...", expanded=True) as status:
                st.write(f"Running Whisper **{whisper_size}** model...")
                result = transcribe(audio_path, model_size=whisper_size)
                lang_code = result["language"]
                lang_name = get_whisper_language_name(lang_code)
                status.update(label="✅  Transcription complete", state="complete")
 
            flag = "🇬🇧" if lang_code == "en" else "🌐"
            arrow = "" if lang_code == "en" else " → summarizing in English"
            st.markdown(f'<div class="lang-badge">{flag} Language detected: <strong>{lang_name}</strong>{arrow}</div>', unsafe_allow_html=True)
 
            transcript_for_summary = get_transcript_with_timestamps(result["segments"]) if summary_style == "timestamps" else result["text"]
 
            with st.status("🧠  Generating summary...", expanded=True) as status:
                st.write(f"Analyzing with AI — style: **{summary_style}**...")
                summary = summarize(transcript=transcript_for_summary, style=summary_style, video_title=meta["title"], language=lang_name)
                status.update(label="✅  Summary ready", state="complete")
 
            st.markdown('<p class="summary-header">📝 Summary</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-card">', unsafe_allow_html=True)
            st.markdown(summary)
            st.markdown('</div>', unsafe_allow_html=True)
 
            col_dl, _ = st.columns([1, 3])
            with col_dl:
                st.download_button("💾  Download summary",
                    data=f"# {meta['title']}\nLanguage: {lang_name}\nStyle: {summary_style}\n\n{summary}",
                    file_name="summary.txt", mime="text/plain")
 
            if show_transcript:
                st.markdown("---")
                st.markdown('<p class="summary-header">📄 Full Transcript</p>', unsafe_allow_html=True)
                with st.expander("View timestamped transcript", expanded=False):
                    st.text(get_transcript_with_timestamps(result["segments"]))
 
    except Exception as e:
        st.error(f"❌  {str(e)}")
        st.markdown("**Common fixes:** Make sure the URL is a valid public YouTube video · Private/age-restricted videos cannot be processed · Try a shorter video first")
 
elif go and not url:
    st.warning("⚠️  Please paste a YouTube URL first.")
 
st.markdown("""
<div class="footer">
  Built with Whisper · Groq LLaMA 3 · Streamlit &nbsp;·&nbsp;
  By <a href="https://www.linkedin.com/in/muneera-ibrahim-79561a255" target="_blank">Muneera Ibrahim</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/muneeracodes" target="_blank">GitHub ↗</a>
</div>
""", unsafe_allow_html=True)