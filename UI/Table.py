import os
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
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels(("Key","Name","Number Of Point","Number Of Cluster","Algorithm",
                                                    "Created Date","Best Length","Action",""))

        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("::section{Background-color:rgb(128, 128, 128)}")
        header.setSectionResizeMode(7, QHeaderView.Stretch)
        header.resizeSection(1, 100)
        header.resizeSection(0, 50)
        header.resizeSection(3, 150)
        header.resizeSection(4, 180)
        header.resizeSection(5, 180)
        header.resizeSection(7, 125)
        header.resizeSection(8, 50)
        # table selection change

    def addTableItem(self, log):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(str(log.key)))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(str(log.name)))
        self.tableWidget.setItem(row, 2, QTableWidgetItem(str(log.number_of_point)))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(log.algorithm))
        self.tableWidget.setItem(row, 5, QTableWidgetItem(log.created_date))
        #self.tableWidget.setItem(row, 5, QTableWidgetItem(str(log.parameter)))
        removeBtn = RemoveBtn(row, 'Remove', self.tableWidget, self.remove_log_function)
        self.tableWidget.setCellWidget(row, 7, removeBtn)
        self.tableWidget.setCellWidget(row, 8, DetailIcon(str(log.parameter)))

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

class DetailIcon(QLabel):
    def __init__(self, param):
        super().__init__()
        path = os.path.dirname(os.path.abspath(__file__))
        self.setPixmap(QPixmap(os.path.join(path, 'information.png')))
        self.setToolTip(param)

