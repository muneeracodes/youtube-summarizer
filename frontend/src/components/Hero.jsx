export default function Hero() {
  return (
    <div className="text-center pt-20 pb-12 px-4">
      <div className="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full px-4 py-1.5 text-sm text-emerald-400 mb-8 backdrop-blur-sm">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
        Whisper · Groq LLaMA 3 · FastAPI · React
      </div>

      <h1 className="text-6xl font-bold tracking-tight mb-5 leading-tight">
        <span className="text-white">YouTube</span>
        <br />
        <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
          Summarizer
        </span>
      </h1>

      <p className="text-white/50 text-lg max-w-lg mx-auto leading-relaxed">
        Paste any video or playlist URL. Get an AI-powered summary with language detection, timestamps, and key insights — in seconds.
      </p>

      <div className="flex items-center justify-center gap-6 mt-8 text-sm text-white/30">
        <span className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-white/20" />
          Language detection
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-white/20" />
          Timestamp markers
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-white/20" />
          Playlist support
        </span>
      </div>
    </div>
  );
}