
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog


class DetailLog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(100, 100, 700, 600)
        self.setFixedSize(self.size())
        mainLayout = QVBoxLayout(self)
        formContainer = QGroupBox("Log Edition")
        formContainer.setStyleSheet("border: 1px solid #ccc!important; border-radius: 16px; padding-left:10px; padding-top:5px;")
        formContainer1 = QGroupBox("Log Detail")
        formContainer1.setStyleSheet("border: 1px solid #ccc!important; border-radius: 16px;padding-left:10px; padding-top:5px;")
        formContainer1.setFixedHeight(200)
        formContainer2 = QGroupBox("Result Chart")
        formContainer2.setStyleSheet("border: 1px solid #ccc!important; border-radius: 16px;padding-left:10px; padding-top:5px;")
        formContainer2.setFixedHeight(300)
        childLayout = QGridLayout()
        labelLogName = QLabel("Log Name:")
        labelLogName.setFixedWidth(200)
        lineLogName = QLabel("LOG1")
        labelCrDate = QLabel("Created Date:")
        labelCrDate.setFixedWidth(200)
        lineCrDate = QLabel("21-3-2018")
        labelLogName.setStyleSheet("border:none;")
        lineLogName.setStyleSheet("border:none;")
        labelCrDate.setStyleSheet("border:none;")
        lineCrDate.setStyleSheet("border:none;")
        childLayout.addWidget(labelLogName, 0, 0)
        childLayout.addWidget(lineLogName, 0, 1)
        childLayout.addWidget(labelCrDate, 1, 0)
        childLayout.addWidget(lineCrDate, 1, 1)
        childLayout1 = QFormLayout()
        childLayout2 = QFormLayout()
        formContainer.setLayout(childLayout)
        formContainer1.setLayout(childLayout1)
        formContainer2.setLayout(childLayout2)
        mainLayout.addWidget(formContainer)
        mainLayout.addWidget(formContainer1)
        mainLayout.addWidget(formContainer2)
        self.setLayout(mainLayout)
