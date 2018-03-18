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
        chartContainer1 = QScrollArea()
        chartContainer2 = QScrollArea()
        leftConLayout.addLayout(topLeftConLayout)
        leftConLayout.addLayout(botLeftConlayout)
        logListTree = ResultFrame(self)
        tableLog = TableLog(self)
        tableLog.setMinimumSize(1000,300)
        rightConLayout.addWidget(logListTree)
        topLeftConLayout.addWidget(tableLog)
        botLeftConlayout.addWidget(chartContainer)
        botLeftConlayout.addWidget(chartContainer1)
        botLeftConlayout.addWidget(chartContainer2)
        self.setLayout(containerLayout)