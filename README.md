# 🎬 AI-Powered YouTube Summarizer & Timestamp Extractor

A sleek, full-stack intelligence pipeline that transforms lengthy YouTube videos or full playlists into structured markdown summaries, actionable takeaways, and timestamped chronological markers. Built using a localized system-level transcription layout paired with blazing-fast cloud inference.

---

## 🚀 Key Features

- **Double-Mode Scope:** Seamlessly parses single video links or complete public YouTube Playlists.
- **Hybrid AI Architecture:** Orchestrates high-speed system processing via `yt-dlp` and `FFmpeg` with cloud-hosted LLM processing.
- **Multilingual Intelligence:** Automatically evaluates and identifies input spoken dialects (e.g., Urdu, Hindi, Spanish) and outputs perfectly structured English summaries.
- **Adaptive Execution Layouts:** Offers custom summary formatting—Bullet Points, Short Syntheses, In-Depth Overviews, or Sequential Time-Stamps.

---

## 🛠️ System Architecture & Tech Stack

- **Frontend Core:** Streamlit Interactive Dynamic Dashboard Engine
- **Audio Scraper:** `yt-dlp` + Native System `FFmpeg` Media Layer
- **Speech-to-Text Processing:** Groq Cloud-Optimized Whisper API (`distil-whisper-large-v3-en`)
- **Inference Engine:** Groq LLaMA 3.3 Versatile Core Architecture (`llama-3.3-70b-versatile`)
- **Language Profiler:** `langdetect` Factory Configuration Matrix

---

## 📋 Installation & Local Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** and **FFmpeg** installed on your operating system.

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME