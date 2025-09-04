import ultralytics

ultralytics.checks()

from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO('yolov8s.pt')

    print(type(model.names), len(model.names))
    print(model.names)

    model.train(
        data=r'C:\Users\sungh\OneDrive\바탕 화면\study\20250901\roboflow\data.yaml',
        epochs=100,
        imgsz=640,            
        batch=16,              
        patience=20, 
        device='cuda'
    )
