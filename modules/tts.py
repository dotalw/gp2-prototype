from io import BytesIO

from gtts import gTTS


def convert(text: str):
    b = BytesIO()
    tts = gTTS(text=text, lang='en')
    tts.write_to_fp(b)
    return b
