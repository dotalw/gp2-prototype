from io import BytesIO

from ftlangdetect import detect
from gtts import gTTS, lang


def convert(text: str):
    b = BytesIO()
    detected_lang = detect(text=text, low_memory=False).get('lang', 'en')
    if detected_lang not in lang.tts_langs():
        detected_lang = 'en'
    gTTS(text=text, lang=detected_lang, lang_check=False).write_to_fp(b)
    return b


def detect_lang(text: str):
    return detect(text=text, low_memory=False)
