from ultralytics import YOLO
import cv2, subprocess, numpy as np
import time
import easyocr

import cv2, re

music_keyword = ["OFF", "BAND", "DAB", "MODE"]
home_keyword  = ["영상 입력 신호가 없습니다."]

conf_print = 0.8

reader_ko = easyocr.Reader(['ko'], gpu=True)
reader_en = easyocr.Reader(['en'], gpu=True)

def _draw_boxes(base_img, results):
    vis = base_img.copy()
    for bbox, _, _ in results:
        pts = [(int(x), int(y)) for (x, y) in bbox]
        for j in range(4):
            p1, p2 = pts[j], pts[(j+1) % 4]
            cv2.line(vis, p1, p2, (0,255,0), 2)
    return vis

def ocr_check(img, target="music", show=True):
    if img is None or img.size == 0:
        return False

    res_en = reader_en.readtext(img, detail=1, paragraph=False)
    res_ko = reader_ko.readtext(img, detail=1, paragraph=False)
    results = res_en + res_ko

    for _, text, conf in results:
        if conf>=conf_print:
            print(f"{text}  conf={conf:.2f}")

    if show:
        vis = _draw_boxes(img, results)
        h, w = vis.shape[:2]
        vis_small = cv2.resize(vis, (w//3, h//3), interpolation=cv2.INTER_AREA)
        cv2.imshow("ocr", vis_small); cv2.waitKey(1)

    if target == "music":
        found = set()
        for _, text, _ in results:
            up = re.sub(r"\s+", "", text.upper())
            for kw in music_keyword:
                if kw in up:
                    found.add(kw)
        return found.issuperset(set(music_keyword))

    elif target == "home":
        full_ko = "".join([t for _, t, _ in res_ko]) 
        return any(kw in full_ko for kw in home_keyword)

    else:
        return False

file = "touch_log.tsv"

model = YOLO("best.pt")

def cap_screen():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)


def read(result):
    with open("touch_log.tsv", "w", encoding="utf-8") as f:
        for i in result.boxes:
            cls_id = int(i.cls[0])
            cls = model.names[cls_id]

            x1, y1, x2, y2 = map(int, i.xyxy[0].tolist())

            cx, cy = (x1 + x2)//2, (y1 + y2)//2
            
            conf = float(i.conf[0])
            print(f"{cls}: center=({cx},{cy}), conf={conf:.2f}")
            f.write(f"{cls}\t{cx}\t{cy}\n")

def run():
    with open(file, "r", encoding="utf-8") as f:
        for i in f:
            parts = i.strip().split()
            _, x, y = parts  

            subprocess.run(["adb", "shell", "input", "tap", x, y])

            time.sleep(2)  

# music 확인
img = cap_screen()
result = model.predict(source=img, conf=0.45, verbose=False, device=0)[0]
read(result)
run()    
annotated1 = result.plot()
h, w = annotated1.shape[:2]
screen1 = cv2.resize(annotated1, (w//4, h//4), interpolation=cv2.INTER_AREA)
cv2.imshow("music", screen1)
cv2.waitKey(1)

check_img1 = cap_screen()
if ocr_check(check_img1, target="music"):
    print("음악앱 맞습니다")
else:
    print("음악앱 아닙니다.")


# home 확인
img2 = cap_screen()
result = model.predict(source=img2, conf=0.45, verbose=False, device=0)[0]
read(result)
run()
annotated2 = result.plot()
h, w = annotated2.shape[:2]
screen2 = cv2.resize(annotated2, (w//4, h//4), interpolation=cv2.INTER_AREA)
cv2.imshow("home", screen2)
cv2.waitKey(1)

check_img2 = cap_screen()
if ocr_check(check_img2, target="home"):
    print("홈 맞습니다")
else:
    print("홈 아닙니다.")


cv2.waitKey(0)
cv2.destroyAllWindows()