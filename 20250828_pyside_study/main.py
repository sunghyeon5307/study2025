import sys
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtCore import Slot
from fruit_ui import Ui_Form   # 위에서 생성된 파일


class Window(QWidget): # Window라는 창을 QWidget을 바탕으로 만들겠다
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form() # 내가 만든 ui화면 불러오기
        self.ui.setupUi(self) # 불러온 디자인을 Window에 배치하기

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.pushButton.clicked.connect(self.page2)       
        self.ui.pushButton_2.clicked.connect(self.page1)     

    def page2(self):
        radios = [self.ui.radioButton, self.ui.radioButton_2, self.ui.radioButton_3, self.ui.radioButton_4]
        select = None
        for rb in radios:
            if rb.isChecked():        # 버튼이 체크돼 있다면
                select = rb.text()       # 그 버튼의 글자 저장
                break                 # 첫 번째 찾은 것만 쓰고 멈춤
        if not select:
            QMessageBox.information(self, "알림", "과일을 하나 선택해 주세요.")
            return
        self.ui.label_4.setText(select)
        self.ui.stackedWidget.setCurrentIndex(1)

    def page1(self):
        self.ui.stackedWidget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
