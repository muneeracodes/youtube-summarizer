import axios from "axios";

export async function summarizeVideo(url, summaryType, modelSize) {
  const response = await axios.post("/api/summarize", {
    url,
    summary_type: summaryType,
    model_size: modelSize,
  });
  return response.data;
}