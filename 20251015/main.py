import time
from save_touch import read_touch, write_touch 
from method.dump import dump_save_keyword
from method.cls import cls_save_keyword
from method.ocr import ocr_save_keyword
from form import Ui_Form
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtCore import QThread, Signal, Qt
from run_touch import start_touch, match_id  # 추가: run_touch.py에서 함수 import

class DetectionWorker(QThread):
    data_signal = Signal(tuple)  # 결과를 메인스레드로 전달하기 위한 시그널
    
    def __init__(self):
        super().__init__()
        self._running = False
        
    def run(self):
        self._running = True
        while self._running:
            try:
                # 터치 감지
                x, y = read_touch()
                if not self._running:
                    break
                    
                xy_print = write_touch(x, y)
                
                # 화면 분석 (무거운 작업들)
                dump_print, dump_keyword, dump_result = dump_save_keyword()
                cls_print, cls_keyword, cls_result = cls_save_keyword()
                ocr_print, ocr_keyword, ocr_result = ocr_save_keyword()
                
                # 결과를 메인스레드로 전송
                self.data_signal.emit((
                    xy_print, 
                    dump_print, dump_keyword, dump_result,
                    cls_print, cls_keyword, cls_result,
                    ocr_print, ocr_keyword, ocr_result
                ))
                
            except Exception as e:
                self.data_signal.emit((f"Error: {str(e)}", "", "", 0, "", "", 0, "", "", 0))
    
    def stop(self):
        self._running = False

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.recording = False
        self.worker = None

        # 버튼 연결
        self.ui.pushButton.clicked.connect(self.script_record_start)   
        self.ui.pushButton_5.clicked.connect(self.script_record_done)  
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
        
        # 워커 스레드 시작
        self.worker = DetectionWorker()
        self.worker.data_signal.connect(self.handle_detection_data)
        self.worker.start()

    def handle_detection_data(self, data):
        # 워커로부터 받은 데이터 처리
        xy_print, dump_print, dump_keyword, dump_result, \
        cls_print, cls_keyword, cls_result, \
        ocr_print, ocr_keyword, ocr_result = data
        
        # UI 업데이트
        output_text = f"{xy_print}\n{dump_print}\n{cls_print}\n{ocr_print}\n{'-'*50}"
        self.ui.textEdit_2.append(output_text)
        
        # 결과 저장
        if self.recording:
            self.save_method(dump_keyword, dump_result, 
                           cls_keyword, cls_result,
                           ocr_keyword, ocr_result)

    def script_record_done(self):
        if not self.recording:
            return
        
        # 워커 스레드 정리
        if self.worker:
            self.worker.stop()
            # 최대 2초간 스레드 종료 대기
            if not self.worker.wait(2000):  
                try:
                    self.worker.terminate()  # 2초 후에도 안 끝나면 강제 종료
                    self.worker.wait(1000)   # 강제 종료 완료 대기
                except:
                    pass
            self.worker = None
            
        self.recording = False
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.textEdit_2.append("스크립트 기록 완료")

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

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec()
