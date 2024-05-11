import requests


class OCR:
    def __init__(self, api_key):
        self.api_key = api_key

    def ocr_space_file(self, filename, overlay=False, engine=2, lang='eng', file_type='Auto',
                       detect_orientation=False, scale=True, detect_checkbox=False):
        payload = {
            'isOverlayRequired': overlay,
            'apikey': self.api_key,
            'language': lang,
            'FileType': file_type,
            'detectOrientation': detect_orientation,
            'scale': scale,
            'OCREngine': engine,
            'detectCheckbox': detect_checkbox,
        }

        with open(filename, 'rb') as f:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={filename: f},
                data=payload,
            )
        return response.json()
