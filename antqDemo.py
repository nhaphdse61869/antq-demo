#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from qgmap.common import QGoogleMap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


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
        for i in range(len(listMarker)):
            if i > 0:
                gmap.directss(listMarker[i - 1]["latitude"],
                              listMarker[i - 1]["longitude"],
                              listMarker[i]["latitude"],
                              listMarker[i]["longitude"])

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

    addressEdit = QLineEdit()
    gamma = QSpinBox()
    tab1.layout.addWidget(gamma)
    addressEdit.editingFinished.connect(goAddress)
    coordsEdit = QLineEdit()
    tab1.layout.addRow('Coords:', coordsEdit)
    coordsEdit.editingFinished.connect(goCoords)

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
    ortherLayout.addWidget(btn1)
    ortherLayout.addWidget(btn2)
    ortherLayout.addWidget(btn3)
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
    w.showFullScreen()

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
