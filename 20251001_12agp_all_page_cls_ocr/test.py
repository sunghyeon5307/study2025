# # -*- coding: utf-8 -*-
# from ultralytics import YOLO
# import subprocess, cv2, numpy as np, torch, threading, queue, time, sys
# import easyocr

# # 콘솔 UTF-8 보장(가능한 경우)
# try:
#     sys.stdout.reconfigure(encoding='utf-8')
# except Exception:
#     pass

# #############################################
# # YOLO 분류 모델
# #############################################
# torch.backends.cudnn.benchmark = True
# model = YOLO("best.pt").to("cuda")
# model.fuse()

# #############################################
# # EasyOCR: ko + en 전용
# #############################################
# reader = easyocr.Reader(["ko", "en"], gpu=True)

# #############################################
# # ADB 스크린샷 캡처 (재시도 포함)
# #############################################
# PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

# def capture_one(max_retries=5, backoff=0.05, timeout_sec=5):
#     for attempt in range(1, max_retries + 1):
#         try:
#             r = subprocess.run(
#                 ["adb", "exec-out", "screencap", "-p"],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 timeout=timeout_sec
#             )
#         except subprocess.TimeoutExpired:
#             if attempt == max_retries:
#                 return None
#             time.sleep(backoff * attempt)
#             continue

#         buf = r.stdout
#         if not buf or len(buf) < 100 or not buf.startswith(PNG_MAGIC):
#             if attempt == max_retries:
#                 return None
#             time.sleep(backoff * attempt)
#             continue

#         img = cv2.imdecode(np.frombuffer(buf, np.uint8), cv2.IMREAD_COLOR)
#         if img is None or img.size == 0:
#             if attempt == max_retries:
#                 return None
#             time.sleep(backoff * attempt)
#             continue

#         return img
#     return None

# #############################################
# # OCR 전처리 (업스케일 + CLAHE)  ※ 스케일 반환
# #############################################
# def preprocess_for_ocr(img_bgr):
#     if img_bgr is None:
#         return None, 1.0
#     h, w = img_bgr.shape[:2]
#     scale = 1.5 if max(h, w) < 1600 else 1.0
#     if scale != 1.0:
#         img_bgr = cv2.resize(img_bgr, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_CUBIC)

#     lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
#     l, a, b = cv2.split(lab)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#     l2 = clahe.apply(l)
#     img_eq = cv2.cvtColor(cv2.merge((l2, a, b)), cv2.COLOR_LAB2BGR)
#     return img_eq, scale

# #############################################
# # ko+en OCR 실행 (좌표를 원본 스케일로 복원)
# #############################################
# def run_ocr(img_bgr, conf_floor=0.23):
#     img_pre, scale = preprocess_for_ocr(img_bgr)
#     if img_pre is None:
#         return []
#     results = reader.readtext(img_pre, detail=1, paragraph=False)

#     out = []
#     inv = (1.0/scale) if scale != 1.0 else 1.0
#     for (bbox, text, conf) in results:
#         if not text or not text.strip() or conf < conf_floor:
#             continue
#         if inv != 1.0:
#             bbox = [(float(x)*inv, float(y)*inv) for (x, y) in bbox]
#         out.append((bbox, text.strip(), float(conf)))

#     out.sort(key=lambda x: x[2], reverse=True)
#     return out

# #############################################
# # OCR 오버레이 (박스만 표시, 텍스트 라벨 없음)
# #############################################
# def draw_ocr(overlay_img, ocr_results, conf_thresh=0.25):
#     vis = overlay_img.copy()
#     for (bbox, _text, conf) in ocr_results:
#         if conf < conf_thresh:
#             continue
#         pts = [(int(round(x)), int(round(y))) for (x, y) in bbox]
#         for j in range(4):
#             p1, p2 = pts[j], pts[(j+1) % 4]
#             cv2.line(vis, p1, p2, (0, 255, 0), 2)
#     return vis

# #############################################
# # 분류 한글 라벨
# #############################################
# def label_kor(top_name: str) -> str:
#     mapping = {
#         "system_setting": "분류된 화면: 시스템 설정 화면 입니다.",
#         "audio": "분류된 화면: 오디오 화면 입니다.",
#         "auto": "분류된 화면: 오토 아이들 설정 화면 입니다.",
#         "device_information": "분류된 화면: 장비 정보 화면 입니다.",
#         "main": "분류된 화면: 메인 화면 입니다.",
#         "menu": "분류된 화면: 사용자 메뉴 화면 입니다.",
#         "mymenu": "분류된 화면: 마이 메뉴 화면 입니다.",
#         "operator assist": "분류된 화면: 작업자 어시스트 화면 입니다.",
#         "user_management": "분류된 화면: 사용자 관리 화면 입니다.",
#         "device_setting": "분류된 화면: 정비 설정 화면 입니다.",
#     }
#     return mapping.get(top_name, f"분류된 화면: {top_name}")

