from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from form import Ui_Form
from ultralytics import YOLO
from PIL import Image
from rembg import remove


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.img1_path = None
        self.img2_path = None
        self.model = YOLO("yolov8n-face.pt")

        self.ui.pushButton_2.clicked.connect(self.upload_image1)  
        self.ui.pushButton.clicked.connect(self.upload_image2)    
        self.ui.pushButton_3.clicked.connect(self.remove_bg)     

    def upload_image1(self):
        path, _ = QFileDialog.getOpenFileName(self, "이미지 1 선택", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.img1_path = path
            self.ui.textEdit.setHtml(f'<img src="{path}" width="400">')
        return path

    def upload_image2(self):
        path, _ = QFileDialog.getOpenFileName(self, "이미지 2 선택", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.img2_path = path
            self.ui.textEdit_2.setHtml(f'<img src="{path}" width="400">')

    def remove_bg(self):

        image = Image.open(self.img1_path).convert("RGB")

        overlay = Image.open(self.img2_path).convert("RGBA")
        overlay = remove(overlay)
        overlay_width = overlay.width // 3
        overlay_height = overlay.height // 3
        overlay = overlay.resize((overlay_width, overlay_height))

        results = self.model.predict(source=str(self.img1_path))

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy().tolist()
            for x1, y1, x2, y2 in boxes:
                top_mid_x = (x1 + x2) / 2.0
                top_mid_y = y1

                paste_x = int(top_mid_x - overlay_width // 2)
                paste_y = int(top_mid_y - overlay_height - 10)

                image.paste(overlay, (paste_x, paste_y), overlay)

        output_path = "result.jpg"
        image.save(output_path)
        self.ui.textEdit.setHtml(f'<img src="{output_path}" width="400">')

if __name__ == "__main__":
    app = QApplication([])
    w = App()
    w.show()
    app.exec()
