import cv2
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFileDialog
from ultralytics import YOLO

class upload_video:
    def __init__(self, ui):
        self.ui = ui
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

        self.model = YOLO("best2.pt")

        self.ui.pushButton.clicked.connect(self.open_video)

    def open_video(self):
        file, _ = QFileDialog.getOpenFileName(None, "영상 선택", "", "Video Files (*.mp4 *.avi *.mov)")
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(file)
        self.timer.start(30)

    def update(self):
        ret, frame = self.cap.read()

        if not ret:
            self.timer.stop()
            self.cap.release()
            self.cap = None
            return

        results= self.model.predict(source=frame, conf=0.25, iou=0.45, verbose=False)
        frame = results[0].plot()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg).scaled(self.ui.label_2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.label_2.setPixmap(pixmap)

    