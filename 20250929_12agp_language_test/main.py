from ultralytics import YOLO
import cv2, subprocess, numpy as np
import time
import easyocr, re

reader_ko = easyocr.Reader(['ko'], gpu=True)
reader_ja = easyocr.Reader(['ja'], gpu=True)
reader_en = easyocr.Reader(['en'], gpu=True)
reader_ch_sim = easyocr.Reader(['ch_sim'], gpu=True)
reader_ch_tra = easyocr.Reader(['ch_tra'], gpu=True)
reader_fr = easyocr.Reader(['fr'], gpu=True)
reader_vi = easyocr.Reader(['vi'], gpu=True)



def draw_boxes(img, results):
    vis = img.copy()
    for bbox, _, _ in results:
        pts = [(int(x), int(y)) for (x, y) in bbox]
        for j in range(4):
            p1, p2 = pts[j], pts[(j+1) % 4]
            cv2.line(vis, p1, p2, (0,255,0), 2)
    return vis


def ocr_check(img, show=True):

    conf = 0.3

    candidates = {
        "ko": reader_ko.readtext(img, detail=1, paragraph=False),
        "ja": reader_ja.readtext(img, detail=1, paragraph=False),
        "ch_sim": reader_ch_sim.readtext(img, detail=1, paragraph=False),
        "ch_tra": reader_ch_tra.readtext(img, detail=1, paragraph=False),
        "fr": reader_fr.readtext(img, detail=1, paragraph=False),
        "vi": reader_vi.readtext(img, detail=1, paragraph=False),
    }
    lang_en = reader_en.readtext(img, detail=1, paragraph=False)

    best_lang, best_results = None, []
    best_score = -1

    for lang, results in candidates.items():
        valid = [r for r in results if r[2] >= conf]
        if valid:
            avg_conf = sum(c for _, _, c in valid) / len(valid)
            score = len(valid) * avg_conf
            if score > best_score:
                best_score = score
                best_lang, best_results = lang, valid

    lang_en = [r for r in lang_en if r[2] >= 0.8]

    all_results = best_results + lang_en

    texts = [t for _, t, _ in all_results]
    print(f"[{best_lang}]인식된 텍스트:", texts)

    if show:
        vis = draw_boxes(img, all_results)
        h, w = vis.shape[:2]
        vis_small = cv2.resize(vis, (max(1, w//3), max(1, h//3)), interpolation=cv2.INTER_AREA)
        cv2.imshow("ocr", vis_small); 
        cv2.waitKey(1)

    return all_results


def cap_screen():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)


img = cap_screen()
ocr_check(img)

cv2.waitKey(0)
cv2.destroyAllWindows()
