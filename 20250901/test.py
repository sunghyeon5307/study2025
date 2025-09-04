import matplotlib.pyplot as plt
from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")  

results = model.predict(source="/content/Aquarium_Data/test/images")

for i, res in range(30):
    img = res.plot()
    plt.figure(figsize=(8, 8))
    plt.imshow(img)
    plt.axis("off")
    plt.title(f"Test Image {i+1}")
    plt.show()