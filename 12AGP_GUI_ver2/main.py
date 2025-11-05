from save_touch import read_touch, write_touch
from cls import cls_save_keyword
from form import Ui_Form
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QThread, Signal
from run_touch import start_touch
import time, subprocess, os

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
                time.sleep(1)
                cls_print, cls_keyword, cls_result = cls_save_keyword()
                self.data_signal.emit((xy_print, cls_print, cls_keyword, cls_result))
            except Exception:
                pass

    def stop(self):
        self._running = False


class ScriptRunnerWorker(QThread):
    result_signal = Signal(tuple)
    finished_signal = Signal()

    def run(self):
        results = start_touch()
        for result, img_path in results:
            self.result_signal.emit((result, img_path))
            time.sleep(0.1)  
        self.finished_signal.emit()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.recording = False
        self.worker = None

        self.ui.pushButton.clicked.connect(self.script_record_start)
        self.ui.pushButton_5.clicked.connect(self.script_record_done)
        self.ui.pushButton_2.clicked.connect(self.run_script)
        self.ui.pushButton_3.clicked.connect(self.script_check)
        self.ui.pushButton_4.clicked.connect(self.script_clean)
        self.ui.pushButton_6.clicked.connect(self.textedit2_clean)
        self.ui.pushButton_7.clicked.connect(self.textedit3_clean)
        self.ui.pushButton_8.clicked.connect(self.textedit_clean)

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
        xy_print, cls_print, cls_keyword, cls_result = data
        output_text = f"{xy_print}\n{cls_print}\n{'-'*50}"
        self.ui.textEdit_2.append(output_text)

        if self.recording:
            self.save_method(cls_keyword, cls_result)

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

    def save_method(self, cls_keyword, cls_result):
        with open("log.tsv", "a", encoding="utf-8") as f:
            f.write(f"ID:{cls_keyword}\nMETHOD:cls\n\n")

    def script_clean(self):
        open("log.tsv", "w", encoding="utf-8").close()
    
    def textedit_clean(self):
        self.ui.textEdit.clear()

    def textedit2_clean(self):
        self.ui.textEdit_2.clear()

    def textedit3_clean(self):
        self.ui.textEdit_3.clear()

    def script_check(self):
        with open("log.tsv", "r", encoding="utf-8") as f:
            self.ui.textEdit_3.setPlainText(f.read())

    def run_script(self):
        self.ui.textEdit_2.append("----------------------------------")
        self.ui.textEdit_2.append("스크립트 실행 시작")
        QApplication.processEvents()

        self.runner = ScriptRunnerWorker()
        self.runner.result_signal.connect(self.handle_script_result)
        self.runner.finished_signal.connect(self.handle_script_finished)
        self.runner.start()
    
    def handle_script_result(self, data):
        result, img_path = data
        self.ui.textEdit_2.append(result)
        QApplication.processEvents()

        if result.startswith("(NG)"):
            if img_path and os.path.exists(img_path):
                accumulated_html = self.ui.textEdit.toHtml()
                new_img_html = f'<img src="{img_path}" width="300" style="margin:5px;"><br><br>'
                accumulated_html += new_img_html
                self.ui.textEdit.setHtml(accumulated_html)
                self.ui.textEdit.append("--------------------------------------------------")
                QApplication.processEvents()

            mem = subprocess.run(
                ["adb", "shell", "grep -E 'MemTotal|MemAvailable|SwapTotal|SwapFree' /proc/meminfo"],
                capture_output=True, text=True, shell=True
            )

            self.ui.textEdit_2.append(mem.stdout)
            QApplication.processEvents()

        self.ui.textEdit_2.append("--------------------------------")
        QApplication.processEvents()

    def handle_script_finished(self):
        self.ui.textEdit_2.append("스크립트 실행 완료")
        QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec()
