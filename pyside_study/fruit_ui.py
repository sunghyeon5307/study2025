# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fruit_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QRadioButton,
    QSizePolicy, QStackedWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(695, 370)
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(170, 0, 471, 371))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 20, 361, 41))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.pushButton = QPushButton(self.page)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(50, 60, 181, 51))
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(False)
        self.pushButton.setFont(font1)
        self.radioButton_4 = QRadioButton(self.page)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(60, 230, 94, 20))
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(True)
        self.radioButton_4.setFont(font2)
        self.radioButton = QRadioButton(self.page)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(60, 140, 94, 20))
        self.radioButton.setFont(font2)
        self.radioButton_2 = QRadioButton(self.page)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(60, 169, 94, 21))
        self.radioButton_2.setFont(font2)
        self.radioButton_3 = QRadioButton(self.page)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(60, 200, 94, 20))
        self.radioButton_3.setFont(font2)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 0, 72, 47))
        font3 = QFont()
        font3.setPointSize(15)
        font3.setBold(True)
        self.label_2.setFont(font3)
        self.label_4 = QLabel(self.page_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(120, 80, 81, 41))
        font4 = QFont()
        font4.setPointSize(13)
        self.label_4.setFont(font4)
        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 80, 104, 31))
        font5 = QFont()
        font5.setPointSize(10)
        font5.setBold(True)
        self.label_3.setFont(font5)
        self.pushButton_2 = QPushButton(self.page_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 140, 109, 31))
        self.pushButton_2.setFont(font1)
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"2025.08.25", None))
        self.label.setText(QCoreApplication.translate("Form", u"2025.08.25 Pyside6 \uacf5\ubd80", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"2\ud398\uc774\uc9c0 \uc774\ub3d9", None))
        self.radioButton_4.setText(QCoreApplication.translate("Form", u"\uc218\ubc15", None))
        self.radioButton.setText(QCoreApplication.translate("Form", u"\uc0ac\uacfc", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"\ubcf5\uc22d\uc544", None))
        self.radioButton_3.setText(QCoreApplication.translate("Form", u"\ud3ec\ub3c4", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"2\ud398\uc774\uc9c0", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\ub0b4\uac00 \uc120\ud0dd\ud55c \uacfc\uc77c:", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"1\ud398\uc774\uc9c0 \uc774\ub3d9", None))
    # retranslateUi

