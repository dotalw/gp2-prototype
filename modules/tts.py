from io import BytesIO

from gtts import gTTS


def convert(text: str, lang: str = 'fr'):
    b = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(b)
    return b
