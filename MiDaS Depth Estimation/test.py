from realesrgan import RealESRGAN
from PIL import Image
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = RealESRGAN(device, scale=4)
model.load_weights('weights/RealESRGAN_x4plus.pth')  # weights 폴더에 다운로드
img = Image.open(r"C:\study\MiDaS Depth Estimation\test.png").convert("RGB")

sr_image = model.predict(img)
sr_image.save("superres_result.png")
print("✅ 초해상도 이미지 저장 완료!")
