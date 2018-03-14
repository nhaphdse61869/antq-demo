#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

from PyQt5.QtGui import QFont, QStandardItemModel

from antQRun import AntQRun
from qgmap.common import QGoogleMap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from figure.chart import LengthChartCanvas, GraphCanvas
from antq.antQ import AntQ
from antq.antQGraph import AntQGraph


class Filter(QSlider):
    defaultK = 0
    filterCount = 0

    def __init__(self):
        super(Filter, self).__init__()
        self.numA = 0
        self.k = round(self.numA*0.6)

        # Label for the slider
        self.k_lbl = QLabel(str(self.k))

        # Increase the number of filters created
        Filter.filterCount += 1

        # Slider for the first OpenCV filter, with min, max, default and step values
        self.thresh_sld = QSlider(Qt.Horizontal, self)
        self.thresh_sld.setMinimum(round(self.numA*0.6))
        self.thresh_sld.setMaximum(self.numA)
        self.thresh_sld.setValue(self.k)


    def changeValue(self, value):
        # Function for setting the value of k1
        self.k = value
        self.thresh_sld.setValue(self.k)
        self.k_lbl.setText(str(self.k))

    def changeMax(self, value):
        self.k = round(value*0.6)
        self.thresh_sld.setMinimum(round(value * 0.6))
        self.thresh_sld.setMaximum(value)
        self.thresh_sld.setValue(self.k)


class ResultFrame(QWidget):
    FROM, TO, TIME = range(3)

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(1345, 0, 300, 680)
        self.dataGroupBox = QGroupBox("Result")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        model = self.createLogModel(self)
        self.dataView.setModel(model)
        self.addLog(model, 'A', 'B', '2h')
        self.addLog(model, 'B', 'C', '30m')
        self.addLog(model, 'C', 'D', '5m')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

    def createLogModel(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        model.setHeaderData(self.TO, Qt.Horizontal, "To")
        model.setHeaderData(self.TIME, Qt.Horizontal, "Time")
        return model

    def addLog(self, model, cofrom, to, time):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), cofrom)
        model.setData(model.index(0, self.TO), to)
        model.setData(model.index(0, self.TIME), time)


class OpenFileDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog()
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            data = json.load(open(fileName))
            global listMarker, numMarker, numOfAgents, graph
            for coord in data:
                numMarker += 1
                marker = {"latitude": coord['latitude'], "longitude": coord['longitude']}
                listMarker.append(marker)
                gmap.addMarker(str(numMarker), coord['latitude'], coord['longitude'], **dict(
                    title="Move me!"
                ))
                graph.add_coord((coord['latitude'],  coord['longitude']))
            numOfAgents.changeMax(numMarker)


