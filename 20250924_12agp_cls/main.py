from ultralytics import YOLO
import subprocess
import cv2
import numpy as np
import torch

model = YOLO("best2.pt")


def capture():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    img = cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)
    return img

now_frame=capture()
results = model(now_frame, device=0, half=True)
r0 = results[0]


top_id = int(r0.probs.top1)
top_name = model.names[top_id]

if top_name == "system_setting":
    print("분류된 화면: 시스템 설정 화면 입니다.")
if top_name == "audio":
    print("분류된 화면: 오디오 화면 입니다.")
if top_name == "auto":
    print("분류된 화면: 오토 아이들 설정 화면 입니다.")
if top_name == "device_information":
    print("분류된 화면: 장비 정보 화면 입니다.")
if top_name == "main":
    print("분류된 화면: 메인 화면 입니다.")
if top_name == "menu":
    print("분류된 화면: 사용자 메뉴 화면 입니다.")
if top_name == "mymenu":
    print("분류된 화면: 마이 메뉴 화면 입니다.")   

annotated = results[0].plot()
h, w = annotated.shape[:2]
screen = cv2.resize(annotated, (w//3, h//3), interpolation=cv2.INTER_AREA)

cv2.imshow("result", screen)
cv2.waitKey(0)
cv2.destroyAllWindows()

