from io import BytesIO

from ftlangdetect import detect
from gtts import gTTS, lang


def convert(text: str):
    b = BytesIO()
    detected_lang = detect_lang(text.replace('\n', ' '))['lang']
    supported_langs = lang.tts_langs()

    if detected_lang not in supported_langs:
        detected_lang = 'en'

    tts = gTTS(text=text, lang=detected_lang, lang_check=False)
    tts.write_to_fp(b)
    return b


def detect_lang(text: str):
    return detect(text=text, low_memory=False)
