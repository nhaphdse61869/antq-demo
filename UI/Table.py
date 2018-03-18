from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class TableLog(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(("Key","Name","NumberOfPoint","Algorithm","CreatedDate","Parameter","Dataset","Result"))

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.resizeSection(1, 100)
        header.resizeSection(0, 50)
        header.resizeSection(5, 200)
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    def addTableItem(self, item):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.filesTable.setItem(row, 0, '')
        self.filesTable.setItem(row, 1, '')
        self.filesTable.setItem(row, 2, '')
        self.filesTable.setItem(row, 3, '')
        self.filesTable.setItem(row, 4, '')
        self.filesTable.setItem(row, 5, '')
        self.filesTable.setItem(row, 6, '')
        self.filesTable.setItem(row, 7, '')
        self.filesTable.setItem(row, 8, '')

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())