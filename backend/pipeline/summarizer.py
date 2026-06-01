# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
 
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-2.0-flash")
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
# ── Summary style prompts ─────────────────────────────────────────────────────
SUMMARY_PROMPTS = {
    "short": """
You are an expert video summarizer. Provide a concise 3-5 sentence summary of what happens or what is discussed in the transcript.
Be direct, clear, and only rely on explicit facts mentioned. Do not speculate or guess the context.
Always respond in English regardless of the transcript language.
""",
    "detailed": """
You are an expert video summarizer. Provide a detailed breakdown of the transcript content.
Structure your response exactly like this:
Overview: (2-3 sentences explaining the main event)
Main Points: (Detailed points of what happens)
Key Takeaways: (Insights or conclusions)
Always respond in English regardless of the transcript language.
""",
    "bullets": """
You are an expert video summarizer. Analyze the transcript text and convert it into crisp, fact-based bullet points.
Strictly follow this layout:
Topic: [Write a 1-sentence topic of the video here]
Key Points:
- [Point 1]
- [Point 2]
Action Items:
- [Action item if any, otherwise write 'None']

Important: Base your response *only* on the provided transcript text. If the transcript is very short, brief, or contains minimal dialogue, just summarize exactly what those few words say without making up an external story or assuming emotional states.
Always respond in English regardless of the transcript language.
""",
    "timestamps": """
You are an expert video summarizer. Analyze this timestamped transcript and extract key moments.
Format each point exactly as:
[MM:SS] — [What was discussed/happened at this moment]
Extract the most important moments based strictly on the text.
Always respond in English regardless of the transcript language.
""",
}
 
def summarize(transcript, style: str = "bullets", language: str = "English") -> str:
    # Force to string no matter what
    if isinstance(transcript, dict):
        transcript = transcript.get("text", "")
    if not isinstance(transcript, str):
        transcript = str(transcript)
    transcript = transcript.strip()

    if not transcript:
        return "No transcript content found."

    system_prompt = SUMMARY_PROMPTS.get(style, SUMMARY_PROMPTS["bullets"])
    lang_note = ""
    if language.lower() not in ["english", "en"]:
        lang_note = f"\nNote: The transcript is in {language}. Summarize in English.\n"

    full_prompt = f"{system_prompt}\n{lang_note}\nTRANSCRIPT:\n{transcript[:12000]}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.4,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()
 
 
def summarize_playlist(
    transcripts: list,
    style: str = "bullets",
) -> str:
    """
    Summarize an entire playlist — one combined summary.
    transcripts: list of dicts with keys: title, text, language
    """
    combined = ""
    for i, t in enumerate(transcripts, 1):
        combined += f"\n\n--- Video {i}: {t['title']} ---\n{t['text'][:3000]}"
 
    full_prompt = f"""
You are an expert summarizer. You will receive transcripts from multiple videos in a playlist.
Create a comprehensive course/playlist summary that:
- Gives an **Overall Theme** of the playlist
- Summarizes **each video** in 2-3 sentences
- Lists **Key Learnings** across all videos
- Suggests a **Learning Path** based on the content
Always respond in English.
 
PLAYLIST TRANSCRIPTS:
{combined[:14000]}
"""
 
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": full_prompt}],
    temperature=0.4,
    max_tokens=1000,
)
    return response.choices[0].message.content.strip()