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
from ui.main.wp_googlemap import GoogleWP
from ui.main.wp_graph import GraphWP
from util.dataset import TSPFileReader, ATSPReader, GMapDataReader
from util.log import LogIO, Log



class MainWindow(QWidget):
    save_log_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Algorithm default parameters
        self.global_best = True
        self.k_number = 1
        self.curTab = 0
        self.delta = 1
        self.beta = 2
        self.Ite = 200
        self.numAgents = 2
        self.LR = 10
        self.DF = 30
        self.BR = 90
        self.T_0 = 0
        self.T_min = 0
        self.algorithm = "AntQ"

        # Graph parameter
        self.best_tour = []
        self.list_point = []
        self.dist_matrix = []
        self.list_address = []
        self.numMarker = 0
        self.log_io = LogIO()
        self.logging = None
        self.algEx = None

        # Google map parameter
        self.google_map_selected_log = None

        # Main layout
        self.mainLayout = QHBoxLayout(self)
        self.setGeometry(0, 40, 0, 0)
        self.resize(2600, 0)

        # Left layout
        self.leftLayout = QTabWidget()
        self.tabGM = QWidget()
        self.tabGraph = QWidget()

        # Google Maps container
        self.gmap = QGoogleMap(self)
        self.gmap.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding)
        self.gmap.waitUntilReady()
        self.gmap.setZoom(15)
        # Center at HCM city
        self.gmap.centerAt(10.857200, 106.628487)

        self.tabGM.layout = QVBoxLayout()
        self.tabGM.setLayout(self.tabGM.layout)
        self.tabGM.layout.addWidget(self.gmap)

        # Graph
        self.graph = AnimationGraphCanvas()
        self.tabGraph.layout = QVBoxLayout()
        self.tabGraph.setLayout(self.tabGraph.layout)
        self.tabGraph.layout.addWidget(self.graph)
        self.tabGraph.layout.setSpacing(0)

        self.leftLayout.addTab(self.tabGraph, "Graph")
        self.leftLayout.addTab(self.tabGM, "Google Map")

        self.leftLayout.tabBarClicked.connect(self.checkGoogleTab)

        # Right layout
        self.rightLayout = QStackedWidget(self)
        self.graphWP = GraphWP()
        self.googleWP = GoogleWP()

        self.rightLayout.addWidget(self.graphWP)
        self.rightLayout.addWidget(self.googleWP)

        self.graphWP.run_button.clicked.connect(self.runAlgorithm)
        self.graphWP.apply_button.clicked.connect(self.applyPara)
        self.graphWP.generate_button.clicked.connect(self.openFileDialog)
        self.graphWP.algorithm_tabs.tabBarClicked.connect(self.checkCurrentTab)
        self.googleWP.show_route_button.clicked.connect(self.run_google_map_log)
        self.googleWP.route_table.cluster_combobox.currentIndexChanged.connect(self.google_map_change_cluster)

        # Add to main layout
        self.mainLayout.addWidget(self.leftLayout)
        self.mainLayout.addWidget(self.rightLayout)
        self.save_log_signal.connect(self.saveLog)
        self.showCurrentParameter()

    def checkGoogleTab(self, pos):
        if pos == 1:
            self.googleWP.log_panel.loadListLog()
            self.rightLayout.setCurrentIndex(1)
        else:
            self.rightLayout.setCurrentIndex(0)

    def checkCurrentTab(self, pos):
        self.curTab = pos
        if pos == 2:
            try:
                self.graphWP.chart_tabs.removeTab(2)
                self.graphWP.chart_tabs.removeTab(1)
                self.algorithm = "Simulated Annealing"
            except:
                traceback.print_exc()
        elif self.graphWP.chart_tabs.count() == 1 and pos == 0 :
            self.graphWP.chart_tabs.addTab(self.graphWP.chart2_tab, "Mean Length")
            self.graphWP.chart_tabs.addTab(self.graphWP.chart3_tab, "Variance Length")
            self.algorithm = "AntQ"
        elif self.graphWP.chart_tabs.count() == 1 and pos == 1 :
            self.graphWP.chart_tabs.addTab(self.graphWP.chart2_tab, "Mean Length")
            self.graphWP.chart_tabs.addTab(self.graphWP.chart3_tab, "Variance Length")
            self.algorithm = "ACO"

    def openFileDialog(self):
        open = OpenFileDialog(self.list_point, self.dist_matrix, self.numMarker, self.graph, self.gmap)
        open.show()
        self.dist_matrix = open.dist_matrix
        self.list_point = open.listMarker
        self.list_address = open.list_address
        self.graphWP.aco_tab.num_agent_slider.changeMax(open.numMarker)
        self.graphWP.antq_tab.num_agent_slider.changeMax(open.numMarker)
        self.numMarker = open.numMarker

    def valuechange(self, label):
        size = self.value()
        label.setFont(QFont("Arial", size))

    def showCurrentParameter(self):
        for i in range(self.graphWP.param_layout.count()):
            self.graphWP.param_layout.removeRow(0)
        self.graphWP.param_layout.update()

        if self.algorithm == "AntQ":
            self.graphWP.param_layout.addRow(QLabel("Algorithm: "), QLabel("AntQ"))
            self.graphWP.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(self.k_number)))
            self.graphWP.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(self.Ite)))
            self.graphWP.param_layout.addRow(QLabel("Number of agent: "), QLabel(str(self.numAgents)))
            self.graphWP.param_layout.addRow(QLabel("Learning rate: "), QLabel(str(self.LR)))
            self.graphWP.param_layout.addRow(QLabel("Discount factor: "), QLabel(str(self.DF)))
            self.graphWP.param_layout.addRow(QLabel("Balance rate: "), QLabel(str(self.BR)))
            self.graphWP.param_layout.addRow(QLabel("Delta: "), QLabel(str(self.delta)))
            self.graphWP.param_layout.addRow(QLabel("Beta: "), QLabel(str(self.beta)))
            dr = "Iter"
            if self.global_best:
                dr = "Global"
            self.graphWP.param_layout.addRow(QLabel("DR: "), QLabel(dr))
        elif self.algorithm == "ACO":
            self.graphWP.param_layout.addRow(QLabel("Algorithm: "), QLabel("ACO"))
            self.graphWP.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(self.k_number)))
            self.graphWP.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(self.Ite)))
            self.graphWP.param_layout.addRow(QLabel("Number of agent: "), QLabel(str(self.numAgents)))
            self.graphWP.param_layout.addRow(QLabel("Residual coefficient: "), QLabel(str(self.LR)))
            self.graphWP.param_layout.addRow(QLabel("Intensity: "), QLabel(str(self.DF)))
            self.graphWP.param_layout.addRow(QLabel("Alpha: "), QLabel(str(self.delta)))
            self.graphWP.param_layout.addRow(QLabel("Beta: "), QLabel(str(self.beta)))
        elif self.algorithm == "Simulated Annealing":
            self.graphWP.param_layout.addRow(QLabel("Algorithm: "), QLabel("ACO"))
            self.graphWP.param_layout.addRow(QLabel("Number of cluster: "), QLabel(str(self.k_number)))
            self.graphWP.param_layout.addRow(QLabel("Number of iteration: "), QLabel(str(self.Ite)))
            self.graphWP.param_layout.addRow(QLabel("Beta: "), QLabel(str(self.delta)))
            self.graphWP.param_layout.addRow(QLabel("T_0: "), QLabel(str(self.T_0)))
            self.graphWP.param_layout.addRow(QLabel("T_min: "), QLabel(str(self.T_min)))

    def applyPara(self):
        try:
            qm = QMessageBox()
            reply = qm.question(self, 'Message',
                                'Do you want to apply new parameter?', QMessageBox.Ok, QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                self.reset_graph()
                if self.curTab == 0:
                    self.algorithm = "AntQ"
                    self.delta = self.graphWP.antq_tab.delta_spin.value()
                    self.beta = self.graphWP.antq_tab.beta_spin.value()
                    self.Ite = self.graphWP.antq_tab.iteration_spin.value()
                    self.LR = self.graphWP.antq_tab.learning_rate_spin.value()
                    self.DF = self.graphWP.antq_tab.discount_factor_spin.value()
                    self.BR = self.graphWP.antq_tab.balance_rate_spin.value()
                    self.numAgents = self.graphWP.antq_tab.num_agent_slider.k
                    self.k_number = self.graphWP.antq_tab.k_num_spin.value()
                    if self.k_number < 2:
                        self.k_number = 1
                    dr = self.graphWP.antq_tab.dr_combobox.currentIndex()
                    self.global_best = True
                    if dr == 0:
                        self.global_best = False
                    self.showCurrentParameter()
                elif self.curTab == 1:
                    self.algorithm = "ACO"
                    self.delta = self.graphWP.aco_tab.delta_spin.value()
                    self.beta = self.graphWP.aco_tab.beta_spin.value()
                    self.Ite = self.graphWP.aco_tab.iteration_spin.value()
                    self.LR = self.graphWP.aco_tab.learning_rate_spin.value()
                    self.DF = self.graphWP.aco_tab.discount_factor_spin.value()
                    self.numAgents = self.graphWP.aco_tab.num_agent_slider.k
                    self.k_number = 1
                    self.showCurrentParameter()
                elif self.curTab == 2:
                    self.algorithm = "Simulated Annealing"
                    self.T_0 = self.graphWP.sa_tab.temper_init_spin.value()
                    self.T_min = self.graphWP.sa_tab.temper_end_spin.value()
                    self.beta = self.graphWP.sa_tab.beta_spin.value()
                    self.Ite = self.graphWP.sa_tab.iteration_spin.value()
                    self.k_number = 1
                    self.showCurrentParameter()
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)

    # Implement Algorithm
    def runAlgorithm(self):
        if self.numMarker < 2:
            qm = QMessageBox
            qm.information(self,"", "Atleast two points!")
        else :
            self.algorithm_result = Queue()
            try:
                self.result_handler = Thread(target=self.drawChart)
                self.result_handler.start()
            except:
                traceback.print_exc()

            if self.algorithm == "AntQ":
                try:
                    # Create AntQ with Clustering
                    self.algEx = AntQClustering(self.list_point, self.dist_matrix, self.k_number, self.numAgents,
                                                self.Ite, self.LR / 100, self.DF / 100, self.delta,
                                                self.beta, q0=self.BR / 100, global_best=self.global_best, result_queue=self.algorithm_result)
                except:
                    traceback.print_exc()

            elif self.algorithm == "ACO":
                try:
                    # Create ACO
                    self.algGraphEx = ACOGraph(self.dist_matrix, len(self.dist_matrix))
                    self.algEx = ACO(self.numAgents, self.Ite, self.algGraphEx,
                                         self.delta, self.beta, self.LR / 100, self.DF / 100, 2,
                                         result_queue=self.algorithm_result)
                except:
                    traceback.print_exc()

            elif self.algorithm == "Simulated Annealing":
                #Create Simulated Annealing
                self.algEx = SimAnneal(self.dist_matrix, T=self.T_0, alpha=self.beta / 100,
                                       stopping_T=self.T_min, stopping_iter=self.Ite, result_queue=self.algorithm_result)

            #Create cluster
            self.graph.clearGraph()
            self.graph.updateCluster(self.algEx.clusters_point)
            #Start algorithm
            self.algEx.run_finished.connect(self.algorithmFinished)
            self.algEx.start()

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
                    if self.algorithm == "AntQ" or self.algorithm == "ACO":
                        iter_avg = result["iter_avg"]
                        iter_deviation = result["iter_deviation"]
                        # Draw chart
                        if iteration == 0:
                            pass
                            # add new lines
                            self.graphWP.best_length_chart.addNewLine(iteration, best_tour_len)
                            self.graphWP.mean_length_chart.addNewLine(iteration, iter_avg)
                            self.graphWP.st_deviation_chart.addNewLine(iteration, iter_deviation)
                        else:
                            pass
                            # update lines
                            self.graphWP.best_length_chart.updateNewestLine(iteration, best_tour_len)
                            self.graphWP.mean_length_chart.updateNewestLine(iteration, iter_avg)
                            self.graphWP.st_deviation_chart.updateNewestLine(iteration, iter_deviation)
                        if self.algorithm == "ACO":
                            best_tour = [best_tour]
                    elif self.algorithm == "Simulated Annealing":
                        # Simulated Annealing
                        best_tour = [best_tour]
                        # Draw chart
                        if iteration == 1:
                            # add new lines
                            self.graphWP.best_length_chart.addNewLine(iteration, best_tour_len)
                        else:
                            # update lines
                            self.graphWP.best_length_chart.updateNewestLine(iteration, best_tour_len)

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
            parameter["number_of_cluster"] = self.k_number
            dataset = {}
            dataset["list_points"] = self.list_point
            dataset["distance_matrix"] = self.dist_matrix
            dataset["list_address"] = self.list_address
            result = {}
            if self.algorithm == "AntQ":
                # AntQ
                # Get all value
                algorithm = "AntQ"
                dr = "Iteration best"
                if self.global_best:
                    dr = "Global best"
                parameter["delayed_reinforcement"] = dr
                parameter["number_of_iteration"] = self.Ite
                parameter["number_of_agent"] = self.numAgents
                parameter["learnning_rate"] = self.LR / 100
                parameter["discount_factor"] = self.DF / 100
                parameter["balance_rate"] = self.BR / 100
                parameter["delta"] = self.delta
                parameter["beta"] = self.beta
                result["clusters_point"] = self.algEx.clusters_point
                result["best_tour"] = self.algEx.clusters_best_tour
                result["best_length"] = self.algEx.best_len
                result["list_iteration"] = list(range(self.Ite))
                result["list_best_tour"] = self.algEx.list_clusters_best_tour
                result["list_best_len"] = self.algEx.list_avg_best_length
                result["list_avg"] = self.algEx.list_avg_mean_length
                result["list_deviation"] = self.algEx.list_avg_dev

                # Create log object
                self.logging = Log(key=key, name=name, algorithm=algorithm, number_of_point=number_of_point,
                                   created_date=created_date, parameter=parameter, dataset=dataset, result=result)
            elif self.algorithm == "ACO":
                # ACO
                # Get all value
                algorithm = "ACO"
                parameter["number_of_iteration"] = self.Ite
                parameter["number_of_agent"] = self.numAgents
                parameter["residual_coefficient"] = self.LR / 100
                parameter["intensity"] = self.DF / 100
                parameter["alpha"] = self.delta
                parameter["beta"] = self.beta
                result["clusters_point"] = self.algEx.clusters_point
                result["best_tour"] = [self.algEx.best_tour]
                result["best_length"] = self.algEx.best_tour_len
                result["list_iteration"] = list(range(self.Ite))
                result["list_best_tour"] = self.algEx.list_best_tour
                result["list_best_len"] = self.algEx.list_best_len
                result["list_avg"] = self.algEx.list_avg
                result["list_deviation"] = self.algEx.list_dev

                # Create log object
                self.logging = Log(key=key, name=name, algorithm=algorithm, number_of_point=number_of_point,
                                   created_date=created_date, parameter=parameter, dataset=dataset, result=result)
            elif self.algorithm == "Simulated Annealing":
                # Simulated Annealing
                # Get all value
                algorithm = "Simulated Annealing"
                parameter["t0"] = self.T_0
                parameter["t_min"] = self.T_min
                parameter["beta"] = self.beta
                parameter["number_of_iteration"] = self.Ite
                result["clusters_point"] = self.algEx.clusters_point
                result["best_tour"] = [self.algEx.best_tour]
                result["best_length"] = self.algEx.best_tour_len
                result["list_iteration"] = list(range(self.Ite))
                result["list_best_tour"] = self.algEx.best_tours
                result["list_best_len"] = self.algEx.best_lens

                # Create log object
                self.logging = Log(key=key, name=name, algorithm=algorithm, number_of_point=number_of_point,
                                   created_date=created_date, parameter=parameter, dataset=dataset, result=result)

            self.algorithm_result.put(None)
            #self.saveLog()
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
                if self.logging != None:
                    self.logging.name = name
                    self.log_io.addNewLog(self.logging)
                    self.logging = None

    def enableSpinBox(self):
        #global Knum, checkK
        if self.graphWP.antq_tab.checkK.isChecked() == True:
            self.graphWP.antq_tab.Knum.setDisabled(False)
        else:
            self.graphWP.antq_tab.Knum.setDisabled(True)

    def reset_graph(self):
        self.graphWP.best_length_chart.clearChart()
        self.graphWP.mean_length_chart.clearChart()
        self.graphWP.st_deviation_chart.clearChart()
        self.logging = None

    def reset_point(self):
        self.list_point = []
        self.list_address = []
        self.dist_matrix = []

    def run_google_map_log(self):
        try:
            log_key = self.googleWP.log_panel.currentKey
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
                self.googleWP.showRouteAddress(list_address, clusters_point, best_tour, 0)

                # Show parameter
                self.googleWP.showAlgorithmParameter(parameter, algorithm)

                #Add cluster number to combobox
                self.googleWP.route_table.cluster_combobox.clear()
                self.googleWP.route_table.cluster_combobox.addItem("All")
                for i in range(len(clusters_point)):
                    self.googleWP.route_table.cluster_combobox.addItem("Cluster {}".format(i + 1))

            else:
                error = QMessageBox()
                error.critical(self, "Error", "Dataset of log isn't Google Map dataset", QMessageBox.Ok)
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)

    def google_map_change_cluster(self, pos):
        cluster_number = pos
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
                self.googleWP.showRouteAddress(list_address, clusters_point, best_tour, pos)
            except:
                traceback.print_exc()

