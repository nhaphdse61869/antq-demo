from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
                          QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QSizePolicy, QHeaderView)
from ui.log.log_managepanel import *

import traceback

class GoogleWP(QWidget):

    def __init__(self):
        super().__init__()
        # Main layout
        self.main_layout = QVBoxLayout()

        # Sub layout
        self.top_layout = QHBoxLayout()
        self.bottom_layout = QVBoxLayout()

        # Top layout
        self.left_top_layout = QVBoxLayout()
        self.right_top_layout = QVBoxLayout()

        self.param_container = QGroupBox("Parameter")
        self.param_layout = QFormLayout()
        self.param_container.setLayout(self.param_layout)
        self.param_container.setFixedHeight(400)
        self.param_container.setFixedWidth(200)
        self.left_top_layout.addWidget(self.param_container)

        self.log_panel = LogPanel(self)
        self.show_route_button = QPushButton("Run")
        self.right_top_layout.addWidget(self.log_panel)
        self.right_top_layout.addWidget(self.show_route_button)

        self.top_layout.addLayout(self.left_top_layout)
        self.top_layout.addLayout(self.right_top_layout)

        # Bottom layout
        self.route_table = RouteTable()
        self.bottom_layout.addWidget(self.route_table)

        # Add to main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)

    def showRouteAddress(self, list_address, clusters_point, best_tour, cluster_number=0):
        try:
            self.route_table.clearAllRoute()
            if cluster_number == 0:
                # Show All Route
                for n in range(len(best_tour)):
                    for i in range(len(best_tour[n]) - 1):
                        from_no = clusters_point[n][best_tour[n][i]]
                        from_add = list_address[from_no]
                        to_no = clusters_point[n][best_tour[n][i + 1]]
                        to_add = list_address[to_no]
                        self.route_table.addRoute(self.route_table.model, from_no + 1, from_add, to_no + 1, to_add, n + 1)
            else:
                cluster_number = cluster_number - 1
                for i in range(len(best_tour[cluster_number]) - 1):
                    from_no = clusters_point[cluster_number][best_tour[cluster_number][i]]
                    from_add = list_address[from_no]
                    to_no = clusters_point[cluster_number][best_tour[cluster_number][i + 1]]
                    to_add = list_address[to_no]
                    self.route_table.addRoute(self.route_table.model, from_no + 1, from_add, to_no + 1, to_add, cluster_number + 1)
        except:
            traceback.print_exc()

    def showAlgorithmParameter(self, parameter, algorithm):
        #Remove all row
        for i in range(self.param_layout.count()):
            self.param_layout.removeRow(0)

        #Add algorithm
        self.param_layout.addRow(QLabel("Algorithm: "), QLabel(algorithm))
        if algorithm == "AntQ":
            self.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(parameter["number_of_cluster"])))
            self.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.param_layout.addRow(QLabel("Number of agent: "), QLabel(str(parameter["number_of_agent"])))
            self.param_layout.addRow(QLabel("Learning rate: "), QLabel(str(parameter["learnning_rate"])))
            self.param_layout.addRow(QLabel("Discount factor: "), QLabel(str(parameter["discount_factor"])))
            self.param_layout.addRow(QLabel("Balance rate: "), QLabel(str(parameter["balance_rate"])))
            self.param_layout.addRow(QLabel("Delta: "), QLabel(str(parameter["delta"])))
            self.param_layout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))
            k_number = int(parameter["number_of_cluster"])
            if k_number <= 0:
                k_number = 1
            self.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(k_number)))
        elif algorithm == "ACO":
            self.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(parameter["number_of_cluster"])))
            self.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.param_layout.addRow(QLabel("Number of agent: "), QLabel(str(parameter["number_of_agent"])))
            self.param_layout.addRow(QLabel("Residual Coefficient: "), QLabel(str(parameter["residual_coefficient"])))
            self.param_layout.addRow(QLabel("Intensity: "), QLabel(str(parameter["intensity"])))
            self.param_layout.addRow(QLabel("Alpha: "), QLabel(str(parameter["alpha"])))
            self.param_layout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))
        elif algorithm == "Simulated Annealing":
            self.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(parameter["number_of_cluster"])))
            self.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(parameter["number_of_iteration"])))
            self.param_layout.addRow(QLabel("Initial T: "), QLabel(str(parameter["t0"])))
            self.param_layout.addRow(QLabel("Minimum T: "), QLabel(str(parameter["t_min"])))
            self.param_layout.addRow(QLabel("Beta: "), QLabel(str(parameter["beta"])))

class RouteTable(QWidget):
    NO1, FROM, NO2, TO, CLUSTER = range(5)

    def __init__(self):
        super().__init__()
        # Main layout
        main_layout = QVBoxLayout()

        # Sub layout
        self.cluster_combobox = QComboBox()
        self.table_container = QGroupBox("Result")

        # Route Table
        self.table = QTreeView()
        self.table.setRootIsDecorated(False)
        self.table.setAlternatingRowColors(True)

        self.model = QStandardItemModel(0, 5, self)
        self.model.setHeaderData(self.NO1, Qt.Horizontal, "No")
        self.model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        self.model.setHeaderData(self.NO2, Qt.Horizontal, "No")
        self.model.setHeaderData(self.TO, Qt.Horizontal, "To")
        self.model.setHeaderData(self.CLUSTER, Qt.Horizontal, "Cluster number")

        self.table.setModel(self.model)
        table_header = self.table.header()
        table_header.resizeSection(0, 25)
        table_header.resizeSection(1, 190)
        table_header.resizeSection(2, 25)
        table_header.resizeSection(3, 190)

        table_container_layout = QHBoxLayout()
        table_container_layout.addWidget(self.table)
        self.table_container.setLayout(table_container_layout)

        # Add to main layout
        main_layout.addWidget(self.cluster_combobox)
        main_layout.addWidget(self.table_container)
        self.setLayout(main_layout)

    def addRoute(self, model, from_no, from_route, to_no, to_route, cluster_number):
        root = self.table.model()
        n = root.rowCount()
        model.insertRow(n)
        model.setData(model.index(n, self.NO1), from_no)
        model.setData(model.index(n, self.FROM), from_route)
        model.setData(model.index(n, self.NO2), to_no)
        model.setData(model.index(n, self.TO), to_route)
        model.setData(model.index(n, self.CLUSTER), cluster_number)

    def clearAllRoute(self):
        root = self.table.model()
        root.removeRows(0, root.rowCount())