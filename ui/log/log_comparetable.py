import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class CompareLogTable(QWidget):
    def __init__(self, parent, removeLogFunction=None):
        super().__init__(parent)
        # Variable
        self.removeLogFunction = removeLogFunction
        self.remove_buttons = []

        # Main layout
        self.main_layout = QVBoxLayout()

        # Selected logs table
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(9)
        self.table_widget.setHorizontalHeaderLabels(("Key", "Name", "Number Of Point", "Number Of Cluster", "Algorithm",
                                                     "Created Date", "Best Length", "Action", ""))
        header = self.table_widget.horizontalHeader()
        header.setStyleSheet("::section{color:white;Background-color:rgb(128, 128, 128)}")
        header.setSectionResizeMode(7, QHeaderView.Stretch)
        header.resizeSection(1, 100)
        header.resizeSection(0, 50)
        header.resizeSection(3, 150)
        header.resizeSection(4, 180)
        header.resizeSection(5, 180)
        header.resizeSection(7, 125)
        header.resizeSection(8, 50)

        # Add to main layout
        self.main_layout.addWidget(self.table_widget)
        self.setLayout(self.main_layout)

    def addLogToTable(self, log):
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        self.table_widget.setItem(row, 0, QTableWidgetItem(str(log.key)))
        self.table_widget.setItem(row, 1, QTableWidgetItem(str(log.name)))
        self.table_widget.setItem(row, 2, QTableWidgetItem(str(log.number_of_point)))
        self.table_widget.setItem(row, 3, QTableWidgetItem(str(log.parameter["number_of_cluster"])))
        self.table_widget.setItem(row, 4, QTableWidgetItem(log.algorithm))
        self.table_widget.setItem(row, 5, QTableWidgetItem(log.created_date))
        self.table_widget.setItem(row, 6, QTableWidgetItem(str(log.result["best_length"])))
        remove_button = RemoveButton(row, self.table_widget, self.removeLogFunction, self.remove_buttons)
        self.remove_buttons.append(remove_button)
        self.table_widget.setCellWidget(row, 7, remove_button)
        self.table_widget.setCellWidget(row, 8, DetailIcon(log.algorithm, log.parameter))

class RemoveButton(QPushButton):
    def __init__(self, row, table, removeLogFunction, remove_buttons):
        super().__init__()
        self.setText("Remove")
        self.row = row
        self.removeLogFunction = removeLogFunction
        self.table_widget = table
        self.remove_buttons = remove_buttons
        self.clicked.connect(self.removeLog)

    def removeLog(self):
        try:
            self.table_widget.removeRow(self.row)
            self.removeLogFunction(self.row)
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
        self.setPixmap(QPixmap(os.path.join(path, 'detail_icon.png')))
        tool_tip = ""
        if algorithm == "AntQ":
            tool_tip += "Number of Iteration: {}\n".format(param["number_of_iteration"])
            tool_tip += "Number of Agent: {}\n".format(param["number_of_agent"])
            tool_tip += "Learning Rate: {}\n".format(param["learnning_rate"])
            tool_tip += "Discount Factor: {}\n".format(param["discount_factor"])
            tool_tip += "Balance Rate: {}\n".format(param["balance_rate"])
            tool_tip += "Delta: {}\n".format(param["delta"])
            tool_tip += "Beta: {}\n".format(param["beta"])
            tool_tip += "Delayed Reinforcement: {}".format(param["delayed_reinforcement"])
        elif algorithm == "ACO":
            tool_tip += "Number of Iteration: {}\n".format(param["number_of_iteration"])
            tool_tip += "Number of Agent: {}\n".format(param["number_of_agent"])
            tool_tip += "Residual Coefficient: {}\n".format(param["residual_coefficient"])
            tool_tip += "Intensity: {}\n".format(param["intensity"])
            tool_tip += "Alpha: {}\n".format(param["alpha"])
            tool_tip += "Beta: {}".format(param["beta"])
        elif algorithm == "Simulated Annealing":
            tool_tip += "Number of iteration: {}\n".format(param["number_of_iteration"])
            tool_tip += "T0: {}\n".format(param["t0"])
            tool_tip += "T min: {}\n".format(param["t_min"])
            tool_tip += "Beta: {}".format(param["beta"])
        self.setToolTip(tool_tip)

