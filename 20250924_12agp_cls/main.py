from ultralytics import YOLO
import subprocess
import cv2
import numpy as np

model = YOLO("best.pt")


def capture():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    img = cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)
    return img


now_frame=capture()
result = model(now_frame, device=0, half=True)

annotated = result[0].plot()
h, w = annotated.shape[:2]
screen = cv2.resize(annotated, (w//3, h//3), interpolation=cv2.INTER_AREA)

cv2.imshow("result", screen)
cv2.waitKey(0)
cv2.destroyAllWindows()