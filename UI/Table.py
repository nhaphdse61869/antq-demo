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
        self.remove_buttons = []
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
        self.tableWidget.setItem(row, 3, QTableWidgetItem(str(log.parameter["number_of_cluster"])))
        self.tableWidget.setItem(row, 4, QTableWidgetItem(log.algorithm))
        self.tableWidget.setItem(row, 5, QTableWidgetItem(log.created_date))
        self.tableWidget.setItem(row, 6, QTableWidgetItem(str(log.result["best_length"])))
        removeBtn = RemoveBtn(row, 'Remove', self.tableWidget, self.remove_log_function, self.remove_buttons)
        self.remove_buttons.append(removeBtn)
        self.tableWidget.setCellWidget(row, 7, removeBtn)
        self.tableWidget.setCellWidget(row, 8, DetailIcon(log.algorithm, log.parameter))

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class RemoveBtn(QPushButton):
    def __init__(self, row, name, table, remove_log_function, remove_buttons):
        super().__init__()
        self.setText(name)
        self.row = row
        self.remove_log_function = remove_log_function
        self.tableWidget = table
        self.remove_buttons = remove_buttons
        self.clicked.connect(self.removeLog)

    def removeLog(self):
        try:
            self.tableWidget.removeRow(self.row)
            self.remove_log_function(self.row)
            for i in range(self.row + 1, len(self.remove_buttons)):
                self.remove_buttons[i].row -= 1
            del self.remove_buttons[self.row]
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)

class DetailIcon(QLabel):
    def __init__(self, algorithm, param):
        super().__init__()
        path = os.path.dirname(os.path.abspath(__file__))
        self.setPixmap(QPixmap(os.path.join(path, 'information.png')))
        tool_tip = ""
        if algorithm == "AntQ":
            tool_tip += "Number of Iteration: {}\n".format(param["number_of_iteration"])
            tool_tip += "Number of Agent: {}\n".format(param["number_of_agent"])
            tool_tip += "Learning Rate: {}\n".format(param["learnning_rate"])
            tool_tip += "Discount Factor: {}\n".format(param["discount_factor"])
            tool_tip += "Delta: {}\n".format(param["delta"])
            tool_tip += "Beta: {}\n".format(param["beta"])
            tool_tip += "Delayed reinforcement: {}".format(param["delayed_reinforcement"])
        elif algorithm == "ACO":
            tool_tip += "Number of Iteration: {}\n".format(param["number_of_iteration"])
            tool_tip += "Number of Agent: {}\n".format(param["number_of_agent"])
            tool_tip += "Learning Rate: {}\n".format(param["learnning_rate"])
            tool_tip += "Discount Factor: {}\n".format(param["discount_factor"])
            tool_tip += "Delta: {}\n".format(param["delta"])
            tool_tip += "Beta: {}".format(param["beta"])
        elif algorithm == "Simulated Annealing":
            tool_tip += "Number of iteration: {}\n".format(param["number_of_iteration"])
            tool_tip += "T0: {}\n".format(param["t0"])
            tool_tip += "T min: {}\n".format(param["t_min"])
            tool_tip += "Beta: {}".format(param["beta"])
        self.setToolTip(tool_tip)

