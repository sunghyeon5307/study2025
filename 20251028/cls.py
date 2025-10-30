from ultralytics import YOLO
import subprocess
import cv2
import numpy as np

model = r"C:\study\20251015\best.pt"
model = YOLO(model).to("cuda")


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

def cls_save_keyword():
    top_id, top_name,result = classify()
    messages = {
        "system_setting": "시스템 설정 화면",
        "audio": "오디오 화면",
        "auto": "오토 아이들 설정 화면",
        "device_information": "장비 정보 화면",
        "main": "홈 화면",
        "menu": "사용자 메뉴 화면",
        "mymenu": "마이 메뉴 화면",
        "device_setting": "장비 설정 화면",
        "operator assist": "작업자 어시스트 화면",
        "user_management": "사용자 관리 화면",
    }
    conf = float(result[0].probs.top1conf)
    if top_name in messages:
        cls_print = f"cls 분류된 화면: {messages[top_name]}, 정확도: {conf:.2f}"
    return cls_print, messages[top_name], conf