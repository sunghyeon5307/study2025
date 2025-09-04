import easyocr

class OCR:
    def __init__(self, languages=['ko'], gpu=True):
        self.reader = easyocr.Reader(languages, gpu=gpu, recog_network='korean_g2')

    def run_ocr(self, img_path: str):
        result = self.reader.readtext(img_path, detail=0)
        return result