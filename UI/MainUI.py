
from PyQt5.QtGui import QFont, QStandardItemModel, QColor

from UI.BlinkingButton import StateWidget
from queue import Queue
import sys
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
        self.tabs.addTab(self.tab1, "Ant-Q")
        self.tabs.addTab(self.tab2, "Others")
        self.tab1.layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1.layout)
        # Paramater Layout

        self.topParaLayout = QVBoxLayout()
        self.subTopParaLayoutUp = QHBoxLayout()
        self.subTopParaLayoutDown = QHBoxLayout()

        self.titleNum = QLabel("Number of Agents:")
        self.numOfAgents = Filter()
        self.numOfAgents.thresh_sld.valueChanged.connect(self.numOfAgents.changeValue)
        self.numText = self.numOfAgents.k_lbl
        self.subTopParaLayoutUp.addWidget(self.titleNum)
        self.subTopParaLayoutUp.addWidget(self.numText)
        self.subTopParaLayoutDown.addWidget(self.numOfAgents.thresh_sld)

        self.topParaLayout.addLayout(self.subTopParaLayoutUp)
        self.topParaLayout.addLayout(self.subTopParaLayoutDown)
        self.formContainer1 = QGroupBox("Weight Relative")
        self.formLayout = QFormLayout()
        self.deltaSpin = QSpinBox()
        self.deltaSpin.setMinimum(0)
        self.deltaSpin.setMaximum(101)
        self.deltaSpin.setValue(1)
        self.formLayout.addRow(QLabel("δ:"), self.deltaSpin)
        self.betaSpin = QSpinBox()
        self.betaSpin.setMinimum(0)
        self.betaSpin.setMaximum(100)
        self.betaSpin.setValue(2)
        self.formLayout.addRow(QLabel("β:"), self.betaSpin)
        self.formContainer1.setLayout(self.formLayout)

        self.formContainer2 = QGroupBox("Learning Rate")
        self.formLayout1 = QFormLayout()
        self.learningRate = QSpinBox()

        self.learningRate.setMinimum(0)
        self.learningRate.setMaximum(100)
        self.learningRate.setValue(10)
        self.formLayout1.addRow(QLabel("α:"), self.learningRate)
        self.formContainer2.setLayout(self.formLayout1)

        self.formContainer3 = QGroupBox("Discount Factor")
        self.formLayout2 = QFormLayout()
        self.discountFactor = QSpinBox()
        self.discountFactor.setMinimum(0)
        self.discountFactor.setMaximum(100)
        self.discountFactor.setValue(30)
        self.formLayout2.addRow(QLabel("ϒ:"), self.discountFactor)
        self.formContainer3.setLayout(self.formLayout2)

        self.formContainer4 = QGroupBox("Balance Rate")
        self.formLayout3 = QFormLayout()
        self.balanceRate = QSpinBox()
        self.balanceRate.setMinimum(0)
        self.balanceRate.setMaximum(100)
        self.balanceRate.setValue(90)
        self.formLayout3.addRow(QLabel("BR:"), self.balanceRate)
        self.formContainer4.setLayout(self.formLayout3)

        self.formContainer5 = QGroupBox("Iteration")
        self.formLayout4 = QFormLayout()
        self.iteration = QSpinBox()
        self.iteration.setToolTip("Current Value:")
        self.iteration.setMinimum(0)
        self.iteration.setMaximum(1000)
        self.iteration.setValue(200)
        self.formLayout4.addRow(QLabel("Iter:"), self.iteration)
        self.formContainer5.setLayout(self.formLayout4)

        self.formContainer6 = QGroupBox("Clustering")
        self.formLayout5 = QFormLayout()
        self.Knum = QSpinBox()
        self.Knum.setMinimum(0)
        self.Knum.setMaximum(1000)
        self.Knum.setDisabled(True)
        self.checkK = QCheckBox()

        self.formLayout5.addRow(QLabel("Use:"), self.checkK)
        self.formLayout5.addRow(QLabel("K nums:"), self.Knum)
        self.formContainer6.setLayout(self.formLayout5)

        self.paraLayoutH = QHBoxLayout()
        self.paraLayoutLeft = QVBoxLayout()
        self.paraLayoutRight = QVBoxLayout()
        self.paraLayoutH.addLayout(self.paraLayoutLeft)
        self.paraLayoutH.addLayout(self.paraLayoutRight)
        self.paraLayoutLeft.addWidget(self.formContainer1)
        self.paraLayoutLeft.addWidget(self.formContainer2)
        self.paraLayoutLeft.addWidget(self.formContainer3)
        self.paraLayoutRight.addWidget(self.formContainer4)
        self.paraLayoutRight.addWidget(self.formContainer5)
        self.paraLayoutRight.addWidget(self.formContainer6)

        self.tab1.layout.addLayout(self.topParaLayout)
        self.tab1.layout.addLayout(self.paraLayoutH)

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

        #self.componentRS = ResultFrame(self)
        #self.componentRS.setWindowOpacity(1)
        #self.showBtn = QPushButton("<", self.componentRS)
        #self.showBtn.resize(30, 50)
        #self.showBtn.move(0, 280)

        #self.animation = QPropertyAnimation(self.componentRS, b"geometry")
        #self.animation1 = QPropertyAnimation(self.componentRS, b"opacity")
        self.animation2 = QPropertyAnimation(self.btn1, b"styleSheet")
        #self.showBtn.clicked.connect(self.moveRs)
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
        self.delta = 1
        self.beta = 2
        self.Ite = 200
        self.numAgents = 1
        self.LR = 10
        self.DF = 30
        self.BR = 90

        self.checkK.stateChanged.connect(self.enableSpinBox)

        self.btn2.clicked.connect(self.runAlgorithm)
        self.btn1.clicked.connect(self.applyPara)
        self.btn3.clicked.connect(self.test)
        self.btn4.clicked.connect(self.openFileDialog)
        #self.btn1.setGraphicsEffect()
        #self.show()


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
        self.numOfAgents.changeMax(self.numMarker)
        print("LClick on ", latitude, longitude)

    def onMapDClick(self, latitude, longitude):
        print("DClick on ", latitude, longitude)

    def showRoute(self, best_tour):
        #global listMarker
        self.gmap.directss(self.listMarker, best_tour)

    def openFileDialog(self):
        open = OpenFileDialog(self.listMarker, self.numMarker, self.graph, self.gmap)
        open.show()
        self.numOfAgents.changeMax(open.numMarker)
        self.numMarker = open.numMarker

    def valuechange(self, label):
        size = self.value()
        label.setFont(QFont("Arial", size))

    def applyPara(self):
        #global numOfAgents, deltaSpin, balanceRate, discountFactor, betaSpin, iteration, delta, beta, Ite, numAgents, LR, DF, BR
        self.delta = self.deltaSpin.value()
        self.beta = self.betaSpin.value()
        self.Ite = self.iteration.value()
        self.LR = self.learningRate.value()
        self.DF = self.discountFactor.value()
        self.BR = self.balanceRate.value()
        self.numAgents = self.numOfAgents.k

    # Implement Algorithm
    def runAlgorithm(self):
        if self.numMarker < 2:
            qm = QMessageBox
            qm.information(self,"", "Atleast two points!")
        else :
            self.applyPara()
            self.algorithm_result = Queue()
            matrix = self.gmap.convertTo2DArray(self.listMarker)
            sys.stdout.flush()
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