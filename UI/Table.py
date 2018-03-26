from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class TableLog(QWidget):

    def __init__(self, parent, remove_log_function=None):
        super().__init__(parent)
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.remove_log_function = remove_log_function
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
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(("Key","Name","NumberOfPoint","Algorithm","CreatedDate","Parameter","Action"))

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.resizeSection(1, 100)
        header.resizeSection(0, 50)
        header.resizeSection(5, 200)
        # table selection change

    def addTableItem(self, log):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(str(log.key)))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(str(log.name)))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(str(log.number_of_point)))
        self.tableWidget.setItem(row, 3, QTableWidgetItem(log.algorithm))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(log.created_date))
        self.tableWidget.setItem(row, 5, QTableWidgetItem(str(log.parameter)))
        removeBtn = RemoveBtn(row, 'Remove', self.tableWidget, self.remove_log_function)
        self.tableWidget.setCellWidget(row, 6, removeBtn)
        #self.tableWidget.setItem(row, 6, '')
        #self.tableWidget.setItem(row, 7, '')
        #self.tableWidget.setItem(row, 8, '')

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class RemoveBtn(QPushButton):
    def __init__(self, row, name, table, remove_log_function):
        super().__init__()
        self.setText(name)
        self.row = row
        self.remove_log_function = remove_log_function
        self.tableWidget = table
        self.clicked.connect(self.removeLog)

    def removeLog(self):
        try:
            self.tableWidget.removeRow(self.row)
            self.remove_log_function(self.row)
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)