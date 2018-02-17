#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QFont

from qgmap.common import QGoogleMap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


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
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

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
    # l1 = QFormLayout()
    layout = QHBoxLayout()
    layout1 = QHBoxLayout()

    btn = QPushButton("Show route")
    btnS = QPushButton("Generate")
    l.addWidget(btn)
    l.addWidget(btnS)

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
    layout1.addWidget(chart)

    subLayout = QVBoxLayout()
    layout.addLayout(h)
    layout.addLayout(subLayout)
    ortherLayout = QHBoxLayout()
    subLayout.addWidget(tabs)
    subLayout.addLayout(ortherLayout)
    btn1 = QPushButton("Apply")
    btn2 = QPushButton("Run")
    btn3 = QPushButton("Stop")
    btn4 = QPushButton("Generate")
    formButCon1 = QGroupBox()
    butLayout1 = QFormLayout()

    butLayout1.addWidget(btn1)
    butLayout1.addWidget(btn2)
    butLayout1.addWidget(btn3)
    #formButCon1.setLayout(butLayout1)

    butLayout2 = QFormLayout()
    butLayout2.addWidget(btn4)
    #ortherLayout.addWidget(btn1)
    #ortherLayout.addWidget(btn2)
    #ortherLayout.addWidget(btn3)
    #ortherLayout.addWidget(btn4)
    ortherLayout.setStretch(10,10)
    ortherLayout.addLayout(butLayout1)
    ortherLayout.addLayout(butLayout2)
    btn4.clicked.connect(openFileDialog)

    mainLayout.addLayout(layout)
    mainLayout.addLayout(layout1)

    h.addLayout(l)
    numMarker = 0
    listMarker = []

    btn.clicked.connect(showRoute)
    gmap = QGoogleMap(w)
    gmap.mapMovedSignal.connect(onMapMoved)
    gmap.markerMovedSignal.connect(onMarkerMoved)
    gmap.mapClickedSignal.connect(onMapLClick)
    gmap.mapDoubleClickedSignal.connect(onMapDClick)
    gmap.mapRightClickedSignal.connect(onMapRClick)
    gmap.markerClickedSignal.connect(onMarkerLClick)
    gmap.markerDoubleClickedSignal.connect(onMarkerDClick)
    gmap.markerRightClickedSignal.connect(onMarkerRClick)
    h.addWidget(gmap)

    gmap.setSizePolicy(
        QSizePolicy.MinimumExpanding,
        QSizePolicy.MinimumExpanding)
    #w.showFullScreen()
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
