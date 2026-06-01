from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 42

LANGUAGE_NAMES = {
    "en": "English", "ur": "Urdu", "ar": "Arabic",
    "fr": "French", "de": "German", "es": "Spanish",
    "zh-cn": "Chinese", "hi": "Hindi", "pt": "Portuguese",
    "ru": "Russian", "ja": "Japanese", "ko": "Korean",
    "it": "Italian", "tr": "Turkish", "nl": "Dutch",
    "pl": "Polish", "sv": "Swedish", "fa": "Persian",
    "bn": "Bengali", "pa": "Punjabi",
}

def detect_language(text) -> str:
    try:
        # Force to string no matter what comes in
        if isinstance(text, dict):
            text = text.get("text", "")
        if not isinstance(text, str):
            text = str(text)
        text = text.strip()
        if len(text) < 10:
            return "English"
        code = detect(text[:500])
        return LANGUAGE_NAMES.get(code, "English")
    except Exception:
        return "English"