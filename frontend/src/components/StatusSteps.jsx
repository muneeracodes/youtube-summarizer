import { CheckCircle2, Circle, Loader2 } from "lucide-react";

const STEPS = [
  { id: "download", label: "Downloading audio", icon: "⬇️" },
  { id: "transcribe", label: "Transcribing with Whisper", icon: "🎙️" },
  { id: "detect", label: "Detecting language", icon: "🌐" },
  { id: "summarize", label: "Generating AI summary", icon: "✨" },
];

export default function StatusSteps({ currentStep }) {
  const currentIndex = STEPS.findIndex((s) => s.id === currentStep);

  return (
    <div className="max-w-2xl mx-auto px-4 mt-6">
      <div className="bg-white/[0.04] border border-white/10 rounded-3xl p-6 backdrop-blur-xl">
        <p className="text-white/40 text-xs uppercase tracking-widest mb-4 font-medium">Processing</p>
        <div className="space-y-3">
          {STEPS.map((step, i) => {
            const done = i < currentIndex;
            const active = i === currentIndex;
            const pending = i > currentIndex;
            return (
              <div
                key={step.id}
                className={`flex items-center gap-3 p-3 rounded-xl transition-all duration-500 ${
                  active ? "bg-emerald-500/10 border border-emerald-500/20" :
                  done ? "opacity-60" : "opacity-25"
                }`}
              >
                <div className="w-7 h-7 flex items-center justify-center shrink-0">
                  {done ? (
                    <CheckCircle2 size={18} className="text-emerald-400" />
                  ) : active ? (
                    <Loader2 size={18} className="text-emerald-400 animate-spin" />
                  ) : (
                    <Circle size={18} className="text-white/20" />
                  )}
                </div>
                <span className={`text-sm ${active ? "text-white font-medium" : "text-white/70"}`}>
                  {step.icon} {step.label}
                </span>
                {active && (
                  <span className="ml-auto text-xs text-emerald-400 animate-pulse">Running…</span>
                )}
                {done && (
                  <span className="ml-auto text-xs text-white/30">Done</span>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}