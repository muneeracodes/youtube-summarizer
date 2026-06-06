import axios from "axios";
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
export async function summarizeVideo(url, summaryType, modelSize) {
  const response = await axios.post(`${API_BASE_URL}/api/summarize`, {
    url: url,
    summary_type: summaryType,
    model_size: modelSize
  });
  return response.data;
};