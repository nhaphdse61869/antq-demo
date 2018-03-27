from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from UI.RouteFrame import *
from UI.ResultFrame import *


class GoogkeWP(QWidget):

    def __init__(self):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.botLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.botLayout)
        self.paramContainer = QGroupBox("Parameter")
        self.paramLayout = QFormLayout()
        self.paramContainer.setLayout(self.paramLayout)
        self.topLeftLayout = QVBoxLayout()
        self.paramContainer.setFixedHeight(400)
        self.paramContainer.setFixedWidth(200)
        self.topRightLayout = QVBoxLayout()
        self.topLeftLayout.addWidget(self.paramContainer)
        self.rsFrame = ResultFrame(self)
        self.viewLogListBtn = QPushButton("View Logs")
        self.showRoute = QPushButton("Run")
        self.topRightLayout.addWidget(self.rsFrame)
        self.topRightLayout.addWidget(self.showRoute)
        self.topLayout.addLayout(self.topLeftLayout)
        self.topLayout.addLayout(self.topRightLayout)
        self.routeFrame = RouteFrame()
        self.botLayout.addWidget(self.routeFrame)
        self.setLayout(self.mainLayout)

    def show_route_address(self, list_address, best_tour):
        self.routeFrame.clearAllRecords()
        for i in range(len(best_tour) - 1):
            from_add = list_address[best_tour[i]]
            to_add = list_address[best_tour[i + 1]]
            self.routeFrame.addRoute(self.routeFrame.model, from_add, to_add)

    def show_algorithm_parameter(self, parameter, algorithm):
        #Remove all row
        for i in range(self.paramLayout.count()):
            self.paramLayout.removeRow(i)

        #Add algorithm
        self.paramLayout.addRow(QLabel("Algorithm: "), QLabel(algorithm))
        if algorithm == "AntQ":
            self.paramLayout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.paramLayout.addRow(QLabel("Number of agent: "), QLabel(str(parameter["number_of_agent"])))
            self.paramLayout.addRow(QLabel("Learning rate: "), QLabel(str(parameter["learnning_rate"])))
            self.paramLayout.addRow(QLabel("Discount factor: "), QLabel(str(parameter["discount_factor"])))
            self.paramLayout.addRow(QLabel("Delta: "), QLabel(str(parameter["delta"])))
            self.paramLayout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))
            k_number = int(parameter["k_number"])
            if k_number <= 0:
                k_number = 1
            self.paramLayout.addRow(QLabel("Number of cluster: "), QLabel(str(k_number)))

        elif algorithm == "ACO":
            self.paramLayout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.paramLayout.addRow(QLabel("Number of agent: "), QLabel(str(parameter["number_of_agent"])))
            self.paramLayout.addRow(QLabel("Learning rate: "), QLabel(str(parameter["learnning_rate"])))
            self.paramLayout.addRow(QLabel("Discount factor: "), QLabel(str(parameter["discount_factor"])))
            self.paramLayout.addRow(QLabel("Delta: "), QLabel(str(parameter["delta"])))
            self.paramLayout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))
        elif algorithm == "Simulated Annealing":
            self.paramLayout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.paramLayout.addRow(QLabel("Initial T: "), QLabel(str(parameter["t0"])))
            self.paramLayout.addRow(QLabel("Minimum T: "), QLabel(str(parameter["t_min"])))
            self.paramLayout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))


