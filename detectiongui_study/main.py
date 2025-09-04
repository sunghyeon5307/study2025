import sys
from PySide6.QtWidgets import QApplication, QWidget
from detectionui import Ui_Form  
from pushbutton import upload_video

class VideoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.controller = upload_video(self.ui)

    def closeEvent(self, e):
        self.controller.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VideoApp()
    win.show()
    sys.exit(app.exec())
