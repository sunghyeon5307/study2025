import subprocess
import time, cv2
import numpy as np
from cls_ocr import cls_save_keyword, ocr_save_keyword

file = "log.tsv"

def capture():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)

def match_method(method):
    if method == "cls":
        cls_print, cls_keyword, _ = cls_save_keyword()
        return cls_keyword
    else:
        ocr_print, ocr_keyword, _ = ocr_save_keyword()
        return ocr_keyword

def match_id(id, method):
    curr_keyword = match_method(method)
    if id == curr_keyword:
        return f"(OK) ID 매칭 성공: {id}"
    else:
        capture()
        return f"(NG) ID 매칭 실패: {id}", print(subprocess.run(["adb", "shell", "grep", "-E", "MemTotal|MemAvailable|SwapTotal|SwapFree", "/proc/meminfo"]))


def start_touch():
    results = []
    id = None
    method = None
    
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("X="):
                x = line.split(",")[0].split("=")[1]
                y = line.split(",")[1].split("=")[1]
                subprocess.run(["adb", "shell", "input", "tap", x, y])
            if line.startswith("ID:"):
                id = line.split(":")[1]
            if line.startswith("METHOD:"):
                method = line.split(":")[1]
                match_method(method)    
                result = match_id(id, method)
                results.append(result)
    return results