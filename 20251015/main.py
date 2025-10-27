# import time
# from save_touch import read_touch, write_touch 
# from method.dump import dump_save_keyword
# from method.cls import cls_save_keyword
# from method.ocr import ocr_save_keyword
# from form import Ui_Form
# from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
# from PySide6.QtCore import QThread, Signal, Qt
# from run_touch import start_touch, match_id

# class DetectionWorker(QThread):
#     data_signal = Signal(tuple)  
    
#     def __init__(self):
#         super().__init__()
#         self._running = False
        
#     def run(self):
#         self._running = True
#         while self._running:
#             try:
#                 x, y = read_touch()
#                 if not self._running:
#                     break
                    
#                 xy_print = write_touch(x, y)
                
#                 dump_print, dump_keyword, dump_result = dump_save_keyword()
#                 cls_print, cls_keyword, cls_result = cls_save_keyword()
#                 ocr_print, ocr_keyword, ocr_result = ocr_save_keyword()
                
#                 self.data_signal.emit((
#                     xy_print, 
#                     dump_print, dump_keyword, dump_result,
#                     cls_print, cls_keyword, cls_result,
#                     ocr_print, ocr_keyword, ocr_result
#                 ))
                
#             except Exception as e:
#                 self.data_signal.emit((f"Error: {str(e)}", "", "", 0, "", "", 0, "", "", 0))
    
#     def stop(self):
#         self._running = False

# class App(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)
        
#         self.recording = False
#         self.worker = None

#         self.ui.pushButton.clicked.connect(self.script_record_start)   
#         self.ui.pushButton_5.clicked.connect(self.script_record_done)  
#         self.ui.pushButton_2.clicked.connect(self.run_script)
#         self.ui.pushButton_3.clicked.connect(self.script_check)
#         self.ui.pushButton_4.clicked.connect(self.script_clean)

#     def script_record_start(self):
#         if self.recording:
#             return
#         self.recording = True
#         self.ui.textEdit_2.append("스크립트 기록 시작")
#         self.ui.pushButton.setEnabled(False)
#         self.ui.pushButton_5.setEnabled(True)
        
#         self.worker = DetectionWorker()
#         self.worker.data_signal.connect(self.handle_detection_data)
#         self.worker.start()

#     def handle_detection_data(self, data):
#         xy_print, dump_print, dump_keyword, dump_result, \
#         cls_print, cls_keyword, cls_result, \
#         ocr_print, ocr_keyword, ocr_result = data
        
#         output_text = f"{xy_print}\n{dump_print}\n{cls_print}\n{ocr_print}\n{'-'*50}"
#         self.ui.textEdit_2.append(output_text)
        
#         if self.recording:
#             self.save_method(dump_keyword, dump_result, 
#                            cls_keyword, cls_result,
#                            ocr_keyword, ocr_result)

#     def script_record_done(self):
#         if not self.recording:
#             return
        
#         if self.worker:
#             self.worker.stop()
#             if not self.worker.wait(2000):  
#                 try:
#                     self.worker.terminate() 
#                     self.worker.wait(1000)   
#                 except:
#                     pass
#             self.worker = None
            
#         self.recording = False
#         self.ui.pushButton.setEnabled(True)
#         self.ui.pushButton_5.setEnabled(False)
#         self.ui.textEdit_2.append("스크립트 기록 완료")

#     def save_method(self, dump_keyword, dump_result, cls_keyword, cls_result, 
#                     ocr_keyword, ocr_result):
#         if dump_result >= cls_result and dump_result >= ocr_result:
#             method = "dump"; id = dump_keyword
#         elif cls_result >= dump_result and cls_result >= ocr_result:
#             method = "cls"; id = cls_keyword
#         else:
#             method = "ocr"; id = ocr_keyword
#         with open("log.tsv", "a", encoding="utf-8") as f:
#             f.write(f"ID:{id}\nMETHOD:{method}\n\n")

#     def script_clean(self):
#         with open("log.tsv", "w", encoding="utf-8") as f:
#             f.write("")

#     def script_check(self):
#         with open("log.tsv", "r", encoding="utf-8") as f:
#             content = f.read()
#         self.ui.textEdit_3.setPlainText(content)

#     def run_script(self):
#         start_touch()
#         result = match_id()
#         self.ui.textEdit_2.clear()
#         self.ui.textEdit_2.append(result)

# if __name__ == "__main__":
#     app = QApplication([])
#     window = App()
#     window.show()
#     app.exec()


from save_touch import read_touch, write_touch
from method.cls import cls_save_keyword
from method.ocr import ocr_save_keyword
from form import Ui_Form
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtCore import QThread, Signal, Qt
from run_touch import start_touch, match_id


class DetectionWorker(QThread):
    data_signal = Signal(tuple)

    def __init__(self):
        super().__init__()
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            try:
                x, y = read_touch()

                xy_print = write_touch(x, y)

                cls_print, cls_keyword, cls_result = cls_save_keyword()
                ocr_print, ocr_keyword, ocr_result = ocr_save_keyword()

                self.data_signal.emit((
                    xy_print,
                    cls_print, cls_keyword, cls_result,
                    ocr_print, ocr_keyword, ocr_result
                ))

            except Exception as e:
                pass

    def stop(self):
        self._running = False

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.recording = False
        self.worker = None

        self.ui.pushButton.clicked.connect(self.script_record_start)   # 시작
        self.ui.pushButton_5.clicked.connect(self.script_record_done)  # 종료
        self.ui.pushButton_2.clicked.connect(self.run_script)
        self.ui.pushButton_3.clicked.connect(self.script_check)
        self.ui.pushButton_4.clicked.connect(self.script_clean)

    def script_record_start(self):
        if self.recording:
            return
        self.recording = True
        self.ui.textEdit_2.append("스크립트 기록 시작")
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_5.setEnabled(True)

        self.worker = DetectionWorker()
        self.worker.data_signal.connect(self.handle_detection_data)
        self.worker.start()

    def handle_detection_data(self, data):
        (
            xy_print,
            cls_print, cls_keyword, cls_result,
            ocr_print, ocr_keyword, ocr_result
        ) = data

        output_text = f"{xy_print}\n{cls_print}\n{ocr_print}\n{'-'*50}"
        self.ui.textEdit_2.append(output_text)

        if self.recording:
            self.save_method(
                cls_keyword, cls_result,
                ocr_keyword, ocr_result
            )

    def script_record_done(self):
        if not self.recording:
            return

        if self.worker:
            self.worker.stop()
            if not self.worker.wait(2000):
                try:
                    self.worker.terminate()
                    self.worker.wait(1000)
                except:
                    pass
            self.worker = None

        self.recording = False
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.textEdit_2.append("스크립트 기록 완료")

    def save_method(self, cls_keyword, cls_result, ocr_keyword, ocr_result):
        # cls vs ocr 중 높은 점수 선택 (동률이면 cls 우선)
        if cls_result >= ocr_result:
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

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec()
