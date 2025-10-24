import time
from save_touch import read_touch, write_touch 
from method.dump import dump_save_keyword
from method.cls import cls_save_keyword
from method.ocr import ocr_save_keyword
from form import Ui_Form
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer  
from save_touch import read_touch, write_touch
from run_touch import start_touch, match_id

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.recording = False
        self.timer = QTimer(self)
        self.timer.setInterval(300)  # ms 단위, 필요시 조절
        self.timer.timeout.connect(self._record_tick)

        # 버튼 연결
        self.ui.pushButton.clicked.connect(self.script_record_start)   # 시작
        self.ui.pushButton_5.clicked.connect(self.script_record_done)  # 종료
        self.ui.pushButton_2.clicked.connect(self.run_script)
        self.ui.pushButton_3.clicked.connect(self.script_check)
        self.ui.pushButton_4.clicked.connect(self.script_clean)

    def script_record_start(self):
        if self.recording:
            return  # 이미 녹화 중이면 재시작 방지
        self.recording = True
        self.ui.textEdit_2.append("스크립트 기록 시작")
        self.ui.pushButton.setEnabled(False)     # 시작버튼 비활성화
        self.ui.pushButton_5.setEnabled(True)    # 종료버튼 활성화
        self.timer.start()  

    def _record_tick(self):
        try:
            x, y = read_touch()
            xy_print = write_touch(x, y) 

            dump_print, dump_keyword, dump_result = dump_save_keyword()
            cls_print, cls_keyword, cls_result = cls_save_keyword()
            ocr_print, ocr_keyword, ocr_result = ocr_save_keyword()

            output_text = f"{xy_print}\n{dump_print}\n{cls_print}\n{ocr_print}\n{'-'*50}"
            self.ui.textEdit_2.append(output_text)

            self.save_method(dump_keyword, dump_result, cls_keyword, cls_result,
                             ocr_keyword, ocr_result)

        except Exception as e:
            pass

    def save_method(self, dump_keyword, dump_result, cls_keyword, cls_result, 
                    ocr_keyword, ocr_result):
        if dump_result >= cls_result and dump_result >= ocr_result:
            method = "dump"; id = dump_keyword
        elif cls_result >= dump_result and cls_result >= ocr_result:
            method = "cls"; id = cls_keyword
        else:
            method = "ocr"; id = ocr_keyword
        with open("log.tsv", "a", encoding="utf-8") as f:
            f.write(f"ID:{id}\nMETHOD:{method}\n\n")

    def script_clean(self):
        with open("log.tsv", "w", encoding="utf-8") as f:
            f.write("")

    def script_check(self):
        with open("log.tsv", "r", encoding="utf-8") as f:
            content = f.read()
        self.ui.textEdit_3.setPlainText(content)

    def run_script(self):
        start_touch()
        result = match_id()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_2.append(result)

    def script_record_done(self):
        if not self.recording:
            return
        self.timer.stop()           
        self.recording = False
        self.ui.pushButton.setEnabled(True)  
        self.ui.pushButton_5.setEnabled(False)
        self.ui.textEdit_2.append("스크립트 기록 완료")

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec()