if __name__ == '__main__':


    def onMarkerRClick(key):
        print("RClick on ", key)
        gmap.setMarkerOptions(key, draggable=False)

    def onMarkerLClick(key):
        print("LClick on ", key)

    def onMarkerDClick(key):
        print("DClick on ", key)
        gmap.setMarkerOptions(key, draggable=True)

    def onMapMoved(latitude, longitude):
        print("Moved to ", latitude, longitude)

    def onMapRClick(latitude, longitude):
        print("RClick on ", latitude, longitude)

    def onMapLClick(latitude, longitude):
        global numMarker, listMarker, numOfAgents
        numMarker += 1
        marker = {"latitude": latitude, "longitude": longitude}
        listMarker.append(marker)
        gmap.addMarker(str(numMarker), latitude, longitude, **dict(
            title="Move me!"
        ))
        graph.add_coord((latitude, longitude))
        numOfAgents.changeMax(numMarker)
        print("LClick on ", latitude, longitude)

    def onMapDClick(latitude, longitude):
        print("DClick on ", latitude, longitude)

    def showRoute():
        global listMarker
        gmap.directss(listMarker)

    def openFileDialog():
        ex = OpenFileDialog();

    app = QApplication(sys.argv)
    w = QDialog()
    h = QVBoxLayout()
    mainLayout = QVBoxLayout(w)
    l = QFormLayout()
    layout = QHBoxLayout()
    layout1 = QVBoxLayout()

    tabs2 = QTabWidget()
    tabGM = QWidget()
    tabGraph = QWidget()
    tabs2.addTab(tabGM, "Google Map")
    tabs2.addTab(tabGraph, "Graph")
    tabGM.layout = QVBoxLayout()
    tabGM.setLayout(tabGM.layout)
    h.addWidget(tabs2)

    tabs = QTabWidget()
    tab1 = QWidget()
    tab2 = QWidget()
    tabs.addTab(tab1, "Ant-Q")
    tabs.addTab(tab2, "Others")
    tab1.layout = QVBoxLayout()
    tab1.setLayout(tab1.layout)


    def valuechange(self,label):
        size = self.value()
        label.setFont(QFont("Arial",size))

    #Paramater Layout

    topParaLayout = QVBoxLayout()
    subTopParaLayoutUp = QHBoxLayout()
    subTopParaLayoutDown = QHBoxLayout()

    titleNum = QLabel("Number of Agents:")
    numOfAgents = Filter()
    numOfAgents.thresh_sld.valueChanged.connect(numOfAgents.changeValue)
    numText = numOfAgents.k_lbl
    subTopParaLayoutUp.addWidget(titleNum)
    subTopParaLayoutUp.addWidget(numText)
    subTopParaLayoutDown.addWidget(numOfAgents.thresh_sld)

    topParaLayout.addLayout(subTopParaLayoutUp)
    topParaLayout.addLayout(subTopParaLayoutDown)
    formContainer1 = QGroupBox("Weight Relative")
    formLayout = QFormLayout()
    deltaSpin = QSpinBox()
    deltaSpin.setMinimum(0)
    deltaSpin.setMaximum(101)
    deltaSpin.setValue(1)
    formLayout.addRow(QLabel("δ:"), deltaSpin)
    betaSpin = QSpinBox()
    betaSpin.setMinimum(0)
    betaSpin.setMaximum(100)
    betaSpin.setValue(2)
    formLayout.addRow(QLabel("β:"), betaSpin)
    formContainer1.setLayout(formLayout)

    formContainer2 = QGroupBox("Learning Rate")
    formLayout1 = QFormLayout()
    learningRate = QSpinBox()

    learningRate.setMinimum(0)
    learningRate.setMaximum(100)
    learningRate.setValue(10)
    formLayout1.addRow(QLabel("α:"), learningRate)
    formContainer2.setLayout(formLayout1)

    formContainer3 = QGroupBox("Discount Factor")
    formLayout2 = QFormLayout()
    discountFactor = QSpinBox()
    discountFactor.setMinimum(0)
    discountFactor.setMaximum(100)
    discountFactor.setValue(30)
    formLayout2.addRow(QLabel("ϒ:"), discountFactor)
    formContainer3.setLayout(formLayout2)

    formContainer4 = QGroupBox("Balance Rate")
    formLayout3 = QFormLayout()
    balanceRate = QSpinBox()
    balanceRate.setMinimum(0)
    balanceRate.setMaximum(100)
    balanceRate.setValue(90)
    formLayout3.addRow(QLabel("BR:"), balanceRate)
    formContainer4.setLayout(formLayout3)

    formContainer5 = QGroupBox("Iteration")
    formLayout4 = QFormLayout()
    iteration = QSpinBox()
    iteration.setMinimum(0)
    iteration.setMaximum(1000)
    iteration.setValue(200)
    formLayout4.addRow(QLabel("Iter:"), iteration)
    formContainer5.setLayout(formLayout4)

    paraLayoutH = QHBoxLayout()
    paraLayoutLeft = QVBoxLayout()
    paraLayoutRight = QVBoxLayout()
    paraLayoutH.addLayout(paraLayoutLeft)
    paraLayoutH.addLayout(paraLayoutRight)
    paraLayoutLeft.addWidget(formContainer1)
    paraLayoutLeft.addWidget(formContainer2)
    paraLayoutLeft.addWidget(formContainer3)
    paraLayoutRight.addWidget(formContainer4)
    paraLayoutRight.addWidget(formContainer5)

    tab1.layout.addLayout(topParaLayout)
    tab1.layout.addLayout(paraLayoutH)

    #Chart LINE
    chart = LengthChartCanvas()
    paraSample = QScrollArea()
    paraSample.setWidgetResizable(True)
    layout1.addWidget(chart)
    layout1.addWidget(paraSample)

    #Chart Graph
    graph = GraphCanvas(width=6, height=5, dpi=110)
    tabGraph.layout = QVBoxLayout()
    tabGraph.setLayout(tabGraph.layout)
    tabGraph.layout.addWidget(graph)
    tabGraph.layout.setSpacing(0)

    subLayout = QVBoxLayout()
    layout.addLayout(h)
    layout.addLayout(subLayout)
    ortherLayout = QHBoxLayout()


    topSubLayout = QHBoxLayout()
    topSubLayout.addWidget(tabs)
    topSubLayout.addLayout(ortherLayout)

    subLayout.addLayout(topSubLayout)


    #function buttons
    subLayout.addLayout(layout1)
    btn1 = QPushButton("Apply")
    btn2 = QPushButton("Run")
    btn3 = QPushButton("Test")
    btn4 = QPushButton("Generate")
    formButCon1 = QGroupBox()
    butLayout1 = QFormLayout()

    butLayout1.addWidget(btn1)
    butLayout1.addWidget(btn2)
    butLayout1.addWidget(btn3)
    butLayout2 = QFormLayout()
    butLayout2.addWidget(btn4)
    ortherLayout.setStretch(10,10)

    ortherLayout.addLayout(butLayout1)
    ortherLayout.addLayout(butLayout2)

    mainLayout.addLayout(layout)

    h.addLayout(l)
    numMarker = 0
    listMarker = []

    #GG Maps container

    gmap = QGoogleMap(w)
    gmap.mapMovedSignal.connect(onMapMoved)
    gmap.mapClickedSignal.connect(onMapLClick)
    gmap.mapDoubleClickedSignal.connect(onMapDClick)
    gmap.mapRightClickedSignal.connect(onMapRClick)
    gmap.markerClickedSignal.connect(onMarkerLClick)
    gmap.markerDoubleClickedSignal.connect(onMarkerDClick)
    gmap.markerRightClickedSignal.connect(onMarkerRClick)

    gmap.setSizePolicy(
        QSizePolicy.MinimumExpanding,
        QSizePolicy.MinimumExpanding)
    tabGM.layout.addWidget(gmap)

    componentRS = ResultFrame(w)
    componentRS.setWindowOpacity(1)
    showBtn = QPushButton("<", componentRS)
    showBtn.resize(30, 50)
    showBtn.move(0, 280)

    animation = QPropertyAnimation(componentRS, b"geometry")
    animation1 = QPropertyAnimation(componentRS, b"opacity")
    #animation
    def moveRs():
        global componentRS, animation, animation1,showBtn
        old_pos = QRect(1345, 0, 300, 680)
        if componentRS.pos().x()==old_pos.x():
            animation.setDuration(1000)
            animation.setStartValue(QRect(1345, 0, 300, 680))
            animation.setEndValue(QRect(1070, 0, 300, 680))
            animation.start()
            showBtn.setText(">")
        else:
            animation.setDuration(1000)
            animation.setStartValue(QRect(1070, 0, 300, 680))
            animation.setEndValue(QRect(1345, 0, 300, 680))
            animation.start()
            showBtn.setText("<")

    showBtn.clicked.connect(moveRs)
    #w.showFullScreen()
    w.setGeometry(0,40,0,0)
    w.resize(2600,0)
    w.show()
    gmap.waitUntilReady()

    gmap.setZoom(15)
    # center at HCM city
    gmap.centerAt(10.857200, 106.628487)
    # Some Static points
    for place in [
        "Plaza Ramon Castilla",
        "Plaza San Martin",
    ]:
        gmap.addMarkerAtAddress(place,
                                icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
                                )
    # gmap.setZoom(15)

    #Parameter to excute algorithm
    #default values
    delta = 1
    beta = 2
    Ite = 200
    numAgents = 2
    LR = 10
    DF = 30
    BR = 90

    def applyPara():
        global numOfAgents, deltaSpin, balanceRate, discountFactor, betaSpin, iteration, delta, beta, Ite, numAgents, LR, DF, BR
        delta = deltaSpin.value()
        beta = betaSpin.value()
        Ite = iteration.value()
        LR = learningRate.value()
        DF = discountFactor.value()
        BR = balanceRate.value()
        numAgents = numOfAgents.k


    def draw_chart(i, render_var, global_best):
        global chart, graph
        # Init chart line
        if i == 0:
            chart.add_new_line([i + 1], [render_var])
        else:
            chart.update_newest_line((i + 1), render_var)

        if i == Ite - 1:
            graph.draw_path_by_tour(global_best)

    #Implement Algorithm
    def runAlgorithm():
        global algEx
        global beta, delta, Ite, numAgents, LR, DF, BR
        matrix = gmap.convertTo2DArray(listMarker)
        algGraphEx = AntQGraph(matrix)
        algEx = AntQ(numAgents, Ite, algGraphEx, LR/100, DF/100, delta, beta, renderFunc=draw_chart)
        algEx.start()

    btn2.clicked.connect(showRoute)
    btn1.clicked.connect(applyPara)
    btn3.clicked.connect(runAlgorithm)
    btn4.clicked.connect(openFileDialog)

    sys.exit(app.exec_())
