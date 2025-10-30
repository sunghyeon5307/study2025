import subprocess
import cv2
import numpy as np
from cls import cls_save_keyword
import time
from datetime import datetime

file = "log.tsv"

def capture(save_path="capture.png"):
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    img = cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)
    cv2.imwrite(save_path, img)
    return save_path


def match_method(method):
    if method == "cls":
        cls_print, cls_keyword, _ = cls_save_keyword()
        return cls_keyword


def match_id(id, method):
    curr_keyword = match_method(method)
    id_norm = (id or "").strip()
    curr_norm = (curr_keyword or "").strip()

    if id_norm and id_norm == curr_norm:
        return f"(OK) ID 매칭 성공: {id_norm}", None
    else:
        ts_ms = int(datetime.now().timestamp() * 1000)
        fname = f"capture/ng_img_{ts_ms}.png"
        path = capture(fname)
        return f"(NG) ID 매칭 실패: 인식해야하는ID={id_norm}, 인식된ID={curr_norm}", path


def start_touch():
    id = None
    method = None

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("X="):
                x = line.split(",")[0].split("=")[1]
                y = line.split(",")[1].split("=")[1]
                subprocess.run(["adb", "shell", "input", "tap", x, y])
                time.sleep(1)  
            elif line.startswith("ID:"):
                id = line.split(":")[1]
            elif line.startswith("METHOD:"):
                method = line.split(":")[1]
                result, path = match_id(id, method)

                yield (result, path)