# #############################################
# # 유틸: 한글 포함 여부
# #############################################
# def contains_hangul(s: str) -> bool:
#     return any('\uac00' <= ch <= '\ud7a3' for ch in s)

# #############################################
# # 쓰레딩/큐
# #############################################
# q = queue.Queue(maxsize=2)
# stop = False

# def consumer():
#     global stop
#     last_cls_text = None

#     # 콘솔 출력 제어
#     last_ocr_blob = None        # 전체 최초 출력 여부
#     last_hangul_blob = None     # 한글 최초 출력 여부

#     # OCR 호출 주기 & 캐시(깜빡임 방지)
#     ocr_last_time = 0.0
#     OCR_MIN_INTERVAL = 0.35
#     ocr_cache = []
#     ocr_cache_time = 0.0
#     OCR_CACHE_TTL = 3.0

#     with torch.inference_mode():
#         while not stop:
#             if q.empty():
#                 time.sleep(0.001)
#                 continue

#             img = q.get()
#             if img is None:
#                 q.task_done()
#                 continue

#             # 1) 분류
#             res = model(img, device=0, half=True, verbose=False, imgsz=64)[0]
#             top_name = model.names[int(res.probs.top1)]
#             cls_text = label_kor(top_name)
#             if cls_text != last_cls_text:
#                 print(cls_text)
#                 last_cls_text = cls_text

#             # 2) OCR (주기 제한 + 캐시)
#             now = time.time()
#             if (now - ocr_last_time) >= OCR_MIN_INTERVAL:
#                 try:
#                     results = run_ocr(img, conf_floor=0.7)
#                     if results:
#                         # 상위 12줄까지 합쳐서 blob 생성
#                         top_lines = [t for (_, t, _) in results[:12]]
#                         blob = " | ".join(top_lines)

#                         # (1) 프로그램 전체에서 최초 한 번 출력
#                         if last_ocr_blob is None:
#                             print(f"인식된 텍스트: {blob}")
#                             last_ocr_blob = blob

#                         # 캐시 저장(시각화용)
#                         ocr_cache = results
#                         ocr_cache_time = now
#                 except Exception as e:
#                     print(f"[OCR ERROR] {e}", file=sys.stderr)
#                 finally:
#                     ocr_last_time = now

#             # 3) 시각화(분류 + OCR 캐시)
#             annotated = res.plot()
#             if ocr_cache and (now - ocr_cache_time) <= OCR_CACHE_TTL:
#                 annotated = draw_ocr(annotated, ocr_cache, conf_thresh=0.25)
#             else:
#                 ocr_cache = []

#             # 보기 좋게 축소
#             h, w = annotated.shape[:2]
#             screen = cv2.resize(annotated, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
#             cv2.imshow("Device Screen", screen)

#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 stop = True
#                 q.task_done()
#                 break

#             q.task_done()

# def producer():
#     global stop
#     while not stop:
#         img = capture_one()
#         if img is not None:
#             if q.full():
#                 try:
#                     _ = q.get_nowait(); q.task_done()
#                 except queue.Empty:
#                     pass
#             q.put(img)
#         else:
#             time.sleep(0.01)


# tp = threading.Thread(target=producer, daemon=True)
# tc = threading.Thread(target=consumer, daemon=True)
# tp.start(); tc.start()

# try:
#     tp.join(); tc.join()
# finally:
#     stop = True
#     cv2.destroyAllWindows()


# -*- coding: utf-8 -*-
from ultralytics import YOLO
import subprocess, cv2, numpy as np, torch, threading, queue, time, sys
import easyocr
import re

# 콘솔 UTF-8 보장(가능한 경우)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