class OpenFileDialog(QWidget):

    def __init__(self, listMarker, dist_matrix, numMarker, graph, gmap):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.listMarker = listMarker
        self.dist_matrix = dist_matrix
        self.numMarker = numMarker
        self.is_googlemap = False
        self.list_address = []

        self.graph = graph
        self.gmap = gmap
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openAtspFileNameDialog()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.numMarker = 0
            data = json.load(codecs.open(fileName, 'r', 'utf-8-sig'))
            for coord in data:
                self.numMarker += 1
                marker = {"latitude": coord['latitude'], "longitude": coord['longitude']}
                self.listMarker.append(marker)
                self.gmap.addMarker(str(self.numMarker), marker['latitude'], marker['longitude'], **dict(
                    title="Move me!"
                ))
                self.graph.add_coord((marker['latitude'],  marker['longitude']))

            self.graph.draw_graph()

    def openAtspFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            try:
                self.is_googlemap = False
                # self.graph.points = []
                self.graph.clearGraph()
                if fileName.lower().endswith('.atsp'):
                    # Read atsp file
                    reader = ATSPReader(fileName.strip())
                    self.listMarker = reader.cities_tups
                    self.numMarker = len(self.listMarker)

                    self.dist_matrix = reader.dist_matrix

                    # Draw graph
                    self.graph.initCoordData(self.listMarker)

                elif fileName.lower().endswith('.tsp'):
                    # Reader tsp file
                    reader = TSPFileReader(fileName.strip())
                    self.listMarker = reader.cities_tups
                    self.numMarker = len(self.listMarker)
                    self.dist_matrix = reader.dist_matrix

                    self.graph.initCoordData(self.listMarker)

                elif fileName.lower().endswith('.json'):
                    self.is_googlemap = True
                    # Reader tsp file
                    reader = GMapDataReader(fileName.strip())
                    self.listMarker = reader.cities_tups
                    self.numMarker = len(self.listMarker)
                    self.dist_matrix = reader.dist_matrix
                    self.list_address = reader.list_address
                    # Draw graph
                    try:
                        self.graph.initCoordData(self.listMarker)
                    except:
                        traceback.print_exc()
                if self.numMarker < 1:
                    qm = QMessageBox
                    qm.critical(self.parent(), "", "Wrong file!")
            except:
                self.graph.clearGraph()
                self.listMarker = []
                self.numMarker = 0
                self.dist_matrix = []
                qm = QMessageBox
                qm.critical(self.parent(), "", "Wrong file!")



