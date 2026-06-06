<div align="center">

# 🎬 YouTube Summarizer

**Paste any YouTube URL — get an intelligent summary in seconds.**

Supports any language · Full playlists · 4 summary styles · Timestamped key moments

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Visit_App-6366f1?style=for-the-badge)](https://youtube-summarizer-frontend-woad.vercel.app/)
[![Backend API](https://img.shields.io/badge/⚡_Backend_API-Render-22c55e?style=for-the-badge)](https://youtube-summarizer-alcl.onrender.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

![App Screenshot](/frontend/src/assets/Screenshot.png)(/frontend/src/assets/Screenshot02.png)

</div>

---

## 🧠 The Problem It Solves

People waste hours watching long YouTube videos just to extract a few key points. Creators post hour-long tutorials, lectures, and podcasts — but viewers often only need the core idea in 2 minutes.

**YouTube Summarizer** solves this by turning any YouTube video or playlist into a clean, structured summary — in seconds, in any language.

---

## ✨ Features

- **4 Summary Styles** — Bullet points, short (3–5 sentences), detailed, or timestamped key moments
- **Multilingual** — Auto-detects spoken language (Urdu, Hindi, Spanish, etc.), always outputs English
- **Playlist Support** — Summarizes up to 10 videos in a playlist with a combined overview
- **Smart Transcript Pipeline** — Uses YouTube captions first (instant), falls back to Groq Whisper AI only when needed
- **Long Video Support** — Automatically chunks transcripts so even hour-long videos work
- **In-Memory Cache** — Same video won't be re-processed, responses are instant on repeat
- **Download Summaries** — Save any summary as a `.txt` file

---

## 🏗️ How It Works

```
YouTube URL
     │
     ▼
 FastAPI Backend (Render)
     │
     ├── Step 1: youtube-transcript-api ──► Captions found → instant transcript ✅
     │                                      (no download, no FFmpeg, works everywhere)
     │
     └── Step 2: Groq Whisper (fallback) ──► No captions? Download audio → transcribe
     │
     ▼
 Chunk long transcripts (prevents LLM context overflow)
     │
     ▼
 Groq LLaMA 3.3 70B (summarize with chosen style)
     │
     ▼
 React Frontend (Vercel) ──► Display + Download
```

**Why not just use yt-dlp for everything?**
YouTube actively blocks audio downloads from cloud server IPs (Render, Railway, etc.). Using `youtube-transcript-api` as the primary method means the app reliably works in production. Whisper is kept as a real fallback for videos that genuinely have no captions.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18 + Vite |
| **Backend** | FastAPI + Python 3.11 |
| **Transcription (primary)** | `youtube-transcript-api` — no download needed |
| **Transcription (fallback)** | Groq Whisper `whisper-large-v3` |
| **Summarization** | Groq LLaMA 3.3 `llama-3.3-70b-versatile` |
| **Backend hosting** | Render.com (Docker) |
| **Frontend hosting** | Vercel |

---

## 📁 Project Structure

```
youtube-summarizer/
├── backend/
│   ├── main.py                   # FastAPI app, routes, in-memory cache
│   ├── pipeline/
│   │   ├── transcript.py         # youtube-transcript-api (primary method)
│   │   ├── whisper_fallback.py   # Groq Whisper (fallback for no-caption videos)
│   │   ├── summarizer.py         # LLaMA 3.3 + transcript chunking logic
│   │   └── utils.py              # URL parsing, video ID extraction, playlist helpers
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main UI component
│   │   └── App.css               # Dark theme styling
│   ├── package.json
│   └── .env.example
├── render.yaml                   # Render deployment config
└── README.md
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- [Groq API key](https://console.groq.com) (free)

### 1. Clone the repo
```bash
git clone https://github.com/muneeracodes/youtube-summarizer.git
cd youtube-summarizer
```

### 2. Backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env → add your GROQ_API_KEY

uvicorn main:app --reload
# → http://localhost:8000
```

### 3. Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local → set VITE_API_URL=http://localhost:8000

npm run dev
# → http://localhost:5173
```

---

## ☁️ Deploy Your Own

### Backend → Render.com

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo
3. Set **Root Directory** → `backend`
4. Set **Environment** → `Docker`
5. Add env var: `GROQ_API_KEY` = your key
6. Add env var: `ALLOWED_ORIGINS` = your Vercel URL
7. Deploy → copy the service URL

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project** → import repo
2. Set **Root Directory** → `frontend`
3. Add env var: `VITE_API_URL` = your Render URL
4. Deploy

---

## 🔑 Environment Variables

### Backend (`backend/.env`)
| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Free at [console.groq.com](https://console.groq.com) |
| `ALLOWED_ORIGINS` | ✅ | Your Vercel URL (for CORS) |

### Frontend (`frontend/.env.local`)
| Variable | Required | Description |
|---|---|---|
| `VITE_API_URL` | ✅ | Your Render backend URL |

---

## 📬 API Reference

### `POST /summarize`
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "style": "bullets"
}
```
**Styles:** `bullets` · `short` · `detailed` · `timestamps`

**Response:**
```json
{
  "video_id": "VIDEO_ID",
  "title": "Video Title",
  "summary": "- Key point one\n- Key point two...",
  "transcript_method": "captions",
  "cached": false
}
```

### `POST /summarize/playlist`
```json
{
  "url": "https://www.youtube.com/playlist?list=PLAYLIST_ID",
  "style": "short"
}
```

### `GET /health`
Returns `{ "status": "ok" }` — used by Render for health checks.

---

## 👩‍💻 Author

**Muneera Ibrahim**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077b5?style=flat&logo=linkedin)](https://www.linkedin.com/in/muneera-ibrahim-79561a255)
[![GitHub](https://img.shields.io/badge/GitHub-muneeracodes-333?style=flat&logo=github)](https://github.com/muneeracodes)
