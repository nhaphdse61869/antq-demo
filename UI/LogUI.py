from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UI.ResultFrame import *
from UI.Table import *

class UILog(QWidget):

    def __init__(self):
        super().__init__()
        containerLayout = QHBoxLayout()
        leftConLayout = QVBoxLayout()
        rightConLayout = QVBoxLayout()
        leftConLayout.setSizeConstraint(QLayout.SetFixedSize)
        #leftConLayout.re
        containerLayout.addLayout(leftConLayout)
        containerLayout.addLayout(rightConLayout)
        #leftConLayout.setGeometry(QRect(0, 0, 0, 600))
        topLeftConLayout = QHBoxLayout()
        botLeftConlayout = QHBoxLayout()
        chartContainer = QScrollArea()
        leftConLayout.addLayout(topLeftConLayout)
        leftConLayout.addLayout(botLeftConlayout)
        logListTree = ResultFrame(self)
        tableLog = TableLog(self)
        tableLog.setMinimumSize(1000,300)

        formContainer = QGroupBox()
        formContainerLayout = QHBoxLayout()
        addToTableBtn = QPushButton("Add to Table")
        addToTableBtn.setStyleSheet("box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);")
        compareBtn = QPushButton("Compare")
        formContainerLayout.addWidget(addToTableBtn)
        formContainerLayout.addWidget(compareBtn)
        formContainer.setLayout(formContainerLayout)

        rightConLayout.addWidget(logListTree)
        rightConLayout.addWidget(formContainer)
        topLeftConLayout.addWidget(tableLog)
        botLeftConlayout.addWidget(chartContainer)
        self.setLayout(containerLayout)