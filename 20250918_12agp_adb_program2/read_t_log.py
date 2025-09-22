from ultralytics import YOLO
import cv2, subprocess, numpy as np
import time

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

img = cap_screen()
result = model.predict(source=img, conf=0.45, verbose=False)[0]
read(result)
run()    
annotated1 = result.plot()
h, w = annotated1.shape[:2]
screen1 = cv2.resize(annotated1, (w//4, h//4), interpolation=cv2.INTER_AREA)


img2 = cap_screen()
result = model.predict(source=img2, conf=0.45, verbose=False)[0]
read(result)
run()
annotated2 = result.plot()
h, w = annotated2.shape[:2]
screen2 = cv2.resize(annotated2, (w//4, h//4), interpolation=cv2.INTER_AREA)

cv2.imshow("music", screen1)
cv2.imshow("home", screen2)
cv2.waitKey(0)
cv2.destroyAllWindows()