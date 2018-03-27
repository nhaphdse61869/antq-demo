
from PyQt5.QtGui import QFont, QStandardItemModel, QColor
import sys
from UI.BlinkingButton import StateWidget
from queue import Queue
from UI.FileDialog import *
from qgmap.common import QGoogleMap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from figure.chart import LengthChartCanvas, GraphCanvas
from antq.antQ import AntQ
from antq.antQGraph import AntQGraph
from UI.Filter import Filter
from UI.ResultFrame import ResultFrame
from threading import Thread
from UI.AntQTab import *
from UI.SimAnnealTab import *
from UI.ACOTab import *
from UI.GraphWorkPlay import *
from UI.GoogleWorkPlay import *
import datetime
from util.logging import LogIO, Log
from hierarchy.antqCluster import *
from hierarchy.sa import *

class UIThread(QWidget):

    def __init__(self):
        super().__init__()
        self.best_tour = []
        self.list_point = []
        self.dist_matrix = []
        self.numMarker = 0
        self.log_io = LogIO()
        self.logging = None
        self.algEx = None
        self.h = QVBoxLayout()
        self.mainLayout = QVBoxLayout(self)
        #self.l = QFormLayout()
        self.layout = QHBoxLayout()
        #self.layout1 = QVBoxLayout()

        self.graphWP = GraphWP()
        self.googleWP = GoogkeWP()

        self.tabs2 = QTabWidget()
        self.tabGM = QWidget()
        self.tabGraph = QWidget()
        self.tabs2.addTab(self.tabGraph, "Graph")
        self.tabs2.addTab(self.tabGM, "Google Map")
        self.tabGM.layout = QVBoxLayout()
        self.tabGM.setLayout(self.tabGM.layout)
        self.h.addWidget(self.tabs2)
        self.graph = GraphCanvas(width=6, height=5, dpi=110)
        self.tabGraph.layout = QVBoxLayout()
        self.tabGraph.setLayout(self.tabGraph.layout)
        self.tabGraph.layout.addWidget(self.graph)
        self.tabGraph.layout.setSpacing(0)
        # layout1.addWidget(chart)
        # layout1.addWidget(paraSample)

        # Chart Graph

        self.layout.addLayout(self.h)

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.graphWP)
        self.Stack.addWidget(self.googleWP)
        self.layout.addWidget(self.Stack)
        self.mainLayout.addLayout(self.layout)

        #self.h.addLayout(self.l)
        numMarker = 0
        listMarker = []

        # GG Maps container

        self.gmap = QGoogleMap(self)
        self.gmap.mapMovedSignal.connect(self.onMapMoved)
        self.gmap.mapClickedSignal.connect(self.onMapLClick)
        self.gmap.mapDoubleClickedSignal.connect(self.onMapDClick)
        self.gmap.mapRightClickedSignal.connect(self.onMapRClick)
        self.gmap.markerClickedSignal.connect(self.onMarkerLClick)
        self.gmap.markerDoubleClickedSignal.connect(self.onMarkerDClick)
        self.gmap.markerRightClickedSignal.connect(self.onMarkerRClick)

        self.gmap.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding)
        self.tabGM.layout.addWidget(self.gmap)

        # w.showFullScreen()
        self.setGeometry(0, 40, 0, 0)
        self.resize(2600, 0)
        self.gmap.waitUntilReady()

        self.gmap.setZoom(15)
        # center at HCM city
        self.gmap.centerAt(10.857200, 106.628487)
        # Some Static points
        for place in [
            "Plaza Ramon Castilla",
            "Plaza San Martin",
        ]:
            self.gmap.addMarkerAtAddress(place,
                                    icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
                                    )
        # gmap.setZoom(15)

        # Parameter to excute algorithm
        # default values
        self.curTab = 0
        self.delta = 1
        self.beta = 2
        self.Ite = 200
        self.numAgents = 1
        self.LR = 10
        self.DF = 30
        self.BR = 90
        self.T_0 = 0
        self.T_min = 0

        self.graphWP.acoParam.checkK.stateChanged.connect(self.enableSpinBox)
        self.graphWP.antQParam.checkK.stateChanged.connect(self.enableSpinBox)

        self.graphWP.btn2.clicked.connect(self.runAlgorithm)
        self.graphWP.btn1.clicked.connect(self.applyPara)
        self.graphWP.btn3.clicked.connect(self.test)
        self.graphWP.btn4.clicked.connect(self.openFileDialog)
        self.graphWP.tabs.tabBarClicked.connect(self.checkCurrentTab)
        self.tabs2.tabBarClicked.connect(self.checkGoogleTab)
        #self.btn1.setGraphicsEffect()
        #self.show()

    def checkGoogleTab(self, pos):
        if pos == 1:
            self.Stack.setCurrentIndex(1)
        else:
            self.Stack.setCurrentIndex(0)

    def checkCurrentTab(self, pos):
        self.curTab = pos
        if pos == 2:
            self.graphWP.tabGraphs.removeTab(2)
            self.graphWP.tabGraphs.removeTab(1)
        elif self.graphWP.tabGraphs.count() == 1:
            self.graphWP.tabGraphs.addTab(self.graphWP.tabG2, "Mean Length")
            self.graphWP.tabGraphs.addTab(self.graphWP.tabG3, "Variance Length")


    def onMarkerRClick(self, key):
        print("RClick on ", key)

        self.gmap.setMarkerOptions(key, draggable=False)

    def onMarkerLClick(self,key):
        print("LClick on ", key)

    def onMarkerDClick(self, key):
        print("DClick on ", key)
        self.gmap.setMarkerOptions(key, draggable=True)

    def onMapMoved(self, latitude, longitude):
        print("Moved to ", latitude, longitude)

    def onMapRClick(self, latitude, longitude):
        print("RClick on ", latitude, longitude)

    def onMapLClick(self, latitude, longitude):
        #global numMarker, listMarker, numOfAgents
        self.numMarker += 1
        marker = {"latitude": latitude, "longitude": longitude}
        self.listMarker.append(marker)
        self.gmap.addMarker(str(self.numMarker), latitude, longitude, **dict(
            title="Move me!"
        ))
        self.graphWP.graph.add_coord((latitude, longitude))
        self.graphWP.acoParam.numOfAgents.changeMax(self.numMarker)
        self.graphWP.antQParam.numOfAgents.changeMax(self.numMarker)
        print("LClick on ", latitude, longitude)

    def onMapDClick(self, latitude, longitude):
        print("DClick on ", latitude, longitude)

    def showRoute(self, best_tour):
        #global listMarker
        self.gmap.directss(self.listMarker, best_tour)

    def openFileDialog(self):
        open = OpenFileDialog(self.list_point, self.dist_matrix, self.numMarker, self.graph, self.gmap)
        open.show()
        self.dist_matrix = open.dist_matrix
        self.list_point = open.listMarker
        self.graphWP.acoParam.numOfAgents.changeMax(open.numMarker)
        self.graphWP.antQParam.numOfAgents.changeMax(open.numMarker)
        self.numMarker = open.numMarker

    def valuechange(self, label):
        size = self.value()
        label.setFont(QFont("Arial", size))


    def applyPara(self):
        if self.curTab == 0:
            self.delta = self.antQParam.deltaSpin.value()
            self.beta = self.antQParam.betaSpin.value()
            self.Ite = self.antQParam.iteration.value()
            self.LR = self.antQParam.learningRate.value()
            self.DF = self.antQParam.discountFactor.value()
            self.BR = self.antQParam.balanceRate.value()
            self.numAgents = self.antQParam.numOfAgents.k
            if self.graphWP.antQParam.checkK.isChecked() == True:
                self.k_number = self.graphWP.antQParam.Knum.value()
            else:
                self.k_number = -1
        elif self.curTab == 1:
            self.delta = self.graphWP.acoParam.deltaSpin.value()
            self.beta = self.graphWP.acoParam.betaSpin.value()
            self.Ite = self.graphWP.acoParam.iteration.value()
            self.LR = self.graphWP.acoParam.learningRate.value()
            self.DF = self.graphWP.acoParam.discountFactor.value()
            self.BR = self.graphWP.acoParam.balanceRate.value()
            self.numAgents = self.graphWP.acoParam.numOfAgents.k
        elif self.curTab == 2:
            self.T_0 = self.graphWP.simAnnealParam.temperInit.value()
            self.T_min = self.graphWP.simAnnealParam.temperEnd.value()
            self.beta = self.graphWP.simAnnealParam.betaSpin.value()
            self.Ite = self.graphWP.simAnnealParam.iterSpin.value()

    # Implement Algorithm
    def runAlgorithm(self):
        if self.numMarker < 2:
            qm = QMessageBox
            qm.information(self,"", "Atleast two points!")
        else :
            self.applyPara()
            self.algorithm_result = Queue()
            #matrix = self.gmap.convertTo2DArray(self.listMarker)
            self.result_handler = Thread(target=self.drawChart)
            self.result_handler.start()

            if self.curTab == 0:
                if self.antQParam.checkK.isChecked() == True:
                    #Excute AntQ with Clustering

                    self.algEx = AntQClustering(self.list_point, self.dist_matrix, self.k_number, self.numAgents,
                                                self.Ite, self.LR / 100, self.DF / 100, self.delta,
                                                self.beta, result_queue=self.algorithm_result)
                    print("Sao éo chạy")
                    self.algEx.run_finished.connect(self.algorithmFinished)
                    self.algEx.start()
                else:
                    #Excute AntQ
                    self.algGraphEx = AntQGraph(self.dist_matrix)
                    self.algEx = AntQ(self.numAgents, self.Ite, self.algGraphEx,
                                      self.LR / 100, self.DF / 100, self.delta, self.beta, result_queue=self.algorithm_result)
                    self.algEx.run_finished.connect(self.algorithmFinished)
                    self.algEx.start()

            elif self.curTab == 1:
                #Excute ACO
                pass
            elif self.curTab == 2:
                self.algEx = SimAnneal(self.dist_matrix, T=self.T_0, alpha=self.beta / 100,
                                       stopping_T=self.T_min, stopping_iter=self.Ite, result_queue=self.algorithm_result)
                self.algEx.run_finished.connect(self.algorithmFinished)
                self.algEx.start()


    def drawChart(self):
        while True:
            result = self.algorithm_result.get()
            iteration = result["iteration"]
            best_tour_len = result["best_tour_len"]
            best_tour = result["best_tour"]
            #Draw Graph
            if self.best_tour != best_tour:
                self.best_tour = best_tour
                self.graph.clear_graph_tour()
                self.graph.draw_tour(best_tour)

            if self.curTab == 0:
                iter_avg = result["iter_avg"]
                iter_variance = result["iter_variance"]
                iter_deviation = result["iter_deviation"]
                # Draw chart
                if iteration == 0:
                    # add new lines
                    self.graphWP.chartBestLength.add_new_line(iteration, best_tour_len)
                    self.graphWP.chartMeanLength.add_new_line(iteration, iter_avg)
                    self.graphWP.chartVarianceLength.add_new_line(iteration, iter_variance)
                else:
                    # update lines
                    self.graphWP.chartBestLength.update_newest_line(iteration, best_tour_len)
                    self.graphWP.chartMeanLength.update_newest_line(iteration, iter_avg)
                    self.graphWP.chartVarianceLength.update_newest_line(iteration, iter_variance)

            elif self.curTab == 1:
                iter_avg = result["iter_avg"]
                iter_variance = result["iter_variance"]
                iter_deviation = result["iter_deviation"]
                # ACO
                # Draw chart
                if iteration == 0:
                    # add new lines
                    self.graphWP.chartBestLength.add_new_line(iteration, best_tour_len)
                    self.graphWP.chartMeanLength.add_new_line(iteration, iter_avg)
                    self.graphWP.chartVarianceLength.add_new_line(iteration, iter_variance)
                else:
                    # update lines
                    self.graphWP.chartBestLength.update_newest_line(iteration, best_tour_len)
                    self.graphWP.chartMeanLength.update_newest_line(iteration, iter_avg)
                    self.graphWP.chartVarianceLength.update_newest_line(iteration, iter_variance)

            elif self.curTab == 2:
                # Simulated Annealing
                # Draw chart
                if iteration == 0:
                    # add new lines
                    self.graphWP.chartBestLength.add_new_line(iteration, best_tour_len)
                else:
                    # update lines
                    self.graphWP.chartBestLength.update_newest_line(iteration, best_tour_len)

    @pyqtSlot()
    def algorithmFinished(self):
        #Create Log object
        if self.curTab == 0:
            print("Finish dk ko nè")
            #AntQ
            #Get all value
            key = self.log_io.get_new_log_key()
            name = key
            algorithm = "AntQ"
            number_of_point = len(self.list_point)
            created_date = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            parameter = {}
            parameter["number_of_iteration"] = self.Ite
            parameter["number_of_agent"] = self.numAgents
            parameter["learnning_rate"] = self.LR / 100
            parameter["discount_factor"] = self.DF / 100
            parameter["delta"] = self.delta
            parameter["beta"] = self.beta
            parameter["k_number"] = self.k_number
            print("Tới dataset nè")
            dataset = {}
            dataset["list_points"] = self.list_point
            dataset["distance_matrix"] = self.dist_matrix
            print("Tới result nè")
            result = {}
            result["best_tour"] = self.algEx.best_tour
            result["best_length"] = self.algEx.best_tour_len
            result["list_iteration"] = list(range(self.Ite))
            result["list_best_tour"] = self.algEx.list_best_tour
            result["list_best_len"] = self.algEx.list_best_len
            result["list_avg"] = self.algEx.list_avg
            result["list_deviation"] = self.algEx.list_dev

            #Create log object
            self.logging = Log(key=key, name=name, algorithm=algorithm, number_of_point=number_of_point,
                               created_date= created_date, parameter=parameter, dataset=dataset, result=result)
            print("Có log object r nè")
        elif self.curTab == 1:
            #ACO
            # Get all value
            key = self.log_io.get_new_log_key()
            name = key
            algorithm = "ACO"
            number_of_point = len(self.list_point)
            created_date = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            parameter = {}
            parameter["number_of_iteration"] = self.Ite
            parameter["number_of_agent"] = self.numAgents
            parameter["learnning_rate"] = self.LR / 100
            parameter["discount_factor"] = self.DF / 100
            parameter["delta"] = self.delta
            parameter["beta"] = self.beta
            dataset = {}
            dataset["list_points"] = self.list_point
            dataset["distance_matrix"] = self.dist_matrix
            result = {}
            result["best_tour"] = self.algEx.best_tour
            result["best_length"] = self.algEx.best_tour_len
            result["list_iteration"] = list(range(self.Ite))
            result["list_best_tour"] = self.algEx.list_best_tour
            result["list_best_len"] = self.algEx.list_best_len
            result["list_avg"] = self.algEx.list_avg
            result["list_deviation"] = self.algEx.list_dev

            # Create log object
            self.logging = Log(key=key, name=name, algorithm=algorithm, number_of_point=number_of_point,
                               created_date=created_date, parameter=parameter, dataset=dataset, result=result)
        elif self.curTab == 2:
            #Simulated Annealing
            # Get all value
            key = self.log_io.get_new_log_key()
            name = key
            algorithm = "Simulated Annealing"
            number_of_point = len(self.list_point)
            created_date = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            parameter = {}
            parameter["t0"] = self.T_0
            parameter["t_min"] = self.T_min
            parameter["beta"] = self.beta
            parameter["number_of_iteration"] = self.Ite
            dataset = {}
            dataset["list_points"] = self.list_point
            dataset["distance_matrix"] = self.dist_matrix
            result = {}
            result["best_tour"] = self.algEx.best_tour
            result["best_length"] = self.algEx.best_tour_len
            result["list_iteration"] = list(range(self.Ite))
            result["list_best_tour"] = self.algEx.best_tours
            result["list_best_len"] = self.algEx.best_lens

            # Create log object
            self.logging = Log(key=key, name=name, algorithm=algorithm, number_of_point=number_of_point,
                               created_date=created_date, parameter=parameter, dataset=dataset, result=result)
        #Test save log
        self.saveLog()

    def saveLog(self):
        qm = QMessageBox()
        reply = qm.question(self, 'Message',
                  'Do you wan to save Log?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            name, ok = QInputDialog.getText(self, 'Create Log', 'Log Name:')
            if ok:
                if self.logging != None:
                    self.logging.name = name
                    self.log_io.add_new_log(self.logging)
                    self.logging = None

    def enableSpinBox(self):
        #global Knum, checkK
        if self.antQParam.checkK.isChecked() == True:
            self.antQParam.Knum.setDisabled(False)
        else:
            self.antQParam.Knum.setDisabled(True)

    def clear_graph(self):
        self.graphWP.graph.clear_graph_tour()
        self.graphWP.chartBestLength.clear_graph()
        self.graphWP.chartMeanLength.clear_graph()
        self.graphWP.chartVarianceLength.clear_graph()
        self.logging = None

    def test(self):
        self.animation2.setDuration(1000)
        self.animation2.setLoopCount(1)
        self.animation2.setStartValue(QColor(192,224,192))
        self.animation2.setKeyValueAt(0.12, QColor(192,192,192))
        self.animation2.setEndValue(QColor(212,208,200))
        self.animation2.start()