import subprocess
import cv2
import numpy as np
import easyocr

reader = easyocr.Reader(['en', 'ko'], gpu=True)

def capture():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)

def ocr_check():
    img = capture()
    result = reader.readtext(img)
    texts = [r[1] for r in result if isinstance(r[1], str) and r[1].strip()]
    c_text = len(texts)
    return texts, c_text

def ocr_save_keyword():
    messages = {
        "홈 화면": ["rpm", "영상 입력 신호가 없습니다."],
        "시스템 설정 화면": ["시스템 설정", "화면 설정", "날짜 및 시간 설정", "언어 설정", "단위 설정", "소프트웨어 업데이트", "추가기능 설치"],
        "오디오 화면": ["OFF", "BAND", "DAB", "MODE"],
        "오토 아이들 설정 화면": ["오토 아이들 설정", "오토 아이들 사용"],
        "장비 정보 화면": ["장비 정보", "모니터링", "소모품 관리", "경고 정보", "작업 리포트", "서비스 번호 설정"],
        "사용자 메뉴 화면": ["사용자 메뉴", "장비 정보", "장비 설정", "작업자 어시스트", "시스템 설정"],
        "마이 메뉴 화면": ["마이 메뉴", "소모품 관리", "오디오", "모니터링"],
        "작업자 어시스트 화면": ["작업자 어시스트", "스마트 AVM 설정"],
        "사용자 관리 화면": ["사용자 관리", "사용자 전환"],
        "장비 설정 화면": ["장비 설정", "비상 모드"]
    }
    page = None
    result=0
    texts, c_text = ocr_check()
    for keyword, keywords in messages.items():
        match_count = 0
        for kw in keywords:
            for text in texts:
                if kw in text:
                    match_count += 1
                    break

        total_count = len(keywords)

        accuracy = (match_count / total_count)
        
        if accuracy >= 0.7:
            page = keyword
            result  = accuracy
            ocr_print = f"ocr 분류된 화면: {keyword}, 정확도: {result:.2f}"
    return ocr_print, keyword, result