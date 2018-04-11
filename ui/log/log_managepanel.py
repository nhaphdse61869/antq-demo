from PyQt5 import QtGui
import sys
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from util.log import LogIO


class LogPanel(QWidget):
    NUM, NAME, DATE = range(3)
    def __init__(self, parent):
        super().__init__(parent)
        # Panel attributes
        self.current_position = -1
        self.log_io = LogIO()
        self.list_log = []

        # Main layout
        main_layout = QVBoxLayout()

        # Sub layout
        self.filter_group_box = QGroupBox("Filter")
        self.data_group_box = QGroupBox("Log")

        # Filter layout
        self.filter_layout = QHBoxLayout()

        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.addItem('All', 0)
        self.algorithm_combobox.addItem('Ant-Q', 1)
        self.algorithm_combobox.addItem('ACO', 2)
        self.algorithm_combobox.addItem('SA', 3)

        self.search_name_textbox = QLineEdit()
        self.search_button = QPushButton('Search')

        self.filter_layout.addWidget(self.algorithm_combobox)
        self.filter_layout.addWidget(self.search_name_textbox)
        self.filter_layout.addWidget(self.search_button)
        self.filter_group_box.setLayout(self.filter_layout)

        # Data layout
        data_layout = QHBoxLayout()
        self.log_table = QTreeView()

        self.model = QStandardItemModel(0, 3, parent)
        self.model.setHeaderData(self.NUM, Qt.Horizontal, "KEY")
        self.model.setHeaderData(self.NAME, Qt.Horizontal, "Record Name")
        self.model.setHeaderData(self.DATE, Qt.Horizontal, "Created Date")

        self.log_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.log_table.setRootIsDecorated(False)
        self.log_table.setAlternatingRowColors(True)
        self.log_table.setModel(self.model)

        data_layout.addWidget(self.log_table)
        self.data_group_box.setLayout(data_layout)

        # List log
        self.loadListLog()
        self.log_table.setCurrentIndex(self.model.index(0, 0));

        self.log_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.log_table.customContextMenuRequested.connect(self.openMenu)

        self.menu = QMenu()
        self.rename_action = QAction(QIcon('exit24.png'), 'Rename', self)
        self.remove_action = QAction(QIcon('exit24.png'), 'Remove', self)

        self.menu.addAction(self.rename_action)
        self.menu.addAction(self.remove_action)

        root = self.log_table.model().invisibleRootItem()
        child = root.child(0, 0)
        if child != None:
            self.currentKey = child.text()

        # Connect widget signal
        self.algorithm_combobox.currentIndexChanged.connect(self.selectionchange)
        self.rename_action.triggered.connect(self.renameLog)
        self.remove_action.triggered.connect(self.removeLog)
        self.log_table.clicked.connect(self.getCurrentKeyLog)
        self.search_button.clicked.connect(self.searchLogs)

        #Add to main layout
        main_layout.addWidget(self.filter_group_box)
        main_layout.addWidget(self.data_group_box)
        self.setLayout(main_layout)


    def loadListLog(self):
        self.clearAllRecords()
        self.list_log = self.log_io.getListLog()
        for log in self.list_log:
            self.addLog(self.model, log.key, log.name, log.created_date)

    def addLog(self, model, number, recordName, createdDate):
        model.insertRow(0)
        model.setData(model.index(0, self.NUM), number)
        model.setData(model.index(0, self.NAME), recordName)
        model.setData(model.index(0, self.DATE), createdDate)

    def removeLog(self):
        root = self.log_table.model().invisibleRootItem()
        child = root.child(self.current_position.row(), 0)
        log_key = child.text()
        self.log_io.removeLog(int(log_key))
        root.removeRow(self.current_position.row())

    def selectionchange(self, i):
        for count in range(self.algorithm_combobox.count()):
            self.algorithm_combobox.itemText(count)

    def openMenu(self, position):
        indexes = self.log_table.selectedIndexes()
        if indexes != None:
            self.current_position = indexes[0]
            self.menu.exec_(self.log_table.viewport().mapToGlobal(position))

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

    def renameLog(self):
        try:
            root = self.log_table.model().invisibleRootItem()
            text, ok = QInputDialog.getText(self, 'Change Log Name', 'Enter New Log Name:')
            child = root.child(self.current_position.row(), 0)
            log_key = child.text()
            if ok:
                self.log_io.renameLog(int(log_key), text)
                root.setChild(int(self.current_position.row()), 1, QStandardItem(text))
                #root.setData(root.indexOfChild(root.child(self.currentPos.row(), 1)), text)
                #root.setData(root.index(self.currentPos.row(), 1), text)
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)

    def getCurrentKeyLog(self):
        indexes = self.log_table.selectedIndexes()
        if indexes != None:
            self.current_position = indexes[0]
            root = self.log_table.model().invisibleRootItem()
            child = root.child(self.current_position.row(), 0)
            self.currentKey = child.text()

    def clearAllRecords(self):
        root = self.log_table.model()
        root.removeRows(0, root.rowCount())

    def searchLogs(self):
        #Clear all records
        self.clearAllRecords()

        #Find record
        show_logs = []
        algorithm = self.algorithm_combobox.itemData(self.algorithm_combobox.currentIndex())
        search_value = self.search_name_textbox.text()

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
        if search_value != "":
            for i in range(len(show_logs)):
                if search_value in show_logs[i].name:
                    result_logs.append(show_logs[i])
        else:
            result_logs = show_logs

        for log in result_logs:
            self.addLog(self.model, log.key, log.name, log.created_date)