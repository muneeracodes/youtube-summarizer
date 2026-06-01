import { useState } from "react";
import { Loader2, Sparkles, ChevronDown } from "lucide-react";

const summaryOptions = [
  { value: "bullets", label: "📋 Bullet Points", desc: "Key takeaways as a clean list" },
  { value: "short", label: "⚡ Short Summary", desc: "3 sentence executive overview" },
  { value: "detailed", label: "📄 Detailed Summary", desc: "In-depth breakdown" },
  { value: "timestamps", label: "🕐 Key Moments", desc: "Points with timestamp markers" },
];

const qualityOptions = [
  { value: "tiny", label: "⚡ Tiny", desc: "Fastest — good for testing" },
  { value: "base", label: "⚖️ Base", desc: "Balanced speed & accuracy" },
];

export default function UrlInput({ onSubmit, loading }) {
  const [url, setUrl] = useState("");
  const [summaryType, setSummaryType] = useState("bullets");
  const [modelSize, setModelSize] = useState("base");

  const handleSubmit = () => {
    if (!url.trim() || loading) return;
    onSubmit(url.trim(), summaryType, modelSize);
  };

  return (
    <div className="max-w-2xl mx-auto px-4">
      <div className="bg-white/[0.04] border border-white/10 rounded-3xl p-6 backdrop-blur-xl shadow-2xl shadow-black/40">

        {/* URL Input */}
        <div className="relative mb-5">
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-white/30 text-sm">🔗</div>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            placeholder="https://youtube.com/watch?v=..."
            className="w-full bg-white/[0.06] border border-white/10 rounded-2xl pl-10 pr-4 py-4 text-white placeholder-white/25 focus:outline-none focus:border-emerald-500/50 focus:bg-white/[0.08] transition-all text-sm"
          />
        </div>

        {/* Options Row */}
        <div className="grid grid-cols-2 gap-3 mb-5">
          <div>
            <label className="text-white/35 text-xs font-medium mb-2 block uppercase tracking-wider">Summary Style</label>
            <div className="relative">
              <select
                value={summaryType}
                onChange={(e) => setSummaryType(e.target.value)}
                className="w-full bg-white/[0.06] border border-white/10 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500/50 appearance-none cursor-pointer"
              >
                {summaryOptions.map((o) => (
                  <option key={o.value} value={o.value} className="bg-[#0d0d1a]">{o.label}</option>
                ))}
              </select>
              <ChevronDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-white/30 pointer-events-none" />
            </div>
          </div>

          <div>
            <label className="text-white/35 text-xs font-medium mb-2 block uppercase tracking-wider">Quality</label>
            <div className="relative">
              <select
                value={modelSize}
                onChange={(e) => setModelSize(e.target.value)}
                className="w-full bg-white/[0.06] border border-white/10 rounded-xl px-3 py-2.5 text-white text-sm focus:outline-none focus:border-emerald-500/50 appearance-none cursor-pointer"
              >
                {qualityOptions.map((o) => (
                  <option key={o.value} value={o.value} className="bg-[#0d0d1a]">{o.label}</option>
                ))}
              </select>
              <ChevronDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-white/30 pointer-events-none" />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={loading || !url.trim()}
          className="w-full relative bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 disabled:opacity-30 disabled:cursor-not-allowed text-black font-semibold rounded-2xl py-3.5 flex items-center justify-center gap-2.5 transition-all duration-200 shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/30 text-sm"
        >
          {loading ? (
            <><Loader2 size={16} className="animate-spin" /> Processing video…</>
          ) : (
            <><Sparkles size={16} /> Generate Summary</>
          )}
        </button>
      </div>
    </div>
  );
}