#############################################
# 화면별 키워드 (네가 제공한 버전)
#############################################
SCREEN_KEYWORDS = {
    "main": ["rpm", "영상 입력 신호가 없습니다."],
    "system_setting": ["시스템 설정", "화면 설정", "언어 설정", "날짜 및 시간 설정"],
    "audio": ["OFF", "MODE"],
    "auto": ["오토 아이들 설정", "오토 아이들 사용"],
    "device_information": ["장비 정보", "소모품 관리", "경고 정보", "작업 리포트"],
    "menu": ["사용자 메뉴", "장비 정보", "장비 설정", "작업자 어시스트", "시스템 설정"],
    "mymenu": ["마이 메뉴", "오디오"],
    "operator assist": ["작업자 어시스트", "스마트 AVM 설정"],
    "user_management": ["사용자 관리", "사용자 전환"],
    "device_setting": ["장비 설정", "비상 모드"],
}

SCREEN_DISPLAY = {
    "system_setting": "시스템 설정",
    "audio": "오디오",
    "auto": "오토 아이들 설정",
    "device_information": "장비 정보",
    "main": "메인",
    "menu": "사용자 메뉴",
    "mymenu": "마이 메뉴",
    "operator assist": "작업자 어시스트",
    "user_management": "사용자 관리",
    "device_setting": "정비 설정",
}



torch.backends.cudnn.benchmark = True
model = YOLO("best.pt").to("cuda")
model.fuse()

#############################################
# EasyOCR: ko + en 전용
#############################################
reader = easyocr.Reader(["ko", "en"], gpu=True)

