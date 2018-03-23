
from PyQt5.QtGui import QFont, QStandardItemModel, QColor

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
import time

class UIThread(QWidget):

    def __init__(self):
        super().__init__()
        self.listMarker = []
        self.numMarker = 0
        self.h = QVBoxLayout()
        self.mainLayout = QVBoxLayout(self)
        self.l = QFormLayout()
        self.layout = QHBoxLayout()
        self.layout1 = QVBoxLayout()

        self.tabs2 = QTabWidget()
        self.tabGM = QWidget()
        self.tabGraph = QWidget()
        self.tabs2.addTab(self.tabGraph, "Graph")
        self.tabs2.addTab(self.tabGM, "Google Map")
        self.tabGM.layout = QVBoxLayout()
        self.tabGM.setLayout(self.tabGM.layout)
        self.h.addWidget(self.tabs2)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab3, "Ant-Q")
        self.tabs.addTab(self.tab1, "ACO")
        self.tabs.addTab(self.tab2, "Simulated Annealing")
        #Ant-Q Parameter layout-------------------------------------------------------------
        self.tab3.layout = QVBoxLayout()
        self.tab3.setLayout(self.tab3.layout)
        self.antQParam = AntQTab()
        self.tab3.layout.addLayout(self.antQParam.topParaLayout)
        self.tab3.layout.addLayout(self.antQParam.paraLayoutH)
        #-----------------------------------------------------------------------------
        self.tab2.layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2.layout)
        self.simAnnealParam = SimAnnealTab()
        self.tab2.layout.addLayout(self.simAnnealParam.firstLayout)
        self.tab2.layout.addLayout(self.simAnnealParam.secondLayout)
        #-----------------------------------------------------------------------------
        self.tab1.layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1.layout)
        self.acoParam = ACOTab()

        self.tab1.layout.addLayout(self.acoParam.topParaLayout)
        self.tab1.layout.addLayout(self.acoParam.paraLayoutH)
        #------------------------------------------------------------------------
        # Chart LINE
        self.tabGraphs = QTabWidget()
        self.tabG1 = QWidget()
        self.tabG2 = QWidget()
        self.tabG3 = QWidget()
        self.chartBestLength = LengthChartCanvas()
        self.chartMeanLength = LengthChartCanvas()
        self.chartVarianceLength = LengthChartCanvas()

        self.tabGraphs.addTab(self.tabG1, "Best Length")
        self.tabGraphs.addTab(self.tabG2, "Mean Length")
        self.tabGraphs.addTab(self.tabG3, "Variance Length")

        self.tabG1.layout = QVBoxLayout()
        self.tabG1.setLayout(self.tabG1.layout)
        self.paraSample = QScrollArea()
        self.paraSample.setWidgetResizable(True)
        self.tabG1.layout.addWidget(self.chartBestLength)
        self.tabG1.layout.addWidget(self.paraSample)

        self.tabG2.layout = QVBoxLayout()
        self.tabG2.setLayout(self.tabG2.layout)
        self.paraSample = QScrollArea()
        self.paraSample.setWidgetResizable(True)
        self.tabG2.layout.addWidget(self.chartMeanLength)
        self.tabG2.layout.addWidget(self.paraSample)

        self.tabG3.layout = QVBoxLayout()
        self.tabG3.setLayout(self.tabG3.layout)
        self.paraSample = QScrollArea()
        self.paraSample.setWidgetResizable(True)
        self.tabG3.layout.addWidget(self.chartVarianceLength)
        self.tabG3.layout.addWidget(self.paraSample)

        self.layout1.addWidget(self.tabGraphs)
        # layout1.addWidget(chart)
        # layout1.addWidget(paraSample)

        # Chart Graph
        self.graph = GraphCanvas(width=6, height=5, dpi=110)
        self.tabGraph.layout = QVBoxLayout()
        self.tabGraph.setLayout(self.tabGraph.layout)
        self.tabGraph.layout.addWidget(self.graph)
        self.tabGraph.layout.setSpacing(0)

        self.subLayout = QVBoxLayout()
        self.layout.addLayout(self.h)
        self.layout.addLayout(self.subLayout)
        self.ortherLayout = QHBoxLayout()

        self.topSubLayout = QHBoxLayout()
        self.topSubLayout.addWidget(self.tabs)
        self.topSubLayout.addLayout(self.ortherLayout)

        self.subLayout.addLayout(self.topSubLayout)

        # function buttons
        self.subLayout.addLayout(self.layout1)
        #self.btn1 = StateWidget()
        self.btn1 = QPushButton("Apply")
        self.btn2 = QPushButton("Run")
        self.btn3 = QPushButton("Test")
        self.btn4 = QPushButton("Generate")
        #self.btn2.setStyleSheet("background-color: red")
        self.formButCon1 = QGroupBox()
        self.butLayout1 = QFormLayout()

        self.butLayout1.addWidget(self.btn1)
        self.butLayout1.addWidget(self.btn2)
        self.butLayout1.addWidget(self.btn3)
        self.butLayout2 = QFormLayout()
        self.butLayout2.addWidget(self.btn4)
        self.ortherLayout.setStretch(10, 10)

        self.ortherLayout.addLayout(self.butLayout1)
        self.ortherLayout.addLayout(self.butLayout2)

        self.mainLayout.addLayout(self.layout)

        self.h.addLayout(self.l)
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

        self.componentRS = ResultFrame(self)
        self.componentRS.setWindowOpacity(1)
        self.showBtn = QPushButton("<", self.componentRS)
        self.showBtn.resize(30, 50)
        self.showBtn.move(0, 280)

        self.animation = QPropertyAnimation(self.componentRS, b"geometry")
        self.animation1 = QPropertyAnimation(self.componentRS, b"opacity")
        self.animation2 = QPropertyAnimation(self.btn1, b"styleSheet")
        self.showBtn.clicked.connect(self.moveRs)
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

        self.acoParam.checkK.stateChanged.connect(self.enableSpinBox)

        self.btn2.clicked.connect(self.runAlgorithm)
        self.btn1.clicked.connect(self.applyPara)
        self.btn3.clicked.connect(self.test)
        self.btn4.clicked.connect(self.openFileDialog)
        self.tabs.tabBarClicked.connect(self.checkCurrentTab)
        #self.btn1.setGraphicsEffect()
        #self.show()


    def checkCurrentTab(self, pos):
        self.curTab = pos

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
        self.graph.add_coord((latitude, longitude))
        self.acoParam.numOfAgents.changeMax(self.numMarker)
        self.antQParam.numOfAgents.changeMax(self.numMarker)
        print("LClick on ", latitude, longitude)

    def onMapDClick(self, latitude, longitude):
        print("DClick on ", latitude, longitude)

    def showRoute(self, best_tour):
        #global listMarker
        self.gmap.directss(self.listMarker, best_tour)

    def openFileDialog(self):
        open = OpenFileDialog(self.listMarker, self.numMarker, self.graph, self.gmap)
        open.show()
        self.acoParam.numOfAgents.changeMax(open.numMarker)
        self.antQParam.numOfAgents.changeMax(open.numMarker)
        self.numMarker = open.numMarker

    def valuechange(self, label):
        size = self.value()
        label.setFont(QFont("Arial", size))

    # animation
    def moveRs(self):
        #global componentRS, animation, animation1, showBtn
        old_pos = QRect(1345, 0, 300, 680)
        if self.componentRS.pos().x() == old_pos.x():
            self.animation.setDuration(1000)
            self.animation.setStartValue(QRect(1345, 0, 300, 680))
            self.animation.setEndValue(QRect(1070, 0, 300, 680))
            self.animation.start()
            self.showBtn.setText(">")
            self.componentRS.dataGroupBox.show()
        else:
            self.animation.setDuration(50)
            self.animation.setStartValue(QRect(1070, 0, 300, 680))
            self.animation.setEndValue(QRect(1345, 0, 300, 680))
            self.animation.start()
            self.showBtn.setText("<")
            self.componentRS.dataGroupBox.hide()



    def applyPara(self):
        if self.curTab == 1:
            self.delta = self.acoParam.deltaSpin.value()
            self.beta = self.acoParam.betaSpin.value()
            self.Ite = self.acoParam.iteration.value()
            self.LR = self.acoParam.learningRate.value()
            self.DF = self.acoParam.discountFactor.value()
            self.BR = self.acoParam.balanceRate.value()
            self.numAgents = self.acoParam.numOfAgents.k
        elif self.curTab == 0:
            self.delta = self.antQParam.deltaSpin.value()
            self.beta = self.antQParam.betaSpin.value()
            self.Ite = self.antQParam.iteration.value()
            self.LR = self.antQParam.learningRate.value()
            self.DF = self.antQParam.discountFactor.value()
            self.BR = self.antQParam.balanceRate.value()
            self.numAgents = self.antQParam.numOfAgents.k
        elif self.curTab == 2:
            self.T_0 = self.simAnnealParam.temperInit.value()
            self.T_min = self.simAnnealParam.temperEnd.value()
            self.beta = self.simAnnealParam.betaSpin.value()
            self.Ite = self.simAnnealParam.iterSpin.value()

    # Implement Algorithm
    def runAlgorithm(self):
        if self.numMarker < 2:
            qm = QMessageBox
            qm.information(self,"", "Atleast two points!")
        else :
            self.applyPara()
            self.algorithm_result = Queue()
            matrix = self.gmap.convertTo2DArray(self.listMarker)
            self.result_handler = Thread(target=self.drawChart)
            self.result_handler.start()
            self.algGraphEx = AntQGraph(matrix)
            self.algEx = AntQ(self.numAgents, self.Ite, self.algGraphEx,
                         self.LR / 100, self.DF / 100, self.delta, self.beta, result=self.algorithm_result)
            self.algEx.start()


    def drawChart(self):
        while True:
            result = self.algorithm_result.get()
            iteration = result["iteration"]
            best_tour_len = result["best_tour_len"]
            best_tour = result["best_tour"]
            iter_avg = result["iter_avg"]
            iter_variance = result["iter_variance"]
            iter_deviation = result["iter_deviation"]
            #Draw Graph
            self.graph.clear_all_line()
            self.graph.draw_path_by_tour(best_tour)

            #Draw chart
            if iteration == 0:
                #add new lines
                self.chartBestLength.add_new_line(iteration, best_tour_len)
                self.chartMeanLength.add_new_line(iteration, iter_avg)
                self.chartVarianceLength.add_new_line(iteration, iter_variance)
            else:
                #update lines
                self.chartBestLength.update_newest_line(iteration, best_tour_len)
                self.chartMeanLength.update_newest_line(iteration, iter_avg)
                self.chartVarianceLength.update_newest_line(iteration, iter_variance)


    def enableSpinBox(self):
        #global Knum, checkK
        if self.checkK.isChecked() == True:
            self.Knum.setDisabled(False)
        else:
            self.Knum.setDisabled(True)

    def test(self):
        self.animation2.setDuration(1000)
        self.animation2.setLoopCount(1)
        self.animation2.setStartValue(QColor(192,224,192))
        self.animation2.setKeyValueAt(0.12, QColor(192,192,192))
        self.animation2.setEndValue(QColor(212,208,200))
        self.animation2.start()