from paddleocr import PaddleOCR

ocr = PaddleOCR(lang='korean', use_angle_cls=True)
img_path = r"C:\Users\sungh\OneDrive\바탕 화면\easyocr_study\image.png"

result = ocr.ocr(img_path)

print("결과")
for line in result[0]:
    box = line[0]
    info = line[1]

    if isinstance(info, (list, tuple)) and len(info) == 2:
        text, score = info
        print(f"{text} (score: {score:.3f})")
print(result)