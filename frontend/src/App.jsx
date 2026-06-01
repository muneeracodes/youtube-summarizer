import { useState } from "react";
import Hero from "./components/Hero";
import UrlInput from "./components/UrlInput";
import StatusSteps from "./components/StatusSteps";
import SummaryResult from "./components/SummaryResult";
import Sidebar from "./components/Sidebar";
import { summarizeVideo } from "./api/summarize";
import './index.css'

export default function App() {
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (url, summaryType, modelSize) => {
    setLoading(true);
    setResult(null);
    setError(null);
    setStep("download");

    const steps = ["download", "transcribe", "detect", "summarize"];
    let i = 0;
    const timer = setInterval(() => {
      i++;
      if (i < steps.length) setStep(steps[i]);
    }, 8000);

    try {
      const data = await summarizeVideo(url, summaryType, modelSize);
      clearInterval(timer);
      setResult(data);
    } catch (err) {
      clearInterval(timer);
      setError(err.response?.data?.detail || "Something went wrong. Check the URL and try again.");
    } finally {
      setLoading(false);
      setStep(null);
    }
  };

  const handleClearCache = async () => {
    try {
      await fetch("/api/clear-cache", { method: "POST" });
      alert("Audio cache cleared!");
    } catch {
      alert("Could not clear cache.");
    }
  };

  return (
    <div className="min-h-screen bg-[#070711] text-white">
      {/* Ambient glows */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-[600px] h-[600px] bg-emerald-500/10 rounded-full blur-[120px]" />
        <div className="absolute top-1/2 -right-40 w-[500px] h-[500px] bg-violet-500/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-0 left-1/3 w-[400px] h-[400px] bg-blue-500/8 rounded-full blur-[100px]" />
      </div>

      <div className="relative z-10 flex min-h-screen">

        {/* Sidebar */}
        <Sidebar onClearCache={handleClearCache} />

        {/* Main content */}
        <div className="flex-1 pb-24">
          <Hero />
          <UrlInput onSubmit={handleSubmit} loading={loading} />
          {loading && step && <StatusSteps currentStep={step} />}
          {error && (
            <div className="max-w-2xl mx-auto px-4 mt-6">
              <div className="bg-red-500/10 border border-red-500/20 rounded-2xl px-5 py-4 text-red-400 text-sm flex items-start gap-3">
                <span className="text-lg">⚠️</span>
                <span>{error}</span>
              </div>
            </div>
          )}
          <SummaryResult data={result} />
        </div>

      </div>
    </div>
  );
}