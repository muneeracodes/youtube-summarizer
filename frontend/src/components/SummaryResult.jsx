import { ExternalLink, Globe, Clock, Copy, CheckCheck, BookOpen } from "lucide-react";
import { useState } from "react";

function SingleResult({ data }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(data.summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white/[0.04] border border-white/10 rounded-3xl overflow-hidden backdrop-blur-xl shadow-2xl shadow-black/40">

      {data.thumbnail && (
        <div className="relative">
          <img src={data.thumbnail} alt={data.title} className="w-full h-52 object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-[#070711] via-transparent to-transparent" />
        </div>
      )}

      <div className="p-6">

        <div className="flex items-start justify-between gap-4 mb-4">
          <h2 className="text-white font-semibold text-lg leading-snug">
            {data.title}
          </h2>
          <a href={data.url} target="_blank" rel="noreferrer" className="shrink-0 p-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white/40 hover:text-white transition-all">
            <ExternalLink size={14} />
          </a>
        </div>

        <div className="flex flex-wrap gap-2 mb-6">
          <span className="flex items-center gap-1.5 bg-white/5 border border-white/10 rounded-full px-3 py-1 text-xs text-white/50">
            <Clock size={11} /> {data.duration}
          </span>
          <span className="flex items-center gap-1.5 bg-white/5 border border-white/10 rounded-full px-3 py-1 text-xs text-white/50">
            <Globe size={11} /> {data.language}
          </span>
          <span className="flex items-center gap-1.5 bg-emerald-500/10 border border-emerald-500/20 rounded-full px-3 py-1 text-xs text-emerald-400">
            <BookOpen size={11} /> Summary ready
          </span>
        </div>

        <div className="relative bg-black/30 border border-white/[0.06] rounded-2xl p-5">
          <button
            onClick={handleCopy}
            className="absolute top-4 right-4 flex items-center gap-1.5 text-xs text-white/30 hover:text-white transition-colors bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg px-2.5 py-1.5"
          >
            {copied ? (
              <>
                <CheckCheck size={12} className="text-emerald-400" />
                <span className="text-emerald-400">Copied</span>
              </>
            ) : (
              <>
                <Copy size={12} />
                <span>Copy</span>
              </>
            )}
          </button>
          <pre className="text-white/75 text-sm whitespace-pre-wrap leading-relaxed font-sans pr-16">
            {data.summary}
          </pre>
        </div>

      </div>
    </div>
  );
}

export default function SummaryResult({ data }) {
  if (!data) return null;

  if (data.type === "playlist") {
    return (
      <div className="max-w-2xl mx-auto px-4 mt-8 space-y-6">
        <div className="flex items-center gap-3">
          <h2 className="text-white font-semibold text-xl">Playlist Summary</h2>
          <span className="bg-white/10 border border-white/10 rounded-full px-3 py-1 text-xs text-white/50">
            {data.results.length} videos
          </span>
        </div>
        {data.results.map((item, i) => (
          <SingleResult key={i} data={item} />
        ))}
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 mt-8">
      <SingleResult data={data} />
    </div>
  );
}