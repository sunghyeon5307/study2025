from ultralytics import YOLO
import cv2, subprocess, numpy as np
import time
import easyocr, re

model = YOLO("best2.pt") # home, menu, audio
model2 = YOLO("best1.pt") # home, menu, audio

file = "touch_log.tsv"

audio_keyword = ["OFF", "BAND", "DAB", "MODE"]
home_keyword  = ["영상 입력 신호가 없습니다."]
menu_keyword = ["소모품 관리", "오디오", "오토 아이들 설정"]

conf_print=0.8

reader_ko = easyocr.Reader(['ko'], gpu=True)
reader_en = easyocr.Reader(['en'], gpu=True)



def draw_boxes(img, results):
    vis = img.copy()
    for bbox, _, _ in results:
        pts = [(int(x), int(y)) for (x, y) in bbox]
        for j in range(4):
            p1, p2 = pts[j], pts[(j+1) % 4]
            cv2.line(vis, p1, p2, (0,255,0), 2)
    return vis

def ocr_check(img, target="audio", show=True):
    if img is None or img.size == 0:
        return False

    res_en = reader_en.readtext(img, detail=1, paragraph=False)
    res_ko = reader_ko.readtext(img, detail=1, paragraph=False)
    results = res_en + res_ko

    texts = [text for _, text, conf in results if conf >= conf_print]
    print("인식된 텍스트:", texts)

    if show:
        vis = draw_boxes(img, results)
        h, w = vis.shape[:2]
        vis_small = cv2.resize(vis, (w//3, h//3), interpolation=cv2.INTER_AREA)
        cv2.imshow("ocr", vis_small); cv2.waitKey(1)

    if target == "audio":
        found = set()
        for _, text, _ in results:
            up = re.sub(r"\s+", "", text.upper())
            for kw in audio_keyword:
                if kw in up:
                    found.add(kw)
        return found.issuperset(set(audio_keyword))

    elif target == "home":
        full_ko = "".join([t for _, t, _ in res_ko]) 
        return all(kw in full_ko for kw in home_keyword)

    elif target == "menu":
        full_ko = "".join([t for _, t, _ in res_ko]) 
        return all(kw in full_ko for kw in menu_keyword)

    else:
        return False



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

img = cap_screen()
result = model.predict(source=img, conf=0.45, verbose=False, device=0)[0]
read(result)
run()    
annotated1 = result.plot()
h, w = annotated1.shape[:2]
screen = cv2.resize(annotated1, (w//4, h//4), interpolation=cv2.INTER_AREA)
cv2.imshow("screen", screen)
cv2.waitKey(1)

check_img1 = cap_screen()
if ocr_check(check_img1, target="menu"):
    print("현재 화면: 메뉴앱 맞습니다")
else:
    print("현재 화면: 메뉴앱 아닙니다.")



img = cap_screen()
result = model.predict(source=img, conf=0.45, verbose=False, device=0)[0]
read(result)
run()
annotated2 = result.plot()
h, w = annotated2.shape[:2]
screen = cv2.resize(annotated2, (w//4, h//4), interpolation=cv2.INTER_AREA)
cv2.imshow("screen", screen)
cv2.waitKey(2)

check_img2 = cap_screen()
if ocr_check(check_img2, target="audio"):
    print("현재 화면: 오디오 맞습니다")
else:
    print("현재 화면: 오디오 아닙니다.")


img = cap_screen()
result = model2.predict(source=img, conf=0.45, verbose=False, device=0)[0]
read(result)
run()
annotated3 = result.plot()
h, w = annotated3.shape[:2]
screen = cv2.resize(annotated3, (w//4, h//4), interpolation=cv2.INTER_AREA)
cv2.imshow("screen", screen)
cv2.waitKey(2)

check_img3 = cap_screen()
if ocr_check(check_img3, target="home"):
    print("현재 화면: 홈 맞습니다")
else:
    print("현재 화면: 홈 아닙니다.")

cv2.waitKey(0)
cv2.destroyAllWindows()