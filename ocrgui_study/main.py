import sys
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import cv2

from ocr_gui import Ui_Form
from ocr import OCR

class ocrapp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ocr = OCR()

        self.ui.uploadbutton.clicked.connect(self.on_upload)
        
        self.img_path = None
    
    def on_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        self.img_path=file_path
        self.show_img(file_path)
        self.run_ocr(file_path)

    def show_img(self, path: str):
        pix = QPixmap(path)
        
        scaled = pix.scaled(self.ui.imglabel.width(),
                            self.ui.imglabel.height(),
                            Qt.KeepAspectRatio,
                            Qt.SmoothTransformation)
        self.ui.imglabel.setPixmap(scaled)
    
    def run_ocr(self, path: str):

        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        enlarged = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # img = cv2.imread(path)
        # img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)  # 2배 확대
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        result = self.ocr.run_ocr(enlarged)
        self.ui.textEdit.setText('\n'.join(result))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ocrapp()
    w.show()
    sys.exit(app.exec())
