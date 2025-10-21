from ultralytics import YOLO
import cv2, subprocess, time, os, numpy as np
import xml.etree.ElementTree as ET

label_kr = {
    "main": "홈 화면",
    "menu": "사용자 메뉴 화면",
    "device_information": "장비 정보 화면",
    "device_setting": "장비 설정 화면",
    "operator assist": "작업자 어시스트 화면",
    "system_setting": "시스템 설정 화면",
    "user_management": "사용자 관리 화면",
    "mymenu": "마이 메뉴 화면",
    "audio": "오디오 화면",
    "auto": "오토 아이들 설정 화면"
}


model = YOLO("cls_best.pt")

keyword_dict = {
    "홈 화면": ["영상 입력 신호가 없습니다."],
    "사용자 메뉴 화면": ["장비 정보", "장비 설정", "작업자 어시스트", "시스템 설정", "사용자 관리"],
    "장비 정보 화면": ["모니터링", "소모품 관리", "경고 정보", "작업 리포트", "서비스 번호 설정"],
    "장비 설정 화면": ["장비 설정", "오토 아이들 설정", "비상 모드"],
    "작업자 어시스트 화면": ["작업자 어시스트", "스마트 AVM 설정"],
    "시스템 설정 화면": ["시스템 설정", "화면 설정", "날짜 및 시간 설정", "언어 설정", "단위 설정", "소프트웨어 업데이트", "추가기능 설치"],
    "사용자 관리 화면": ["사용자 관리", "사용자 전환"],
    "오토 아이들 설정 화면": ["오토 아이들 설정", "오토 아이들 사용"]
}

def yolo_predict(frame):
    results = model(frame)
    pred_name = results[0].names[int(results[0].probs.top1)]
    conf = float(results[0].probs.top1conf)
    pred_name = label_kr.get(pred_name, pred_name)
    return pred_name, conf

def cap_screen():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    img = cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)
    return img

def dump_ui_xml():
    subprocess.run(["adb", "shell", "uiautomator", "dump", "/sdcard/window_dump.xml"])
    subprocess.run(["adb", "pull", "/sdcard/window_dump.xml", "."])

def xml_keyword(xml_path, keyword_dict):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    text_nodes = [node.attrib.get("text", "") for node in root.iter() if "text" in node.attrib]

    score_dict = {screen: 0 for screen in keyword_dict}
    for screen, keywords in keyword_dict.items():
        for kw in keywords:
            score_dict[screen] += sum(kw in t for t in text_nodes)

    best_match = max(score_dict, key=score_dict.get)
    return best_match, score_dict[best_match]

def fuse_results(yolo_result, xml_result, yolo_conf, xml_score, threshold=0.7):
    if yolo_result == xml_result:
        return yolo_result 
    
    if yolo_conf > threshold:
        return yolo_result
    else:
        return xml_result

def detect_screen():
    frame = cap_screen()
    yolo_name, yolo_conf = yolo_predict(frame)

    dump_ui_xml()
    xml_name, xml_score = xml_keyword("window_dump.xml", keyword_dict)

    final_screen = fuse_results(yolo_name, xml_name, yolo_conf, xml_score)
    print(f"[YOLO] {yolo_name} ({yolo_conf:.2f}) | [XML] {xml_name} ({xml_score}) → [최종 판별 화면] {final_screen}")

if __name__ == "__main__":
    while True:
        detect_screen()
        time.sleep(3)  