#############################################
# ADB 스크린샷 (재시도 포함)
#############################################
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
def capture_one(max_retries=5, backoff=0.05, timeout_sec=5):
    for attempt in range(1, max_retries + 1):
        try:
            r = subprocess.run(
                ["adb", "exec-out", "screencap", "-p"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_sec
            )
        except subprocess.TimeoutExpired:
            if attempt == max_retries:
                return None
            time.sleep(backoff * attempt); continue

        buf = r.stdout
        if not buf or len(buf) < 100 or not buf.startswith(PNG_MAGIC):
            if attempt == max_retries:
                return None
            time.sleep(backoff * attempt); continue

        img = cv2.imdecode(np.frombuffer(buf, np.uint8), cv2.IMREAD_COLOR)
        if img is None or img.size == 0:
            if attempt == max_retries:
                return None
            time.sleep(backoff * attempt); continue
        return img
    return None

#############################################
# OCR 전처리 (업스케일 + CLAHE)  ※ 스케일 반환
#############################################
def preprocess_for_ocr(img_bgr):
    if img_bgr is None:
        return None, 1.0
    h, w = img_bgr.shape[:2]
    scale = 1.5 if max(h, w) < 1600 else 1.0
    if scale != 1.0:
        img_bgr = cv2.resize(img_bgr, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_CUBIC)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l2 = clahe.apply(l)
    img_eq = cv2.cvtColor(cv2.merge((l2, a, b)), cv2.COLOR_LAB2BGR)
    return img_eq, scale

#############################################
# ko+en OCR 실행 (좌표 원본 스케일로 복원)
#############################################
def run_ocr(img_bgr, conf_floor=0.7):
    img_pre, scale = preprocess_for_ocr(img_bgr)
    if img_pre is None:
        return []
    results = reader.readtext(img_pre, detail=1, paragraph=False)

    out = []
    inv = (1.0/scale) if scale != 1.0 else 1.0
    for (bbox, text, conf) in results:
        if not text or not text.strip() or conf < conf_floor:
            continue
        if inv != 1.0:
            bbox = [(float(x)*inv, float(y)*inv) for (x, y) in bbox]
        out.append((bbox, text.strip(), float(conf)))
    out.sort(key=lambda x: x[2], reverse=True)
    return out

#############################################
# OCR 오버레이 (박스만)
#############################################
def draw_ocr(overlay_img, ocr_results, conf_thresh=0.25):
    vis = overlay_img.copy()
    for (bbox, _text, conf) in ocr_results:
        if conf < conf_thresh:
            continue
        pts = [(int(round(x)), int(round(y))) for (x, y) in bbox]
        for j in range(4):
            p1, p2 = pts[j], pts[(j+1) % 4]
            cv2.line(vis, p1, p2, (0, 255, 0), 2)
    return vis

#############################################
# 분류 라벨 (로그용)
#############################################
def label_kor(top_name: str) -> str:
    mapping = {
        "system_setting": "분류된 화면: 시스템 설정 화면 입니다.",
        "audio": "분류된 화면: 오디오 화면 입니다.",
        "auto": "분류된 화면: 오토 아이들 설정 화면 입니다.",
        "device_information": "분류된 화면: 장비 정보 화면 입니다.",
        "main": "분류된 화면: 메인 화면 입니다.",
        "menu": "분류된 화면: 사용자 메뉴 화면 입니다.",
        "mymenu": "분류된 화면: 마이 메뉴 화면 입니다.",
        "operator assist": "분류된 화면: 작업자 어시스트 화면 입니다.",
        "user_management": "분류된 화면: 사용자 관리 화면 입니다.",
        "device_setting": "분류된 화면: 정비 설정 화면 입니다.",
    }
    return mapping.get(top_name, f"분류된 화면: {top_name}")

#############################################
# 텍스트 정규화 & 키워드 매칭 (공백/구두점 무시)
#############################################
_PUNCT_RGX = re.compile(r"[^\w\s가-힣]+", flags=re.UNICODE)

def normalize_text(s: str) -> str:
    # 1) 구두점 제거  2) 연속 공백 1개로  3) 소문자/대소문자 무시(casefold)
    s = _PUNCT_RGX.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.casefold()

def all_keywords_matched(screen_key: str, all_text: str) -> bool:
    req = SCREEN_KEYWORDS.get(screen_key, [])
    if not req:
        return False
    tgt = normalize_text(all_text)
    tgt_nospace = tgt.replace(" ", "")
    for kw in req:
        k = normalize_text(kw)
        if k not in tgt and k.replace(" ", "") not in tgt_nospace:
            return False
    return True

#############################################
# 쓰레딩/큐
#############################################
q = queue.Queue(maxsize=2)
stop = False

def consumer():
    global stop
    last_cls_text = None

    # 화면별 OCR 전문을 한 번씩만 출력
    printed_blob_once = set()
    last_hard_confirmed = None

    # OCR 스로틀 & 캐시
    ocr_last_time = 0.0
    OCR_MIN_INTERVAL = 0.35
    ocr_cache = []
    ocr_cache_time = 0.0
    OCR_CACHE_TTL = 3.0

    with torch.inference_mode():
        while not stop:
            if q.empty():
                time.sleep(0.001); continue

            img = q.get()
            if img is None:
                q.task_done(); continue

            # 1) 분류
            res = model(img, device=0, half=True, verbose=False, imgsz=64)[0]
            top_name = model.names[int(res.probs.top1)]
            cls_text = label_kor(top_name)
            if cls_text != last_cls_text:
                print(cls_text)
                last_cls_text = cls_text

            # 2) OCR
            now = time.time()
            if (now - ocr_last_time) >= OCR_MIN_INTERVAL:
                try:
                    results = run_ocr(img, conf_floor=0.7)
                    if results:
                        # OCR 전문 만들기(최대 80개 라인)
                        all_lines = [t for (_, t, _) in results[:80]]
                        blob = " | ".join(all_lines)

                        # 현재 화면에 대해 OCR 전문을 아직 안 찍었으면 한 번 출력
                        if top_name not in printed_blob_once:
                            print(f"인식된 텍스트: {blob}")
                            printed_blob_once.add(top_name)

                        # 키워드 매칭으로 화면 확정(각 화면 최초 한 번)
                        if all_keywords_matched(top_name, " ".join(all_lines)):
                            if last_hard_confirmed != top_name:
                                disp = SCREEN_DISPLAY.get(top_name, top_name)
                                print(f"결과: {disp} 화면이 맞습니다.")
                                last_hard_confirmed = top_name

                        # 캐시 저장(박스 오버레이용)
                        ocr_cache = results
                        ocr_cache_time = now
                except Exception as e:
                    print(f"[OCR ERROR] {e}", file=sys.stderr)
                finally:
                    ocr_last_time = now

            # 3) 시각화
            annotated = res.plot()
            if ocr_cache and (now - ocr_cache_time) <= OCR_CACHE_TTL:
                annotated = draw_ocr(annotated, ocr_cache, conf_thresh=0.25)
            else:
                ocr_cache = []

            h, w = annotated.shape[:2]
            screen = cv2.resize(annotated, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
            cv2.imshow("Device Screen", screen)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                stop = True
                q.task_done()
                break

            q.task_done()

def producer():
    global stop
    while not stop:
        img = capture_one()
        if img is not None:
            if q.full():
                try:
                    _ = q.get_nowait(); q.task_done()
                except queue.Empty:
                    pass
            q.put(img)
        else:
            time.sleep(0.01)

tp = threading.Thread(target=producer, daemon=True)
tc = threading.Thread(target=consumer, daemon=True)
tp.start(); tc.start()

try:
    tp.join(); tc.join()
finally:
    stop = True
    cv2.destroyAllWindows()
