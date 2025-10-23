from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from form import Ui_Form
from ultralytics import YOLO
from PIL import Image
from rembg import remove
# from detection import detect_face
model = YOLO("yolov8n-face.pt")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.img1_path = None
        self.img2_path = None
        self.model = YOLO("yolov8n-face.pt")

        self.ui.pushButton_2.clicked.connect(self.upload_image1)  # 사진 업로드 1
        self.ui.pushButton.clicked.connect(self.upload_image2)  # 사진 업로드 2
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
        if not self.img1_path or not self.img2_path:
            return
        
        image = Image.open(self.img1_path).convert("RGB")
        
        overlay = Image.open(self.img2_path).convert("RGBA")
        # 배경 제거
        overlay = remove(overlay)
        # 크기 조정
        overlay_width = overlay.width // 4
        overlay_height = overlay.height // 4
        overlay = overlay.resize((overlay_width, overlay_height))

        # YOLO 예측
        results = self.model.predict(source=str(self.img1_path))

        for result in results:  
            boxes = result.boxes.xyxy.cpu().numpy().tolist()
            for x1, y1, x2, y2 in boxes:
                top_mid_x = (x1 + x2) / 2.0
                top_mid_y = y1
                
                paste_x = int(top_mid_x - overlay_width // 2)
                paste_y = int(top_mid_y - overlay_height -5)
                
                # 배경이 제거된 이미지 합성
                image.paste(overlay, (paste_x, paste_y), overlay)
        
        # 결과 이미지 저장
        output_path = "result_with_overlay.jpg"
        image.save(output_path)
        
        # 결과 이미지를 텍스트창에 표시
        self.ui.textEdit.setHtml(f'<img src="{output_path}" width="400">')
    
def detect_face(img1):
    results = model.predict(source=img1, save=True, save_txt=True)
    return results

def remove_bg(self):

    img2 = Image.open(self.img2_path).convert("RGBA")

    img2_no_bg = remove(img2)
    


app = QApplication([])
w = App()
w.show()
app.exec()
