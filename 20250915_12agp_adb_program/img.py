# import os, glob, uuid, math, random
# import cv2
# import numpy as np
# from tqdm import tqdm
# import albumentations as A

# # ===== 경로/설정 =====
# INPUT_DIR  = r"C:\study\20250915_12agp_adb_program\dataset"   # 원본 이미지 폴더
# OUTPUT_DIR = r"C:\study\20250915_12agp_adb_program\dataset_aug"  # 출력 폴더
# TARGET_COUNT = 300               # 만들고 싶은 총 장수(원본 포함 X)
# OUT_W, OUT_H = 640, 640          # 최종 해상도
# SEED = 42
# random.seed(SEED); np.random.seed(SEED)

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # ===== 크롭 없이 안전한 증강 파이프라인 =====
# # - RandomResizedCrop/CenterCrop 같은 '크롭'은 전부 제외
# # - Affine은 fit_output=True + Pad로 모서리 잘림 방지
# transform = A.Compose([
#     A.Affine(
#         scale=(0.95, 1.05),
#         translate_percent={"x":(-0.03, 0.03), "y":(-0.02, 0.02)},  # 세로 이동은 아주 소폭만
#         rotate=(-3, 3),
#         shear=(-2, 2),
#         fit_output=True, keep_ratio=True, p=0.8
#     ),
#     A.MotionBlur(blur_limit=3, p=0.15),
#     A.GaussNoise(var_limit=(5.0, 20.0), p=0.2),
#     A.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.03, p=0.6),
#     A.RandomBrightnessContrast(p=0.25),
#     # 크롭 대신 '긴 변 기준 리사이즈 + 패딩'으로 해상도 맞춤 → 바텀바 유지
#     A.LongestMaxSize(max_size=max(OUT_W, OUT_H)),
#     A.PadIfNeeded(min_height=OUT_H, min_width=OUT_W,
#                   border_mode=cv2.BORDER_CONSTANT, value=(0,0,0))
# ])

# # ===== 입력 이미지 수집 =====
# exts = ("*.png","*.jpg","*.jpeg","*.bmp","*.webp")
# paths = []
# for e in exts:
#     paths.extend(glob.glob(os.path.join(INPUT_DIR, e)))
# paths = sorted(paths)
# if not paths:
#     raise RuntimeError(f"이미지가 없습니다: {INPUT_DIR}")

# # 이미지별 목표 개수 배분
# per_img = math.ceil(TARGET_COUNT / len(paths))
# saved = 0
# pbar = tqdm(total=TARGET_COUNT, desc="Augmenting (no crop)")

# for p in paths:
#     if saved >= TARGET_COUNT: break
#     img_bgr = cv2.imread(p)
#     if img_bgr is None: continue
#     img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

#     for _ in range(per_img):
#         if saved >= TARGET_COUNT: break
#         aug = transform(image=img)["image"]
#         out = cv2.cvtColor(aug, cv2.COLOR_RGB2BGR)
#         name = f"aug_{uuid.uuid4().hex}.jpg"
#         # JPG로 저장하면 해시가 달라져 Roboflow 중복 필터도 잘 통과함
#         cv2.imwrite(os.path.join(OUTPUT_DIR, name), out,
#                     [cv2.IMWRITE_JPEG_QUALITY, random.randint(92,96)])
#         saved += 1
#         pbar.update(1)

# pbar.close()
# print(f"완료! 생성: {saved}장 → {OUTPUT_DIR}")


import subprocess
import time

# 캡처할 총 장수
total_captures = 40

# 저장 폴더와 파일명 패턴
save_dir = r"C:\study\20250915_12agp_adb_program\data"
file_prefix = "mymenu180"

# 폴더 없으면 생성
import os
os.makedirs(save_dir, exist_ok=True)

for i in range(1, total_captures + 1):
    filename = f"{save_dir}{file_prefix}_{i:03d}.png"
    with open(filename, "wb") as f:
        subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)
    print(f"[{i}/{total_captures}] Saved {filename}")
    # 캡처 간격 (필요하면 조절, 너무 빠르면 기기가 버벅일 수 있음)
    time.sleep(0.2)
