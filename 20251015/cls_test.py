import cv2
from ultralytics import YOLO
import subprocess, numpy as np, time

model = YOLO("best.pt").to("cuda")

def capture():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)

def classify():
    img = capture()
    results = model(img, device=0)
    r = results[0]
    top_id = int(r.probs.top1)
    top_name = model.names[top_id]
    return top_id, top_name, results

if __name__ == "__main__":
    while True:
        classify()
        time.sleep(1)
