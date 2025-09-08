from paddleocr import PaddleOCR

class OCR:
    def __init__(self, lang='korean'):
        self.reader = PaddleOCR(lang=lang)

    def run_ocr(self, img_path: str):
        result = self.reader.ocr(img_path)
        texts = []
        if result:
            for line in result[0]:
                texts.append(line[1][0])  
        return texts
