import subprocess
import os


def ui_dump_keyword():
    with open("window_dump.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    if "사용자 메뉴" in xml:
        return "사용자 메뉴 화면", 1.00
    elif "com.ivi.app.cameraavm:id/tv_no_signal_1" in xml:
        return "홈 화면", 0.00
    elif "소모품 관리" in xml:
        return "장비 정보 화면", 1.00
    elif "장비 설정" in xml:
        return "장비 설정 화면", 1.00
    elif "작업자 어시스트" in xml:
        return "작업자 어시스트 화면", 1.00
    elif "시스템 설정" in xml:
        return "시스템 설정 화면", 1.00
    elif "사용자 관리" in xml:
        return "사용자 관리 화면", 1.00
    elif "오토 아이들 설정" in xml:
        return "오토 아이들 설정 화면", 1.00
    else:
        return "Unknown"

def xml_bring():
    xml_file = "window_dump.xml"
    if os.path.exists(xml_file):
        os.remove(xml_file)
    else:
        pass
    subprocess.run(["adb", "shell", "uiautomator", "dump"])
    subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "."])
    with open("window_dump.xml", "r", encoding="utf-8") as f:
        xml = f.read()

def dump_save_keyword():
    xml_bring()
    keyword, result = ui_dump_keyword()
    print(f"dump 분류된 화면: {keyword}, 정확도: {result}")
    return keyword, result