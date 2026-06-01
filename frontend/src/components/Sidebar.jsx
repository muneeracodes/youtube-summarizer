import { useState } from "react";
import {
  Trash2, CheckCircle2, ChevronDown, ChevronUp,
  Mic2, Zap, Play, Globe, Clock, List, Info
} from "lucide-react";

const HOW_TO_STEPS = [
  { icon: "1️⃣", title: "Paste a URL", desc: "Copy any YouTube video or playlist link and paste it into the input field." },
  { icon: "2️⃣", title: "Choose style", desc: "Pick Bullet Points, Short, Detailed, or Key Moments with timestamps." },
  { icon: "3️⃣", title: "Select quality", desc: "Tiny is fastest for testing. Base gives better accuracy." },
  { icon: "4️⃣", title: "Click Summarize", desc: "Wait ~1–3 min depending on video length. The pipeline runs Whisper locally." },
  { icon: "5️⃣", title: "Copy & use", desc: "Copy the summary with one click and use it anywhere." },
];

const SUPPORTS = [
  { icon: <Play size={13} />, label: "Single videos" },
  { icon: <List size={13} />, label: "Full playlists" },
  { icon: <Globe size={13} />, label: "Any language → English" },
  { icon: <Clock size={13} />, label: "Timestamp extraction" },
];

const STACK = [
  { icon: "🎙️", label: "OpenAI Whisper" },
  { icon: "⚡", label: "Groq LLaMA 3" },
  { icon: "📥", label: "yt-dlp + ffmpeg" },
  { icon: "🐍", label: "FastAPI backend" },
  { icon: "⚛️", label: "React + Tailwind" },
];

export default function Sidebar({ onClearCache }) {
  const [howToOpen, setHowToOpen] = useState(true);
  const [cleared, setCleared] = useState(false);

  const handleClear = () => {
    onClearCache();
    setCleared(true);
    setTimeout(() => setCleared(false), 2500);
  };

  return (
    <aside className="w-72 shrink-0 border-r border-white/[0.06] bg-white/[0.02] backdrop-blur-xl min-h-screen p-5 flex flex-col gap-6 overflow-y-auto">

      {/* Logo */}
      <div className="flex items-center gap-2.5 pt-2 pb-1">
        <div className="w-8 h-8 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-base">
          🎬
        </div>
        <div>
          <p className="text-white font-semibold text-sm leading-none">YT Summarizer</p>
          <p className="text-white/30 text-xs mt-0.5">AI-powered · Free</p>
        </div>
      </div>

      <div className="h-px bg-white/[0.06]" />

      {/* How to use */}
      <div>
        <button
          onClick={() => setHowToOpen(!howToOpen)}
          className="w-full flex items-center justify-between text-white/50 text-xs uppercase tracking-widest font-medium mb-3 hover:text-white/70 transition-colors"
        >
          <span className="flex items-center gap-1.5"><Info size={12} /> How to use</span>
          {howToOpen ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
        </button>

        {howToOpen && (
          <div className="space-y-3">
            {HOW_TO_STEPS.map((s, i) => (
              <div key={i} className="flex gap-3 p-3 bg-white/[0.03] border border-white/[0.06] rounded-xl">
                <span className="text-base shrink-0 mt-0.5">{s.icon}</span>
                <div>
                  <p className="text-white text-xs font-medium">{s.title}</p>
                  <p className="text-white/40 text-xs mt-0.5 leading-relaxed">{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="h-px bg-white/[0.06]" />

      {/* Supports */}
      <div>
        <p className="text-white/50 text-xs uppercase tracking-widest font-medium mb-3">Supports</p>
        <div className="space-y-2">
          {SUPPORTS.map((item, i) => (
            <div key={i} className="flex items-center gap-2.5 text-sm text-white/60">
              <CheckCircle2 size={14} className="text-emerald-400 shrink-0" />
              <span className="flex items-center gap-1.5">
                <span className="text-white/30">{item.icon}</span>
                {item.label}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="h-px bg-white/[0.06]" />

      {/* Stack */}
      <div>
        <p className="text-white/50 text-xs uppercase tracking-widest font-medium mb-3">
          <span className="flex items-center gap-1.5"><Zap size={12} /> Stack</span>
        </p>
        <div className="space-y-2">
          {STACK.map((item, i) => (
            <div key={i} className="flex items-center gap-2.5 text-xs text-white/50">
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="h-px bg-white/[0.06]" />

      {/* Cache clear */}
      <div>
        <p className="text-white/50 text-xs uppercase tracking-widest font-medium mb-3">
          <span className="flex items-center gap-1.5"><Mic2 size={12} /> Cache</span>
        </p>
        <button
          onClick={handleClear}
          className={`w-full flex items-center justify-center gap-2 rounded-xl py-2.5 text-sm font-medium border transition-all duration-200 ${
            cleared
              ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
              : "bg-red-500/10 border-red-500/20 text-red-400 hover:bg-red-500/20"
          }`}
        >
          {cleared ? (
            <><CheckCircle2 size={14} /> Cleared!</>
          ) : (
            <><Trash2 size={14} /> Clear audio cache</>
          )}
        </button>
        <p className="text-white/25 text-xs mt-2 text-center">
          Removes downloaded .mp3 files
        </p>
      </div>

    </aside>
  );
}