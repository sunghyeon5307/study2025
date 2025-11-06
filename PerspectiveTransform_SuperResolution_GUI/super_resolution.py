from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from form import Ui_Form
import cv2, numpy as np, matplotlib.pyplot as plt
import time
import os

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("app")
        self.setGeometry(100, 100, 300, 200)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.upload_image)
        self.ui.pushButton.clicked.connect(self.perspective_transform)
    
    def upload_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "이미지 1 선택", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.img1_path = path
            self.ui.textEdit.setHtml(f'<img src="{path}" width="400">')
        return path
    
    def perspective_transform(self):
        plt.close('all')
        img_bgr = cv2.imread(self.img1_path)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        pts = plt.ginput(4, timeout=-1)
        plt.close()

        src = np.float32(pts)

        width_top = np.linalg.norm(src[0] - src[1])
        width_bottom = np.linalg.norm(src[2] - src[3])
        height_left = np.linalg.norm(src[0] - src[3])
        height_right = np.linalg.norm(src[1] - src[2])

        W = int(max(width_top, width_bottom))
        H = int(max(height_left, height_right))

        dst = np.float32([[0, 0], [W, 0], [W, H], [0, H]])

        M = cv2.getPerspectiveTransform(src, dst)
        rectified = cv2.warpPerspective(img_bgr, M, (W, H))

        model_path = r"C:\study\20251104\EDSR_x4.pb" 

        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(model_path)
        sr.setModel("edsr", 4) 
        result_sr = sr.upsample(rectified)

        result_path = rf"C:\study\20251104\result_sr_{int(time.time())}.jpg"
        cv2.imwrite(result_path, result_sr)
        self.ui.textEdit_2.setHtml(f'<img src="{result_path}" width="800">')

if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()
