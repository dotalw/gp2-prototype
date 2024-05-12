from io import BytesIO

from ftlangdetect import detect
from gtts import gTTS


def convert(text: str):
    b = BytesIO()
    tts = gTTS(text=text, lang=detect_lang(text.replace('\n', ' '))['lang'], lang_check=False)
    tts.write_to_fp(b)
    return b


def detect_lang(text: str):
    return detect(text=text, low_memory=False)
