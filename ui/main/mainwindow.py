from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QStandardItemModel, QColor

import sys
import json
import codecs
import datetime
import time
import traceback
from queue import Queue
from threading import Thread

from algorithm.aco import ACOGraph,ACO
from algorithm.cluster_antq import AntQClustering
from algorithm.sa import SimAnneal
from qgmap.common import QGoogleMap
from ui.figure import AnimationGraphCanvas
from ui.main.wp_googlemap import GoogleMapWP
from ui.main.wp_graph import GraphWP
from util.dataset import TSPFileReader, ATSPReader, GMapDataReader
from util.log import LogIO, Log



class MainWindow(QWidget):
    save_log_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # General Parameters
        self.current_algorithm_tab = 0
        self.current_algorithm = "AntQ"
        self.number_of_cluster = 1

        # Antq parameters
        self.antq_global_best = True
        self.antq_delta = 1
        self.antq_beta = 2
        self.antq_number_of_iteration = 200
        self.antq_number_of_agent = 2
        self.antq_learning_rate = 0.1
        self.antq_discount_factor = 0.3
        self.antq_balance_rate = 0.9

        # ACO parameters
        self.aco_number_of_iteration = 200
        self.aco_number_of_agent = 1
        self.aco_residual_coefficient = 1
        self.aco_intensity = 1
        self.aco_beta = 1
        self.aco_alpha = 2

        #SA parameters
        self.sa_beta = 1
        self.sa_T0 = 100
        self.sa_T_min = 0
        self.sa_number_of_iteration = 200

        # Graph parameter
        self.best_tour = []
        self.list_point = []
        self.dist_matrix = []
        self.list_address = []
        self.log_io = LogIO()
        self.result_log = None
        self.algorithm_thread = None

        # Google map parameter
        self.google_map_selected_log = None

        # Initial Main Window
        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.setGeometry(0, 40, 0, 0)
        self.resize(2600, 0)

        # Left layout
        self.left_layout = QTabWidget()
        self.google_map_tab = QWidget()
        self.graph_tab = QWidget()

        # Google Maps container
        self.gmap = QGoogleMap(self)
        self.gmap.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding)
        self.gmap.waitUntilReady()
        self.gmap.setZoom(15)
        # Center at HCM city
        self.gmap.centerAt(10.857200, 106.628487)

        self.google_map_tab.layout = QVBoxLayout()
        self.google_map_tab.setLayout(self.google_map_tab.layout)
        self.google_map_tab.layout.addWidget(self.gmap)

        # Graph
        self.graph = AnimationGraphCanvas()
        self.graph_tab.layout = QVBoxLayout()
        self.graph_tab.setLayout(self.graph_tab.layout)
        self.graph_tab.layout.addWidget(self.graph)
        self.graph_tab.layout.setSpacing(0)

        self.left_layout.addTab(self.graph_tab, "Graph")
        self.left_layout.addTab(self.google_map_tab, "Google Map")

        # Right layout
        self.right_layout = QStackedWidget(self)
        self.graph_WP = GraphWP()
        self.google_map_WP = GoogleMapWP()

        self.right_layout.addWidget(self.graph_WP)
        self.right_layout.addWidget(self.google_map_WP)

        # Add to main layout
        self.main_layout.addWidget(self.left_layout)
        self.main_layout.addWidget(self.right_layout)

        # Connect signals
        self.save_log_signal.connect(self.saveLog)
        self.left_layout.tabBarClicked.connect(self.checkGoogleTab)
        self.graph_WP.run_button.clicked.connect(self.runAlgorithm)
        self.graph_WP.apply_button.clicked.connect(self.applyParameter)
        self.graph_WP.generate_button.clicked.connect(self.openFileDialog)
        self.graph_WP.algorithm_tabs.tabBarClicked.connect(self.checkCurrentTab)
        self.google_map_WP.show_route_button.clicked.connect(self.runLogGoogleMap)
        self.google_map_WP.route_table.cluster_combobox.currentIndexChanged.connect(self.changeClusterGoogleMap)

        #Show current parameter
        self.showCurrentParameter()

    def checkGoogleTab(self, pos):
        if pos == 1:
            self.google_map_WP.log_panel.loadListLog()
            self.right_layout.setCurrentIndex(1)
        else:
            self.right_layout.setCurrentIndex(0)

    def checkCurrentTab(self, pos):
        self.current_algorithm_tab = pos
        if pos == 2:
            try:
                self.graph_WP.chart_tabs.removeTab(2)
                self.graph_WP.chart_tabs.removeTab(1)
                self.current_algorithm = "Simulated Annealing"
            except:
                traceback.print_exc()
        elif self.graph_WP.chart_tabs.count() == 1 and pos == 0 :
            self.graph_WP.chart_tabs.addTab(self.graph_WP.chart2_tab, "Mean Length")
            self.graph_WP.chart_tabs.addTab(self.graph_WP.chart3_tab, "Variance Length")
            self.current_algorithm = "AntQ"
        elif self.graph_WP.chart_tabs.count() == 1 and pos == 1 :
            self.graph_WP.chart_tabs.addTab(self.graph_WP.chart2_tab, "Mean Length")
            self.graph_WP.chart_tabs.addTab(self.graph_WP.chart3_tab, "Variance Length")
            self.current_algorithm = "ACO"

    def openFileDialog(self):
        try:
            open = OpenTSPFileDialog(visualize_graph=self.graph)
            open.show()

            # Get data
            self.dist_matrix = open.dist_matrix
            self.list_point = open.list_point
            self.list_address = open.list_address
            self.graph_WP.aco_tab.num_agent_slider.changeMax(len(self.list_point))
            self.graph_WP.antq_tab.num_agent_slider.changeMax(len(self.list_point))
        except:
            traceback.print_exc()

    def showCurrentParameter(self):
        # Clear layout
        for i in range(self.graph_WP.param_layout.count()):
            self.graph_WP.param_layout.removeRow(0)
        self.graph_WP.param_layout.update()

        # Show AntQ Parameter
        if self.current_algorithm == "AntQ":
            self.graph_WP.param_layout.addRow(QLabel("Algorithm: "), QLabel("AntQ"))
            self.graph_WP.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(self.number_of_cluster)))
            self.graph_WP.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(self.antq_number_of_iteration)))
            self.graph_WP.param_layout.addRow(QLabel("Number of agent: "), QLabel(str(self.antq_number_of_agent)))
            self.graph_WP.param_layout.addRow(QLabel("Learning rate: "), QLabel(str(self.antq_learning_rate)))
            self.graph_WP.param_layout.addRow(QLabel("Discount factor: "), QLabel(str(self.antq_discount_factor)))
            self.graph_WP.param_layout.addRow(QLabel("Balance rate: "), QLabel(str(self.antq_balance_rate)))
            self.graph_WP.param_layout.addRow(QLabel("Delta: "), QLabel(str(self.antq_delta)))
            self.graph_WP.param_layout.addRow(QLabel("Beta: "), QLabel(str(self.antq_beta)))
            dr = "Iter"
            if self.antq_global_best:
                dr = "Global"
            self.graph_WP.param_layout.addRow(QLabel("DR: "), QLabel(dr))

        # Show ACO Parameter
        elif self.current_algorithm == "ACO":
            self.graph_WP.param_layout.addRow(QLabel("Algorithm: "), QLabel("ACO"))
            self.graph_WP.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(self.number_of_cluster)))
            self.graph_WP.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(self.aco_number_of_iteration)))
            self.graph_WP.param_layout.addRow(QLabel("Number of agent: "), QLabel(str(self.aco_number_of_agent)))
            self.graph_WP.param_layout.addRow(QLabel("Residual coefficient: "), QLabel(str(self.aco_residual_coefficient)))
            self.graph_WP.param_layout.addRow(QLabel("Intensity: "), QLabel(str(self.aco_intensity)))
            self.graph_WP.param_layout.addRow(QLabel("Alpha: "), QLabel(str(self.aco_alpha)))
            self.graph_WP.param_layout.addRow(QLabel("Beta: "), QLabel(str(self.aco_beta)))

        # Show SA Parameter
        elif self.current_algorithm == "Simulated Annealing":
            self.graph_WP.param_layout.addRow(QLabel("Algorithm: "), QLabel("SA"))
            self.graph_WP.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(self.number_of_cluster)))
            self.graph_WP.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(self.sa_number_of_iteration)))
            self.graph_WP.param_layout.addRow(QLabel("Beta: "), QLabel(str(self.sa_beta)))
            self.graph_WP.param_layout.addRow(QLabel("T_0: "), QLabel(str(self.sa_T0)))
            self.graph_WP.param_layout.addRow(QLabel("T_min: "), QLabel(str(self.sa_T_min)))

    def applyParameter(self):
        try:
            qm = QMessageBox()
            reply = qm.question(self, 'Message',
                                'Do you want to apply new parameter?', QMessageBox.Ok, QMessageBox.Cancel)

            if reply == QMessageBox.Ok:
                self.number_of_cluster = 1
                # Apply AntQ parameter
                if self.current_algorithm_tab == 0:
                    self.current_algorithm = "AntQ"
                    self.antq_delta = self.graph_WP.antq_tab.delta_spin.value()
                    self.antq_beta = self.graph_WP.antq_tab.beta_spin.value()
                    self.antq_number_of_iteration = self.graph_WP.antq_tab.iteration_spin.value()
                    self.antq_learning_rate = self.graph_WP.antq_tab.learning_rate_spin.value() / 100
                    self.antq_discount_factor = self.graph_WP.antq_tab.discount_factor_spin.value() / 100
                    self.antq_balance_rate = self.graph_WP.antq_tab.balance_rate_spin.value() / 100
                    self.antq_number_of_agent = self.graph_WP.antq_tab.num_agent_slider.k
                    self.number_of_cluster = self.graph_WP.antq_tab.k_num_spin.value()
                    dr = self.graph_WP.antq_tab.dr_combobox.currentIndex()
                    self.antq_global_best = True
                    if dr == 0:
                        self.antq_global_best = False

                # Apply ACO parameter
                elif self.current_algorithm_tab == 1:
                    self.current_algorithm = "ACO"
                    self.aco_alpha = self.graph_WP.aco_tab.alpha_spin.value()
                    self.aco_beta = self.graph_WP.aco_tab.beta_spin.value()
                    self.aco_number_of_iteration = self.graph_WP.aco_tab.iteration_spin.value()
                    self.aco_residual_coefficient = self.graph_WP.aco_tab.residual_coefficient_spin.value() / 100
                    self.aco_intensity = self.graph_WP.aco_tab.intensity_spin.value() / 100
                    self.aco_number_of_agent = self.graph_WP.aco_tab.num_agent_slider.k

                # Apply SA Parameter
                elif self.current_algorithm_tab == 2:
                    self.current_algorithm = "Simulated Annealing"
                    self.sa_T0 = self.graph_WP.sa_tab.temper_init_spin.value()
                    self.sa_T_min = self.graph_WP.sa_tab.temper_end_spin.value()
                    self.sa_beta = self.graph_WP.sa_tab.beta_spin.value() / 100
                    self.sa_number_of_iteration = self.graph_WP.sa_tab.iteration_spin.value()

                self.resetGraph()
                self.showCurrentParameter()
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)

    # Implement Algorithm
    def runAlgorithm(self):
        if len(self.list_point) < 2:
            qm = QMessageBox
            qm.information(self,"", "Atleast two points!")
        else :
            # Start draw chart thread
            self.algorithm_result = Queue()
            try:
                self.result_handler = Thread(target=self.drawChart)
                self.result_handler.start()
            except:
                traceback.print_exc()

            # Initial AntQ Algorithm
            if self.current_algorithm == "AntQ":
                try:
                    self.algorithm_thread = AntQClustering(self.list_point, self.dist_matrix,
                                                           self.number_of_cluster,
                                                           self.antq_number_of_agent,
                                                           self.antq_number_of_iteration,
                                                           self.antq_learning_rate,
                                                           self.antq_discount_factor,
                                                           self.antq_delta,
                                                           self.antq_beta,
                                                           q0=self.antq_balance_rate,
                                                           global_best=self.antq_global_best, result_queue=self.algorithm_result)
                except:
                    traceback.print_exc()

            # Initial ACO Algorithm
            elif self.current_algorithm == "ACO":
                try:
                    self.aco_graph = ACOGraph(self.dist_matrix, len(self.dist_matrix))
                    self.algorithm_thread = ACO(self.aco_number_of_agent,
                                                self.aco_number_of_iteration,
                                                self.aco_graph,
                                                self.aco_alpha,
                                                self.aco_beta,
                                                self.aco_residual_coefficient,
                                                self.aco_intensity,
                                                result_queue=self.algorithm_result)
                except:
                    traceback.print_exc()

            # Initial SA Algorithm
            elif self.current_algorithm == "Simulated Annealing":
                self.algorithm_thread = SimAnneal(self.dist_matrix,
                                                  T=self.sa_T0,
                                                  alpha=self.sa_beta,
                                                  stopping_T=self.sa_T_min,
                                                  stopping_iter=self.sa_number_of_iteration,
                                                  result_queue=self.algorithm_result)

            # Visualize cluster
            self.graph.clearGraph()
            self.graph.updateCluster(self.algorithm_thread.clusters_point)

            # Run algorithm
            self.algorithm_thread.run_finished.connect(self.algorithmFinished)
            self.algorithm_thread.start()

    def drawChart(self):
        try:
            prev_best_length = sys.maxsize
            while True:
                while self.graph.draw_done == False:
                    time.sleep(0.1)

                result = self.algorithm_result.get()
                if result != None:
                    iteration = result["iteration"]
                    best_tour_len = result["best_tour_len"]
                    best_tour = result["best_tour"]
                    if self.current_algorithm == "AntQ" or self.current_algorithm == "ACO":
                        iter_avg = result["iter_avg"]
                        iter_deviation = result["iter_deviation"]
                        # Draw chart
                        if iteration == 0:
                            pass
                            # add new lines
                            self.graph_WP.best_length_chart.addNewLine(iteration, best_tour_len)
                            self.graph_WP.mean_length_chart.addNewLine(iteration, iter_avg)
                            self.graph_WP.st_deviation_chart.addNewLine(iteration, iter_deviation)
                        else:
                            pass
                            # update lines
                            self.graph_WP.best_length_chart.updateNewestLine(iteration, best_tour_len)
                            self.graph_WP.mean_length_chart.updateNewestLine(iteration, iter_avg)
                            self.graph_WP.st_deviation_chart.updateNewestLine(iteration, iter_deviation)
                        if self.current_algorithm == "ACO":
                            best_tour = [best_tour]
                    elif self.current_algorithm == "Simulated Annealing":
                        # Simulated Annealing
                        best_tour = [best_tour]
                        # Draw chart
                        if iteration == 1:
                            # add new lines
                            self.graph_WP.best_length_chart.addNewLine(iteration, best_tour_len)
                        else:
                            # update lines
                            self.graph_WP.best_length_chart.updateNewestLine(iteration, best_tour_len)

                    # Draw Graph
                    if prev_best_length > best_tour_len:
                        prev_best_length = best_tour_len
                        self.graph.updateClusterGraph(best_tour)
                else:
                    self.save_log_signal.emit()
                    break
        except:
            traceback.print_exc()

    @pyqtSlot()
    def algorithmFinished(self):
        try:
            # Create Log object
            key = self.log_io.getNewLogKey()
            name = key
            number_of_point = len(self.list_point)
            created_date = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            parameter = {}
            parameter["number_of_cluster"] = self.number_of_cluster
            dataset = {}
            dataset["list_points"] = self.list_point
            dataset["distance_matrix"] = self.dist_matrix
            dataset["list_address"] = self.list_address
            result = {}

            if self.current_algorithm == "AntQ":
                # AntQ
                dr = "Iteration best"
                if self.antq_global_best:
                    dr = "Global best"
                parameter["delayed_reinforcement"] = dr
                parameter["number_of_iteration"] = self.antq_number_of_iteration
                parameter["number_of_agent"] = self.antq_number_of_agent
                parameter["learnning_rate"] = self.antq_learning_rate
                parameter["discount_factor"] = self.antq_discount_factor
                parameter["balance_rate"] = self.antq_balance_rate
                parameter["delta"] = self.antq_delta
                parameter["beta"] = self.antq_beta
                result["clusters_point"] = self.algorithm_thread.clusters_point
                result["best_tour"] = self.algorithm_thread.clusters_best_tour
                result["best_length"] = self.algorithm_thread.best_len
                result["list_iteration"] = list(range(self.antq_number_of_iteration))
                result["list_best_tour"] = self.algorithm_thread.list_clusters_best_tour
                result["list_best_len"] = self.algorithm_thread.list_avg_best_length
                result["list_avg"] = self.algorithm_thread.list_avg_mean_length
                result["list_deviation"] = self.algorithm_thread.list_avg_dev

            elif self.current_algorithm == "ACO":
                # ACO
                parameter["number_of_iteration"] = self.aco_number_of_iteration
                parameter["number_of_agent"] = self.aco_number_of_agent
                parameter["residual_coefficient"] = self.aco_residual_coefficient
                parameter["intensity"] = self.aco_intensity
                parameter["alpha"] = self.aco_alpha
                parameter["beta"] = self.aco_beta
                result["clusters_point"] = self.algorithm_thread.clusters_point
                result["best_tour"] = [self.algorithm_thread.global_best_tour]
                result["best_length"] = self.algorithm_thread.global_best_tour_len
                result["list_iteration"] = list(range(self.aco_number_of_iteration))
                result["list_best_tour"] = self.algorithm_thread.list_best_tour
                result["list_best_len"] = self.algorithm_thread.list_best_len
                result["list_avg"] = self.algorithm_thread.list_avg
                result["list_deviation"] = self.algorithm_thread.list_dev

            elif self.current_algorithm == "Simulated Annealing":
                # Simulated Annealing
                parameter["t0"] = self.sa_T0
                parameter["t_min"] = self.sa_T_min
                parameter["beta"] = self.sa_beta
                parameter["number_of_iteration"] = self.sa_number_of_iteration
                result["clusters_point"] = self.algorithm_thread.clusters_point
                result["best_tour"] = [self.algorithm_thread.best_tour]
                result["best_length"] = self.algorithm_thread.best_tour_len
                result["list_iteration"] = list(range(self.sa_number_of_iteration))
                result["list_best_tour"] = self.algorithm_thread.best_tours
                result["list_best_len"] = self.algorithm_thread.best_lens

            # Create log object
            self.result_log = Log(key=key, name=name, algorithm=self.current_algorithm,
                                  number_of_point=number_of_point, created_date=created_date,
                                  parameter=parameter, dataset=dataset, result=result)

            self.algorithm_result.put(None)
        except:
            traceback.print_exc()

    @pyqtSlot()
    def saveLog(self):
        qm = QMessageBox()
        reply = qm.question(self, 'Message',
                  'Do you wan to save Log?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            name, ok = QInputDialog.getText(self, 'Create Log', 'Log Name:')
            if ok:
                if self.result_log != None:
                    self.result_log.name = name
                    self.log_io.addNewLog(self.result_log)
                    self.result_log = None

    def enableSpinBox(self):
        #global Knum, checkK
        if self.graph_WP.antq_tab.checkK.isChecked() == True:
            self.graph_WP.antq_tab.Knum.setDisabled(False)
        else:
            self.graph_WP.antq_tab.Knum.setDisabled(True)

    def resetGraph(self):
        self.graph_WP.best_length_chart.clearChart()
        self.graph_WP.mean_length_chart.clearChart()
        self.graph_WP.st_deviation_chart.clearChart()
        self.result_log = None

    def runLogGoogleMap(self):
        try:
            log_key = self.google_map_WP.log_panel.currentKey
            self.google_map_selected_log = self.log_io.getLog(int(log_key))
            if len(self.google_map_selected_log.dataset["list_address"]) > 0:
                #Get log parameter
                clusters_point = self.google_map_selected_log.result["clusters_point"]
                list_point = self.google_map_selected_log.dataset["list_points"]
                list_address = self.google_map_selected_log.dataset["list_address"]
                best_tour = self.google_map_selected_log.result["best_tour"]
                parameter = self.google_map_selected_log.parameter
                algorithm = self.google_map_selected_log.algorithm

                # Add marker
                for n in range(len(clusters_point)):
                    for i in range(len(clusters_point[n])):
                        point = list_point[clusters_point[n][i]]
                        lat = point[0]
                        long = point[1]
                        label = clusters_point[n][i] + 1

                        self.gmap.addMarker(str(label), lat, long, n, **dict(
                            title="Click me"
                        ))

                # Show all cluster route
                for n in range(len(clusters_point)):
                    #Get list point of cluster
                    cluster_point = [0 for x in range(len(clusters_point[n]))]
                    for i in range(len(clusters_point[n])):
                        cluster_point[i] = list_point[clusters_point[n][i]]

                    #Return to start point
                    if (len(best_tour[n]) > 1):
                        best_tour[n].append(best_tour[n][0])

                    #Show best tour of cluster
                    self.gmap.createRoute(cluster_point, best_tour[n], n)

                # Show all cluster address
                self.google_map_WP.showRouteAddress(list_address, clusters_point, best_tour, 0)

                # Show parameter
                self.google_map_WP.showAlgorithmParameter(parameter, algorithm)

                #Add cluster number to combobox
                self.google_map_WP.route_table.cluster_combobox.clear()
                self.google_map_WP.route_table.cluster_combobox.addItem("All")
                for i in range(len(clusters_point)):
                    self.google_map_WP.route_table.cluster_combobox.addItem("Cluster {}".format(i + 1))

            else:
                error = QMessageBox()
                error.critical(self, "Error", "Dataset of log isn't Google Map dataset", QMessageBox.Ok)
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)

    def changeClusterGoogleMap(self, pos):
        if pos > 0:
            try:
                cluster_index = pos - 1
                clusters_point = self.google_map_selected_log.result["clusters_point"]
                list_point = self.google_map_selected_log.dataset["list_points"]
                list_address = self.google_map_selected_log.dataset["list_address"]
                best_tour = self.google_map_selected_log.result["best_tour"]

                # Clear all marker and route
                self.gmap.clearAllRoute()
                self.gmap.clearAllMarker()

                # Add marker
                for i in range(len(clusters_point[cluster_index])):
                    point = list_point[clusters_point[cluster_index][i]]
                    lat = point[0]
                    long = point[1]
                    label = clusters_point[cluster_index][i] + 1

                    self.gmap.addMarker(str(label), lat, long, cluster_index, **dict(
                        title="Click me"
                    ))

                # Show all cluster route
                # Get list point of cluster
                cluster_point = [0 for x in range(len(clusters_point[cluster_index]))]
                for i in range(len(clusters_point[cluster_index])):
                    cluster_point[i] = list_point[clusters_point[cluster_index][i]]

                # Show best tour of cluster
                self.gmap.createRoute(cluster_point, best_tour[cluster_index], cluster_index)

                # Show route address
                self.google_map_WP.showRouteAddress(list_address, clusters_point, best_tour, pos)
            except:
                traceback.print_exc()

