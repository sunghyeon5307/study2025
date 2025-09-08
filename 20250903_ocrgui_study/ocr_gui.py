# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ocr_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(711, 478)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.imglabel = QLabel(Form)
        self.imglabel.setObjectName(u"imglabel")
        self.imglabel.setMinimumSize(QSize(400, 300))
        font1 = QFont()
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.imglabel.setFont(font1)

        self.verticalLayout.addWidget(self.imglabel)

        self.textEdit = QTextEdit(Form)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)

        self.uploadbutton = QPushButton(Form)
        self.uploadbutton.setObjectName(u"uploadbutton")
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(False)
        self.uploadbutton.setFont(font2)

        self.verticalLayout.addWidget(self.uploadbutton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"2025\ub1449\uc6d43\uc77c \uc2e4\uc2b5", None))
        self.imglabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.uploadbutton.setText(QCoreApplication.translate("Form", u"\uc774\ubbf8\uc9c0 \uc5c5\ub85c\ub4dc", None))
    # retranslateUi

