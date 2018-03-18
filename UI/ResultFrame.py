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
        #self.setGeometry(0, 0, 300, 680)
        self.dataGroupBox = QGroupBox("Log")
        self.filterGroupBox = QGroupBox("Filter")
        self.filterLayout = QHBoxLayout()
        self.algorithmCb = QComboBox()
        self.algorithmCb.addItem('All')
        self.algorithmCb.addItem('Ant-Q')
        self.algorithmCb.addItem('ACO')
        self.nameSearch = QLineEdit()
        self.searchBtn = QPushButton('Search')
        self.filterLayout.addWidget(self.algorithmCb)
        self.filterLayout.addWidget(self.nameSearch)
        self.filterLayout.addWidget(self.searchBtn)
        self.filterGroupBox.setLayout(self.filterLayout)
        self.algorithmCb.currentIndexChanged.connect(self.selectionchange)
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.model = self.createLogModel(self)
        self.dataView.setModel(self.model)
        addLog = QPushButton('ok')
        self.addLog(self.model, addLog, 'B', '2h')
        self.addLog(self.model, 'B', 'C', '30m')
        self.addLog(self.model, 'C', 'D', '5m')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.filterGroupBox)
        mainLayout.addWidget(self.dataGroupBox)

        self.setLayout(mainLayout)
        #self.dataView.clicked.connect(self.applyFormerParameters)
        self.dataView.customContextMenuRequested.connect(self.openMenu)
        #self.dataGroupBox.hide()

    def createLogModel(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.NUM, Qt.Horizontal, "Action")
        model.setHeaderData(self.NAME, Qt.Horizontal, "Record Name")
        model.setHeaderData(self.DATE, Qt.Horizontal, "Created Date")
        return model

    def addLog(self, model, number, recordName, createdDate):
        model.insertRow(0)
        model.setData(model.index(0, self.NUM), number)
        model.setData(model.index(0, self.NAME), recordName)
        model.setData(model.index(0, self.DATE), createdDate)

    def applyFormerParameters(self,index):
        menu = QMenu()
        menu.addAction('Rename')
        menu.addAction('Remove')
        #menu.exec_(index)

    def selectionchange(self, i):
        for count in range(self.algorithmCb.count()):
            self.algorithmCb.itemText(count)

    def openMenu(self, position):
        menu = QMenu()
        menu.addAction("Edit object/container")
        menu.addAction("Edit object")
        menu.exec_(self.dataView.viewport().mapToGlobal(position))