class OpenTSPFileDialog(QWidget):

    def __init__(self, visualize_graph = None):
        super().__init__()
        self.setGeometry(10, 10, 640, 480)

        self.list_point = []
        self.list_address = []
        self.dist_matrix = []
        self.is_googlemap = False
        self.visualize_graph = visualize_graph

        self.openTSPFileDialog()

    def openTSPFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            try:
                self.is_googlemap = False
                self.visualize_graph.clearGraph()
                if fileName.lower().endswith('.atsp'):
                    # Read atsp file
                    reader = ATSPReader(fileName.strip())
                    self.list_point = reader.cities_tups
                    self.dist_matrix = reader.dist_matrix

                    # Draw graph
                    self.visualize_graph.initCoordData(self.list_point)

                elif fileName.lower().endswith('.tsp'):
                    # Reader tsp file
                    reader = TSPFileReader(fileName.strip())
                    self.list_point = reader.cities_tups
                    self.dist_matrix = reader.dist_matrix

                    self.visualize_graph.initCoordData(self.list_point)

                elif fileName.lower().endswith('.json'):
                    self.is_googlemap = True
                    # Reader tsp file
                    reader = GMapDataReader(fileName.strip())
                    self.list_point = reader.cities_tups
                    self.dist_matrix = reader.dist_matrix
                    self.list_address = reader.list_address
                    # Draw graph
                    try:
                        self.visualize_graph.initCoordData(self.list_point)
                    except:
                        traceback.print_exc()
                if len(self.list_point) < 1:
                    qm = QMessageBox
                    qm.critical(self.parent(), "", "Wrong file!")
            except:
                traceback.print_exc()
                self.visualize_graph.clearGraph()
                self.list_point = []
                self.dist_matrix = []
                qm = QMessageBox
                qm.critical(self.parent(), "", "Wrong file!")

