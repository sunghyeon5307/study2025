# from ultralytics import YOLO
# import cv2, subprocess, numpy as np, time, os

# model = YOLO("best.pt")
# model2 = YOLO("cls_best.pt")

# file = "touch_log.tsv"

# # target = "home"  
# target = "menu"  
# # target = "audio"  

# def cap_screen():
#     res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
#     return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)

# img = cap_screen()
# result = model.predict(source=img, conf=0.45, verbose=False)[0]

# with open("touch_log.tsv", "w", encoding="utf-8") as f:
#     for i in result.boxes:
#         cls_id = int(i.cls[0])
#         cls = model.names[cls_id]
#         if cls != target:
#             continue  

#         x1, y1, x2, y2 = map(int, i.xyxy[0].tolist())

#         cx, cy = (x1 + x2)//2, (y1 + y2)//2
        
#         conf = float(i.conf[0])
#         print(f"{cls}: center=({cx},{cy}), conf={conf:.2f}")
#         f.write(f"{cls}\t{cx}\t{cy}\n")

# annotated = result.plot()
# h, w = annotated.shape[:2]
# screen = cv2.resize(annotated, (w//4, h//4), interpolation=cv2.INTER_AREA)

# with open(file, "r", encoding="utf-8") as f:
#     for i in f:
#         parts = i.strip().split()
#         _, x, y = parts

#         subprocess.run(["adb", "shell", "input", "tap", x, y])
#         time.sleep(5)

# if target=="audio" or target=="menu":
#     now_frame = cap_screen()
#     results = model2(now_frame, device=0, half=True)
#     r0 = results[0]
#     top_id = int(r0.probs.top1)
#     top_name = model.names[top_id]
#     if top_name == "audio":
#         print("분류된 화면: 오디오 화면")
#     if top_name == "menu":
#         print("분류된 화면: 마이 메뉴 화면")
# else:
#     os.remove("window_dump.xml")
#     subprocess.run(["adb", "shell", "uiautomator", "dump"])
#     subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "."])
#     with open("window_dump.xml", "r", encoding="utf-8") as f:
#         xml = f.read()

#     if "com.ivi.app.usermenu:id/tv_title" in xml:
#         print("분류된 화면: 메뉴 화면")
#     elif "com.ivi.app.cameraavm:id/tv_no_signal_1" in xml:
#         print("분류된 화면: 홈 화면")
#     else:
#         print("다른 화면")


# cv2.imshow("detection", screen)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


from ultralytics import YOLO
import cv2, subprocess, time, os, numpy as np

model = YOLO("cls_best.pt")

def cap_screen():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)


now_frame = cap_screen()
results = model(now_frame, device=0, half=True)
r0 = results[0]


xml_file = "window_dump.xml"
os.remove(xml_file)
subprocess.run(["adb", "shell", "uiautomator", "dump"])
subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "."])
with open("window_dump.xml", "r", encoding="utf-8") as f:
    xml = f.read()
if "사용자 메뉴" in xml:
    print("분류된 화면: 사용자 메뉴 화면")
elif "com.ivi.app.cameraavm:id/tv_no_signal_1" in xml:
    print("분류된 화면: 홈 화면")
elif "소모품 관리" in xml:
    print("분류된 화면: 장비 정보 화면")
elif "장비 설정" in xml:
    print("분류된 화면: 장비 설정 화면")
elif "작업자 어시스트" in xml:
    print("분류된 화면: 작업자 어시스트 화면")
elif "시스템 설정" in xml:
    print("분류된 화면: 시스템 설정 화면")
elif "사용자 관리" in xml:
    print("분류된 화면: 사용자 관리 화면")
else:
    print("다른 화면")

cv2.imshow("screen", now_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
