from PyQt5 import QtGui
import sys
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI.DetailLog import *
from util.logging import LogIO


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
        self.algorithmCb.addItem('All',0)
        self.algorithmCb.addItem('Ant-Q',1)
        self.algorithmCb.addItem('ACO',2)
        self.algorithmCb.addItem('SA', 3)
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
        # Init list log
        self.log_io = LogIO()
        self.list_log = []
        #self.load_list_log()
        self.dataView.setCurrentIndex(self.model.index(0, 0));
        #self.dataView.selectionModel().setCurrentIndex(self.model.createIndex( 0, 0), QItemSelectionModel.SelectCurrent)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.filterGroupBox)
        mainLayout.addWidget(self.dataGroupBox)

        self.setLayout(mainLayout)
        #self.dataView.clicked.connect(self.openDetail)
        self.dataView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dataView.customContextMenuRequested.connect(self.openMenu)
        #self.dataView.setItem
        self.menu = QMenu()
        self.renameAction = QAction(QIcon('exit24.png'), 'Rename', self)
        self.removeAction = QAction(QIcon('exit24.png'), 'Remove', self)
        self.viewDetailAction = QAction(QIcon('exit24.png'), 'View Detail', self)
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.removeAction)
        self.menu.addAction(self.viewDetailAction)
        self.renameAction.triggered.connect(self.renameLogItem)
        self.removeAction.triggered.connect(self.removeLog)
        self.viewDetailAction.triggered.connect(self.openDetail)
        root = self.dataView.model().invisibleRootItem()
        child = root.child(0, 0)
        if child != None:
            self.currentKey = child.text()
        self.dataView.clicked.connect(self.getCurrentKeyLog)
        self.searchBtn.clicked.connect(self.searchFilter)
        #self.dataGroupBox.hide()

    def load_list_log(self):
        self.clearAllRecords()
        self.list_log = self.log_io.get_list_log()
        for log in self.list_log:
            self.addLog(self.model, log.key, log.name, log.created_date)


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

    def removeLog(self):
        root = self.dataView.model().invisibleRootItem()
        child = root.child(self.currentPos.row(), 0)
        log_key = child.text()
        self.log_io.remove_log(int(log_key))
        root.removeRow(self.currentPos.row())

    def selectionchange(self, i):
        for count in range(self.algorithmCb.count()):
            self.algorithmCb.itemText(count)

    def openMenu(self, position):
        indexes = self.dataView.selectedIndexes()
        if indexes != None:
            self.currentPos = indexes[0]
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
        try:
            root = self.dataView.model().invisibleRootItem()
            text, ok = QInputDialog.getText(self, 'Change Log Name', 'Enter New Log Name:')
            child = root.child(self.currentPos.row(), 0)
            log_key = child.text()
            if ok:
                self.log_io.rename_log(int(log_key), text)
                root.setChild(int(self.currentPos.row()), 1, QStandardItem(text))
                #root.setData(root.indexOfChild(root.child(self.currentPos.row(), 1)), text)
                #root.setData(root.index(self.currentPos.row(), 1), text)
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)


    def openDetail(self):
        detailLog = DetailLog(self)
        root = self.dataView.model().invisibleRootItem()
        child = root.child(self.currentPos.row(),0)
        qm = QMessageBox
        qm.information(self, "", child.text())
        detailLog.show()

    def getCurrentKeyLog(self):
        indexes = self.dataView.selectedIndexes()
        if indexes != None:
            self.currentPos = indexes[0]
            root = self.dataView.model().invisibleRootItem()
            child = root.child(self.currentPos.row(), 0)
            self.currentKey = child.text()

    def clearAllRecords(self):
        root = self.dataView.model()
        root.removeRows(0, root.rowCount())

    def searchFilter(self):
        #Clear all records
        self.clearAllRecords()

        #Find record
        show_logs = []
        algorithm = self.algorithmCb.itemData(self.algorithmCb.currentIndex())
        searchInput = self.nameSearch.text()

        if algorithm == 1:
            #Searching AntQ
            for i in range(len(self.list_log)):
                if self.list_log[i].algorithm == "AntQ":
                    show_logs.append(self.list_log[i])
        elif algorithm == 2:
            #Searching ACO
            for i in range(len(self.list_log)):
                if self.list_log[i].algorithm == "ACO":
                    show_logs.append(self.list_log[i])
        elif algorithm == 3:
            #Searching Simulated Annealing
            for i in range(len(self.list_log)):
                if self.list_log[i].algorithm == "Simulated Annealing":
                    show_logs.append(self.list_log[i])
        else:
            #Searching all
            show_logs = self.list_log

        result_logs = []
        #Searching for name
        if searchInput != "":
            for i in range(len(show_logs)):
                if searchInput in show_logs[i].name:
                    result_logs.append(show_logs[i])
        else:
            result_logs = show_logs

        for log in result_logs:
            self.addLog(self.model, log.key, log.name, log.created_date)