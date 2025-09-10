from ultralytics import YOLO
import cv2, subprocess, numpy as np

model = YOLO("best.pt")

target = "youtube"  
# target = "phone"  

def cap_screen():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)

img = cap_screen()
result = model.predict(source=img, conf=0.45, verbose=False)[0]

with open("touch_log.tsv", "w", encoding="utf-8") as f:
    for i in result.boxes:
        cls_id = int(i.cls[0])
        cls = model.names[cls_id]
        if cls != target:
            continue  

        x1, y1, x2, y2 = map(int, i.xyxy[0].tolist())
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        conf = float(i.conf[0])
        print(f"{cls}: center=({cx},{cy}), conf={conf:.2f}")
        f.write(f"{cls}\t{cx}\t{cy}\n")

annotated = result.plot()
h, w = annotated.shape[:2]
screen = cv2.resize(annotated, (w//4, h//4), interpolation=cv2.INTER_AREA)

cv2.imshow("detection", screen)
cv2.waitKey(0)
cv2.destroyAllWindows()