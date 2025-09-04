from ultralytics import YOLO

model = YOLO("/root/.cache/kagglehub/datasets/lakshaytyagi01/fruit-detection/runs/detect/train/weights/best.pt")

metrics = model.val(data="/root/.cache/kagglehub/datasets/lakshaytyagi01/fruit-detection/versions/1/Fruits-detection/data.yaml", split="val")

print("mAP50-95:", metrics.box.map)
print("mAP50:", metrics.box.map50)
print("Precision:", metrics.box.mp)
print("Recall:", metrics.box.mr)