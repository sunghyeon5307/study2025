# ocr_multilang_labels.py
from ultralytics import YOLO
import cv2, subprocess, numpy as np
import time, easyocr, re, os, unicodedata
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from functools import lru_cache

# ---------- 언어별 폰트 우선순위(있는 것부터 사용) ----------
FONT_CANDIDATES = {
    "ko": [
        r"C:\Windows\Fonts\malgun.ttf",
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ],
    "ja": [
        r"C:\Windows\Fonts\meiryo.ttc",
        r"C:\Windows\Fonts\YuGothM.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ],
    "ch_sim": [
        r"C:\Windows\Fonts\msyh.ttc",   # Microsoft YaHei
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ],
    "ch_tra": [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\mingliu.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ],
    "vi": [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ],
    # 라틴(영/불/포/이탈리아 등)
    "latin": [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ],
}
# 최종 글로벌 폴백(어떤 언어든 마지막 시도)
GLOBAL_FALLBACK = [
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]

def pick_font_path(lang: str):
    groups = []
    if lang in ("fr","pt","it","en"): groups.append("latin")
    groups.append(lang)
    for g in groups:
        for p in FONT_CANDIDATES.get(g, []):
            if os.path.exists(p):
                return p
    for p in GLOBAL_FALLBACK:
        if os.path.exists(p):
            return p
    return None

@lru_cache(maxsize=64)
def load_font(lang: str, size: int):
    path = pick_font_path(lang)
    try:
        if path: return ImageFont.truetype(path, size)
    except Exception:
        pass
    return ImageFont.load_default()

# ---------- EasyOCR Readers ----------
reader_ko      = easyocr.Reader(['ko','en'], gpu=True)           # ko는 en 병행
reader_ja      = easyocr.Reader(['ja'], gpu=True)
reader_en      = easyocr.Reader(['en'], gpu=True)
reader_pt      = easyocr.Reader(['pt'], gpu=True)
reader_it      = easyocr.Reader(['it'], gpu=True)
reader_ch_sim  = easyocr.Reader(['ch_sim','en'], gpu=True)
reader_ch_tra  = easyocr.Reader(['ch_tra','en'], gpu=True)
reader_fr      = easyocr.Reader(['fr'], gpu=True)
reader_vi      = easyocr.Reader(['vi'], gpu=True)

def draw_boxes(img, results_with_lang):
    """
    results_with_lang: list of (bbox, text, conf, lang)
    """
    vis = img.copy()
    # 1) 박스
    for bbox, _, _, _ in results_with_lang:
        pts = [(int(x), int(y)) for (x, y) in bbox]
        for j in range(4):
            cv2.line(vis, pts[j], pts[(j+1) % 4], (0, 255, 0), 2)

    # 2) 라벨
    vis_rgb = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)
    base = Image.fromarray(vis_rgb).convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    h, w = vis.shape[:2]
    base_size = max(24, int(min(w, h) * 0.04))

    for bbox, text, conf, lang in results_with_lang:
        label = unicodedata.normalize("NFC", f"{text} ({conf:.2f})")
        font = load_font(lang, base_size)

        xs = [p[0] for p in bbox]; ys = [p[1] for p in bbox]
        x0, y0 = int(min(xs)), int(min(ys))

        try:
            tb = draw.textbbox((0, 0), label, font=font)
            tw, th = tb[2] - tb[0], tb[3] - tb[1]
        except AttributeError:
            tw, th = draw.textsize(label, font=font)

        pad = 6
        x1 = x0
        y1 = max(0, y0 - th - pad*2)
        x2 = x1 + tw + pad*2
        y2 = y1 + th + pad*2

        draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 180))
        draw.text((x1 + pad, y1 + pad), label, font=font, fill=(0, 255, 0, 255))

    out = Image.alpha_composite(base, overlay).convert("RGB")
    return cv2.cvtColor(np.array(out), cv2.COLOR_RGB2BGR)

def ocr_check(img, show=True, save=True):
    conf = 0.3
    # 언어별 1패스 (중국어는 임계 완화)
    raw = {
        "ko":      reader_ko.readtext(img, detail=1, paragraph=False),
        "ja":      reader_ja.readtext(img, detail=1, paragraph=False),
        "ch_sim":  reader_ch_sim.readtext(img, detail=1, paragraph=False),
        "ch_tra":  reader_ch_tra.readtext(img, detail=1, paragraph=False),
        "fr":      reader_fr.readtext(img, detail=1, paragraph=False),
        "vi":      reader_vi.readtext(img, detail=1, paragraph=False),
        "pt":      reader_pt.readtext(img, detail=1, paragraph=False),
        "it":      reader_it.readtext(img, detail=1, paragraph=False),
    }
    raw_en = reader_en.readtext(img, detail=1, paragraph=False)

    # 스코어로 최고 언어 선택
    best_lang, best_results, best_score = None, [], -1
    for lang, results in raw.items():
        thr = 0.25 if lang.startswith("ch_") else conf
        valid = [r for r in results if r[2] >= thr]
        if not valid: continue
        avg_conf = sum(c for _,_,c in valid) / len(valid)
        score = len(valid) * avg_conf
        if score > best_score:
            best_lang, best_results, best_score = lang, valid, score

    # 영어는 높은 임계로 보조 병합
    add_en = [r for r in raw_en if r[2] >= 0.8]

    # 언어 태그를 붙여서 보관
    def tagify(rs, lang):
        return [(bbox, txt, cf, lang) for (bbox, txt, cf) in rs]

    all_results = tagify(best_results, best_lang) + tagify(add_en, "en")

    print(f"[{best_lang}] 인식된 텍스트:", [t for _, t, _, _ in all_results])

    if show or save:
        vis = draw_boxes(img, all_results)

    if show:
        h, w = vis.shape[:2]
        vis_small = cv2.resize(vis, (max(1, w//2), max(1, h//2)), interpolation=cv2.INTER_AREA)
        cv2.imshow("ocr", vis_small)
        cv2.waitKey(1)

    if save:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"ocr_result_{ts}.png"
        cv2.imwrite(fname, vis)
        print(f"[SAVE] {fname}")

    return all_results

def cap_screen():
    res = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    return cv2.imdecode(np.frombuffer(res.stdout, np.uint8), cv2.IMREAD_COLOR)

if __name__ == "__main__":
    img = cap_screen()
    if img is None:
        print("[ERR] ADB 캡처 실패")
    else:
        ocr_check(img, show=True, save=True)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
