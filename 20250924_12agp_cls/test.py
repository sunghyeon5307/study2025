from ultralytics import YOLO
import subprocess, cv2, numpy as np, torch, threading, queue

torch.backends.cudnn.benchmark = True
model = YOLO("best.pt").to("cuda")
model.fuse()

def capture_one():
    r = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    img = cv2.imdecode(np.frombuffer(r.stdout, np.uint8), cv2.IMREAD_COLOR)
    return img

q = queue.Queue(maxsize=2)
stop = False

def consumer():
    last_text = None  # 이전에 출력한 문구 저장

    with torch.inference_mode():
        while not stop:
            if q.empty():
                continue

            img = q.get()
            res = model(img, device=0, half=True, verbose=False, imgsz=64)[0]
            top_name = model.names[int(res.probs.top1)]

            if top_name == "system_setting":
                text = "분류된 화면: 시스템 설정 화면 입니다."
            elif top_name == "audio":
                text = "분류된 화면: 오디오 화면 입니다."
            elif top_name == "auto":
                text = "분류된 화면: 오토 아이들 설정 화면 입니다."
            elif top_name == "device_information":
                text = "분류된 화면: 장비 정보 화면 입니다."
            elif top_name == "main":
                text = "분류된 화면: 메인 화면 입니다."
            elif top_name == "menu":
                text = "분류된 화면: 사용자 메뉴 화면 입니다."
            elif top_name == "mymenu":
                text = "분류된 화면: 마이 메뉴 화면 입니다."
            elif top_name == "operator assist":
                text = "분류된 화면: 작업자 어시스트 화면 입니다."
            elif top_name == "user_management":
                text = "분류된 화면: 사용자 관리 화면 입니다."
            elif top_name == "device_setting":
                text = "분류된 화면: 정비 설정 화면 입니다."
            else:
                text = f"분류된 화면: {top_name}"

            if text != last_text:
                print(text)
                last_text = text

            annotated = res.plot()
            h, w = annotated.shape[:2]
            screen = cv2.resize(annotated, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
            cv2.imshow("Device Screen", screen)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            q.task_done()

def producer():
    global stop
    while not stop:
        img = capture_one()
        if img is not None and not q.full():
            q.put(img)

tp = threading.Thread(target=producer, daemon=True)
tc = threading.Thread(target=consumer, daemon=True)
tp.start(); tc.start()

try:
    tp.join(); tc.join()
finally:
    stop = True
    cv2.destroyAllWindows()
