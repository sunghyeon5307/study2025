from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='korean')
res = ocr.predict(r"C:\study\test.png")

if not res:
    print("❌ 인식 결과가 비어있습니다.")
else:
    item = res[0]
    # 여러 버전 대응: 어떤 key가 있는지 확인
    boxes  = item.get("boxes") or item.get("det_polygons") or item.get("det_boxes")
    texts  = item.get("rec_texts") or item.get("texts")
    scores = item.get("rec_scores") or item.get("scores")

    if boxes and texts:
        for b, t, s in zip(boxes, texts, scores or [None]*len(texts)):
            print("text:", t, "| score:", s, "| box:", b)
    else:
        print("❌ boxes/texts 키를 찾을 수 없음. item 구조:", item.keys())
