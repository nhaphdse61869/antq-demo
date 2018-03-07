#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

from PyQt5.QtGui import QFont, QStandardItemModel

from qgmap.common import QGoogleMap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *




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

        model = self.createMailModel(self)
        self.dataView.setModel(model)
        self.addMail(model, 'A', 'B', '2h')
        self.addMail(model, 'B', 'C', '30m')
        self.addMail(model, 'C', 'D', '5m')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

    def createMailModel(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        model.setHeaderData(self.TO, Qt.Horizontal, "To")
        model.setHeaderData(self.TIME, Qt.Horizontal, "Time")
        return model

    def addMail(self, model, cofrom, to, time):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), cofrom)
        model.setData(model.index(0, self.TO), to)
        model.setData(model.index(0, self.TIME), time)

    def moveRs(self):
        old_pos = QRect(1345, 0, 300, 680)
        new_pos = QRect(1060, 0, 300, 680)
        if self.pos().x()==old_pos.x():
            animation = QPropertyAnimation(self, b"geometry")
            animation.setDuration(10000)
            animation.setStartValue(QRect(1060, 0, 300, 680))
            animation.setEndValue(QRect(1345, 0, 300, 680))
            animation.start()
        else:
            animation = QPropertyAnimation(self, b"geometry")
            animation.setDuration(10000)
            animation.setStartValue(QRect(1345, 0, 300, 680))
            animation.setEndValue(QRect(1060, 0, 300, 680))
            animation.start()

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
            global listMarker, numMarker
            for coord in data:
                numMarker += 1
                marker = {"latitude": coord['latitude'], "longitude": coord['longitude']}
                listMarker.append(marker)
                gmap.addMarker(str(numMarker), coord['latitude'], coord['longitude'], **dict(
                    title="Move me!"
                ))


if __name__ == '__main__':

    def goCoords():
        def resetError():
            coordsEdit.setStyleSheet('')

        try:
            latitude, longitude = coordsEdit.text().split(",")
        except ValueError:
            coordsEdit.setStyleSheet("color: red;")
            QTimer.singleShot(500, resetError)
        else:
            gmap.centerAt(latitude, longitude)
            gmap.moveMarker("MyDragableMark", latitude, longitude)


    def goAddress():
        def resetError():
            addressEdit.setStyleSheet('')

        coords = gmap.centerAtAddress(addressEdit.text())
        if coords is None:
            addressEdit.setStyleSheet("color: red;")
            QTimer.singleShot(500, resetError)
            return
        gmap.moveMarker("MyDragableMark", *coords)
        coordsEdit.setText("{}, {}".format(*coords))

    def onMarkerMoved(key, latitude, longitude):
        print("Moved!!", key, latitude, longitude)
        coordsEdit.setText("{}, {}".format(latitude, longitude))

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
        global numMarker, listMarker
        numMarker += 1
        marker = {"latitude": latitude, "longitude": longitude}
        listMarker.append(marker)
        gmap.addMarker(str(numMarker), latitude, longitude, **dict(
            title="Move me!"
        ))
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
    tab1.layout = QFormLayout()
    tab1.setLayout(tab1.layout)


    def valuechange(self,label):
        size = self.value()
        label.setFont(QFont("Arial",size))

    addressEdit = QLineEdit()
    titleNum = QLabel("Number of Agents:")
    numOfAgents = QSlider(Qt.Horizontal)
    numOfAgents.setMinimum(0)
    numOfAgents.setMinimum(10)
    #numOfAgents.valueChanged.connect(valuechange(titleNum))
    tab1.layout.addWidget(titleNum)
    tab1.layout.addWidget(numOfAgents)
    coordsEdit = QLineEdit()


    coordsEdit.editingFinished.connect(goCoords)
    formContainer1 = QGroupBox("Weight Relative")
    formLayout = QFormLayout()
    formLayout.addRow(QLabel("δ:"), QSpinBox())
    formLayout.addRow(QLabel("β:"), QSpinBox())
    formContainer1.setLayout(formLayout)

    formContainer2 = QGroupBox("Learning Rate")
    formLayout1 = QFormLayout()
    learningRate = QSpinBox()
    learningRate.setMinimum(0)
    learningRate.setMaximum(100)
    formLayout1.addRow(QLabel("α:"), learningRate)
    formContainer2.setLayout(formLayout1)

    formContainer3 = QGroupBox("Discount Factor")
    formLayout2 = QFormLayout()
    discountFactor = QSpinBox()
    discountFactor.setMinimum(0)
    discountFactor.setMaximum(100)
    formLayout2.addRow(QLabel("ϒ:"), discountFactor)
    formContainer3.setLayout(formLayout2)

    tab1.layout.addWidget(formContainer1)
    tab1.layout.addWidget(formContainer2)
    tab1.layout.addWidget(formContainer3)


    chart = QGraphicsView()

    paraSample = QScrollArea()
    paraSample.setWidgetResizable(True)
    layout1.addWidget(chart)
    layout1.addWidget(paraSample)

    subLayout = QVBoxLayout()
    layout.addLayout(h)
    layout.addLayout(subLayout)
    ortherLayout = QHBoxLayout()


    topSubLayout = QHBoxLayout()
    topSubLayout.addWidget(tabs)
    topSubLayout.addLayout(ortherLayout)

    subLayout.addLayout(topSubLayout)

    subLayout.addLayout(layout1)
    #subLayout.addLayout()
    btn1 = QPushButton("Apply")
    btn2 = QPushButton("Run")
    btn4 = QPushButton("Generate")
    formButCon1 = QGroupBox()
    butLayout1 = QFormLayout()

    butLayout1.addWidget(btn1)
    butLayout1.addWidget(btn2)
    #formButCon1.setLayout(butLayout1)

    butLayout2 = QFormLayout()
    butLayout2.addWidget(btn4)
    ortherLayout.setStretch(10,10)

    ortherLayout.addLayout(butLayout1)
    ortherLayout.addLayout(butLayout2)
    btn4.clicked.connect(openFileDialog)

    mainLayout.addLayout(layout)

    h.addLayout(l)
    numMarker = 0
    listMarker = []

    btn2.clicked.connect(showRoute)
    gmap = QGoogleMap(w)
    gmap.mapMovedSignal.connect(onMapMoved)
    gmap.markerMovedSignal.connect(onMarkerMoved)
    gmap.mapClickedSignal.connect(onMapLClick)
    gmap.mapDoubleClickedSignal.connect(onMapDClick)
    gmap.mapRightClickedSignal.connect(onMapRClick)
    gmap.markerClickedSignal.connect(onMarkerLClick)
    gmap.markerDoubleClickedSignal.connect(onMarkerDClick)
    gmap.markerRightClickedSignal.connect(onMarkerRClick)
    #h.addWidget(gmap)

    gmap.setSizePolicy(
        QSizePolicy.MinimumExpanding,
        QSizePolicy.MinimumExpanding)
    tabGM.layout.addWidget(gmap)

    componentRS = ResultFrame(w)
    showBtn = QPushButton("<", componentRS)
    showBtn.resize(30, 50)
    showBtn.move(0, 280)
    showBtn.clicked.connect(componentRS.moveRs)

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

    sys.exit(app.exec_())
