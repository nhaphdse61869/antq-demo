from PyQt5 import QtGui

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.DetailLog import *


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
        self.model = QtGui.QStandardItemModel()
        self.dataView.setModel(self.model)
        self.currentPos = -1
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.model = self.createLogModel(self)
        self.dataView.setModel(self.model)
        addLog = QPushButton('ok')
        self.addLog(self.model, 'LOG1', 'Ant-Q Log DataSet1', '21-3-2018')
        self.addLog(self.model, 'LOG2', 'ACO Log DataSet2', '21-3-2018')
        self.addLog(self.model, 'LOG3', 'FI Log DataSet1', '19-3-2018')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.filterGroupBox)
        mainLayout.addWidget(self.dataGroupBox)

        self.setLayout(mainLayout)
        self.dataView.clicked.connect(self.openDetail)
        self.dataView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dataView.customContextMenuRequested.connect(self.openMenu)
        self.menu = QMenu()
        self.renameAction = QAction(QIcon('exit24.png'), 'Rename', self)
        self.removeAction = QAction(QIcon('exit24.png'), 'Remove', self)
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.removeAction)
        self.renameAction.triggered.connect(self.renameLogItem)


        #self.dataGroupBox.hide()

    def createLogModel(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.NUM, Qt.Horizontal, "KEY")
        model.setHeaderData(self.NAME, Qt.Horizontal, "Record Name")
        model.setHeaderData(self.DATE, Qt.Horizontal, "Created Date")
        return model

    def addLog(self, model, number, recordName, createdDate):
        model.insertRow(0)
        model.setData(model.index(0, self.NUM), number)
        model.setData(model.index(0, self.NAME), recordName)
        model.setData(model.index(0, self.DATE), createdDate)

    def selectionchange(self, i):
        for count in range(self.algorithmCb.count()):
            self.algorithmCb.itemText(count)

    def openMenu(self, position):
        self.currentPos = position
        self.menu.exec_(self.dataView.viewport().mapToGlobal(position))

    def iterItems(self, root):
        def recurse(parent):
            for row in range(parent.rowCount()):
                for column in range(parent.columnCount()):
                    child = parent.child(row, column)
                    yield child
                    if child.hasChildren():
                        yield from recurse(child)
        if root is not None:
            yield from recurse(root)

    def renameLogItem(self):
        model = self.dataView.selectionModel()
        item = model.currentIndex()
        qm = QMessageBox
        qm.information(self, "", str(item.row))

    def openDetail(self,pos):
        detailLog = DetailLog(self)
        root = self.dataView.model().invisibleRootItem()
        child = root.child(pos.row(),0)
        qm = QMessageBox
        qm.information(self, "", child.text())
        detailLog.show()


