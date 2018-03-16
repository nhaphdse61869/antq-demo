from PyQt5 import QtGui

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ResultFrame(QWidget):
    NUM, NAME, DATE = range(3)
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(1345, 0, 300, 680)
        self.dataGroupBox = QGroupBox("Result")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.model = self.createLogModel(self)
        self.dataView.setModel(self.model)
        self.addLog(self.model, 'A', 'B', '2h')
        self.addLog(self.model, 'B', 'C', '30m')
        self.addLog(self.model, 'C', 'D', '5m')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)
        self.dataView.clicked.connect(self.applyFormerParameters)
        self.dataGroupBox.hide()

    def createLogModel(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.NUM, Qt.Horizontal, "No")
        model.setHeaderData(self.NAME, Qt.Horizontal, "Record Name")
        model.setHeaderData(self.DATE, Qt.Horizontal, "Created Date")
        return model

    def addLog(self, model, number, recordName, createdDate):
        model.insertRow(0)
        model.setData(model.index(0, self.NUM), number)
        model.setData(model.index(0, self.NAME), recordName)
        model.setData(model.index(0, self.DATE), createdDate)

    def applyFormerParameters(self,index):
        qm = QMessageBox
        ret = qm.question(self, '', "Are you sure to reset all the values?", qm.Yes | qm.No)
        if ret == qm.Yes:
            qm.information(self, '', str(index.row()))
        else:
            qm.information(self, '', "Nothing Changed")