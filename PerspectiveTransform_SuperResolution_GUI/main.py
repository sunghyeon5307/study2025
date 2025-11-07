# from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
# from form import Ui_Form
# import cv2, numpy as np, matplotlib.pyplot as plt
# import time

# class MainApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("app")
#         self.setGeometry(100, 100, 300, 200)
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)
#         self.ui.pushButton_2.clicked.connect(self.upload_image)
#         self.ui.pushButton.clicked.connect(self.perspective_transform)
    
#     def upload_image(self):
#         path, _ = QFileDialog.getOpenFileName(self, "이미지 1 선택", "", "Images (*.png *.jpg *.jpeg)")
#         if path:
#             self.img1_path = path
#             self.ui.textEdit.setHtml(f'<img src="{path}" width="400">')
#         return path
    
#     def perspective_transform(self):
#         plt.close('all')
#         img_bgr = cv2.imread(self.img1_path)
#         img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

#         plt.figure(figsize=(8, 6))
#         plt.imshow(img)
#         pts = plt.ginput(4, timeout=-1)
#         plt.close()

#         src = np.float32(pts)

#         width_top = np.linalg.norm(src[0] - src[1])
#         width_bottom = np.linalg.norm(src[2] - src[3])
#         height_left = np.linalg.norm(src[0] - src[3])
#         height_right = np.linalg.norm(src[1] - src[2])

#         W = int(max(width_top, width_bottom))
#         H = int(max(height_left, height_right))

#         dst = np.float32([[0, 0], [W, 0], [W, H], [0, H]])

#         M = cv2.getPerspectiveTransform(src, dst)
#         rectified = cv2.warpPerspective(img_bgr, M, (W, H))

#         result_path = rf"C:\study\20251104\result_{int(time.time())}.jpg"
#         cv2.imwrite(result_path, rectified)
#         self.ui.textEdit_2.setHtml(f'<img src="{result_path}" width="400">')
        

# if __name__ == "__main__":
#     app = QApplication([])
#     window = MainApp()
#     window.show()
#     app.exec()


from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from form import Ui_Form
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QImage
import cv2, numpy as np, matplotlib.pyplot as plt
import time, os, subprocess

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("app")
        self.setGeometry(100, 100, 300, 200) # 창 초기 크기
        self.ui = Ui_Form() # UI 폼 객체 생성
        self.ui.setupUi(self) # 디자이너에서 만든 버튼/textEdit 등 배치
        self.ui.pushButton_2.clicked.connect(self.upload_image)
        self.ui.pushButton.clicked.connect(self.perspective_transform)

    def img_resize(self, label, path, max_width=400):
        # opencv=BGR, Qt=RGB
        img = cv2.imread(path) # 이미지 cv로 읽음

        h, w, _ = img.shape
        if w > 2000 or h > 2000: # 2000px
            scale = 2000 / max(w, h)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888) # numpy 이미지 → Qt가 읽을 수 있는 QImage
        pixmap = QPixmap.fromImage(qimg) # QPixmap(Qt에서 화면에 그리기 좋은 형식) 으로 변환
        scaled_pixmap = pixmap.scaledToWidth(max_width) # 가로 폭을 max_width로 줄임(세로는 비율 유지)
        label.setPixmap(scaled_pixmap) # 라벨에 넣기
    
    def upload_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "이미지 1 선택", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.img1_path = path
            self.img_resize(self.ui.label, path)
        return path 
    
    def perspective_transform(self):
        plt.close('all')
        img_bgr = cv2.imread(self.img1_path) # cv로 이미지 읽기(BGR)
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # RGB변환

        plt.figure(figsize=(12, 10)) # 그림 창 크기 지정
        plt.imshow(img) # 그림 창 띄우기
        pts = plt.ginput(4, timeout=-1) # 4점 입력 받음, timeout=-1은 무한대기
        plt.close()

        src = np.float32(pts) # 입력한 점 좌표를 float32형식으로 변환
        width_top = np.linalg.norm(src[0] - src[1])
        width_bottom = np.linalg.norm(src[2] - src[3])
        height_left = np.linalg.norm(src[0] - src[3])
        height_right = np.linalg.norm(src[1] - src[2])

        W = int(max(width_top, width_bottom))
        H = int(max(height_left, height_right))

        dst = np.float32([[0, 0], [W, 0], [W, H], [0, H]])

        M = cv2.getPerspectiveTransform(src, dst)
        rectified = cv2.warpPerspective(img_bgr, M, (W, H))

        time_set = int(time.time())
        base_dir = r"C:\study\PerspectiveTransform_SuperResolution_GUI\Real-ESRGAN"
        input_dir = r"C:\study\PerspectiveTransform_SuperResolution_GUI\Real-ESRGAN\input"
        input_path = os.path.join(input_dir, f"rectified_{time_set}.jpg")
        cv2.imwrite(input_path, rectified)
    
        command = [
            "python",
            os.path.join(base_dir, "inference_realesrgan.py"),
            "-n", "realesr-general-x4v3",
            "-i", input_path,
            "--model_path", os.path.join(base_dir, "weights", "realesr-general-x4v3.pth"),
            "--denoise_strength", "1",
            "-o", os.path.join(base_dir, "results")  
        ]

        subprocess.run(command, shell=True)

        out_dir = r"C:\study\PerspectiveTransform_SuperResolution_GUI\Real-ESRGAN\results"
        result_path = os.path.join(out_dir, f"rectified_{time_set}_out.jpg")

        self.img_resize(self.ui.label_2, result_path)

if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()
