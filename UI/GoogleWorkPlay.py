from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from UI.RouteFrame import *
from UI.ResultFrame import *

import traceback

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

    def show_route_address(self, list_address, clusters_point, best_tour, cluster_number=0):
        try:
            self.routeFrame.clearAllRecords()
            if cluster_number == 0:
                # Show All Route
                for n in range(len(best_tour)):
                    for i in range(len(best_tour[n]) - 1):
                        from_no = clusters_point[n][best_tour[n][i]]
                        from_add = list_address[from_no]
                        to_no = clusters_point[n][best_tour[n][i + 1]]
                        to_add = list_address[to_no]
                        self.routeFrame.addRoute(self.routeFrame.model, from_no + 1, from_add, to_no + 1, to_add, n + 1)
            else:
                cluster_number = cluster_number - 1
                for i in range(len(best_tour[cluster_number]) - 1):
                    from_no = clusters_point[cluster_number][best_tour[cluster_number][i]]
                    from_add = list_address[from_no]
                    to_no = clusters_point[cluster_number][best_tour[cluster_number][i + 1]]
                    to_add = list_address[to_no]
                    self.routeFrame.addRoute(self.routeFrame.model, from_no + 1, from_add, to_no + 1, to_add, cluster_number + 1)
        except:
            traceback.print_exc()

    def show_algorithm_parameter(self, parameter, algorithm):
        #Remove all row
        for i in range(self.paramLayout.count()):
            self.paramLayout.removeRow(0)

        #Add algorithm
        self.paramLayout.addRow(QLabel("Algorithm: "), QLabel(algorithm))
        if algorithm == "AntQ":
            self.paramLayout.addRow(QLabel("Number of cluster: "), QLabel(str(parameter["number_of_cluster"])))
            self.paramLayout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.paramLayout.addRow(QLabel("Number of agent: "), QLabel(str(parameter["number_of_agent"])))
            self.paramLayout.addRow(QLabel("Learning rate: "), QLabel(str(parameter["learnning_rate"])))
            self.paramLayout.addRow(QLabel("Discount factor: "), QLabel(str(parameter["discount_factor"])))
            self.paramLayout.addRow(QLabel("Delta: "), QLabel(str(parameter["delta"])))
            self.paramLayout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))
            k_number = int(parameter["number_of_cluster"])
            if k_number <= 0:
                k_number = 1
            self.paramLayout.addRow(QLabel("Number of cluster: "), QLabel(str(k_number)))

        elif algorithm == "ACO":
            self.paramLayout.addRow(QLabel("Number of cluster: "), QLabel(str(parameter["number_of_cluster"])))
            self.paramLayout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.paramLayout.addRow(QLabel("Number of agent: "), QLabel(str(parameter["number_of_agent"])))
            self.paramLayout.addRow(QLabel("Learning rate: "), QLabel(str(parameter["learnning_rate"])))
            self.paramLayout.addRow(QLabel("Discount factor: "), QLabel(str(parameter["discount_factor"])))
            self.paramLayout.addRow(QLabel("Delta: "), QLabel(str(parameter["delta"])))
            self.paramLayout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))
        elif algorithm == "Simulated Annealing":
            self.paramLayout.addRow(QLabel("Number of cluster: "), QLabel(str(parameter["number_of_cluster"])))
            self.paramLayout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.paramLayout.addRow(QLabel("Initial T: "), QLabel(str(parameter["t0"])))
            self.paramLayout.addRow(QLabel("Minimum T: "), QLabel(str(parameter["t_min"])))
            self.paramLayout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))


