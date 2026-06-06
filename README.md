# YouTube Intelligence Pipeline

Transforms long-form YouTube videos and full playlists into structured
summaries, key insights, and timestamped markers — with automatic multilingual
detection. Paste a URL, get a production-quality briefing document in seconds.

**Live demo:** [link] <!-- deploy to Render/Railway free tier and add this -->

![Demo GIF] <!-- record with LICEcap or Kap and add here — this is critical -->

---

## The problem it solves

Researchers, students, and content teams spend hours watching long videos
to extract key information. This pipeline reduces that to a 30-second
automated workflow — regardless of the video's original language.

---

## Architecture

YouTube URL
│
▼
yt-dlp (audio extraction)
│
▼
FFmpeg (audio processing)
│
▼
Groq Whisper API (speech-to-text, multilingual)
│
▼
langdetect (language identification)
│
▼
Groq LLaMA 3.3 70B (summarization, insight extraction, timestamp generation)
│
▼
React Frontend (summary display, format selection, export)

---

## Stack

| Layer | Technology |
|---|---|
| Frontend | React · JavaScript · CSS |
| Backend | Python · Flask |
| Speech-to-Text | Groq Whisper API (distil-whisper-large-v3-en) |
| LLM Inference | Groq · LLaMA 3.3 70B Versatile |
| Language Detection | langdetect |
| Audio Processing | yt-dlp · FFmpeg |

---

## Key capabilities

- Single video or full playlist processing
- Automatic language detection — outputs English regardless of input language
  (tested: Urdu, Hindi, Spanish)
- Four output modes: bullet summary, short synthesis, in-depth overview,
  timestamped markers
- Processes a 1-hour video in under 90 seconds via Groq's inference speed

---

## Local setup

**Requirements:** Python 3.10+, FFmpeg, Node.js 18+

```bash
# Clone
git clone https://github.com/muneeracodes/youtube-summarizer.git
cd youtube-summarizer

# Backend
cd backend
pip install -r requirements.txt
# Add your GROQ_API_KEY to .env
python app.py

# Frontend
cd ../frontend
npm install
npm run dev
```

---

## What I'd add next

- Export to Notion / Google Docs via API
- n8n automation: trigger summarization on new YouTube subscriptions
- Fine-tuned prompt templates by content type (lecture, podcast, tutorial)
