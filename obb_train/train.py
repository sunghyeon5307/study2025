from ultralytics import YOLO
import multiprocessing

def main():
    model = YOLO("yolo11n-obb.yaml")
    results = model.train(
        data="DOTAv1.yaml",  # 자동으로 zip 다운로드 & 압축 해제
        epochs=100,
        imgsz=1024,
        device=0,
        workers=0,
        batch=8,
        name="DOTA_pretrain_win"
    )

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
