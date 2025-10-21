# from ultralytics import YOLO
# import cv2, subprocess, time, os, numpy as np

# model = YOLO("cls_best.pt")

# def cap_screen():
#     res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
#     return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)

# xml_file = "window_dump.xml"

# try:
#     while True:
#         now_frame = cap_screen()
#         results = model(now_frame, device=0, half=True)
#         r0 = results[0]

#         subprocess.run(["adb", "shell", "uiautomator", "dump"], stdout=subprocess.DEVNULL)
#         subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "."], stdout=subprocess.DEVNULL)

#         with open(xml_file, "r", encoding="utf-8") as f:
#             xml = f.read()

#         if "사용자 메뉴" in xml:
#             print("분류된 화면: 사용자 메뉴 화면")
#         elif "com.ivi.app.cameraavm:id/tv_no_signal_1" in xml:
#             print("분류된 화면: 홈 화면")
#         elif "소모품 관리" in xml:
#             print("분류된 화면: 장비 정보 화면")
#         elif "장비 설정" in xml:
#             print("분류된 화면: 장비 설정 화면")
#         elif "작업자 어시스트" in xml:
#             print("분류된 화면: 작업자 어시스트 화면")
#         elif "시스템 설정" in xml:
#             print("분류된 화면: 시스템 설정 화면")
#         elif "사용자 관리" in xml:
#             print("분류된 화면: 사용자 관리 화면")
#         else:
#             print("다른 화면")

#         time.sleep(1)

# except KeyboardInterrupt:
#     print("실행 종료")


import subprocess, time, os

xml_file = "window_dump.xml"

try:
    while True:
        # UI Automator로 현재 화면 XML 덤프
        subprocess.run(["adb", "shell", "uiautomator", "dump"], stdout=subprocess.DEVNULL)
        subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "."], stdout=subprocess.DEVNULL)

        # XML 파일 읽기
        if os.path.exists(xml_file):
            with open(xml_file, "r", encoding="utf-8") as f:
                xml = f.read()

            # 화면 구분
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
        else:
            print("XML 파일이 존재하지 않습니다.")

        time.sleep(1)

except KeyboardInterrupt:
    print("실행 종료")
