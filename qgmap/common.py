import googlemaps

doTrace = False

import json
import os

import decorator

from PyQt5.QtCore import pyqtSignal, QUrl, QUrlQuery, QXmlStreamReader
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from PyQt5.QtWebChannel import QWebChannel


@decorator.decorator
def trace(function, *args, **k):
    """Decorates a function by tracing the begining and
    end of the function execution, if doTrace global is True"""

    if doTrace: print("> " + function.__name__, args, k)
    result = function(*args, **k)
    if doTrace: print("< " + function.__name__, args, k, "->", result)
    return result


class _LoggedPage(QWebEnginePage):
    @trace
    def javaScriptConsoleMessage(self, msg, line, source):
        print('JS: %s line %d: %s' % (source, line, msg))


class QGoogleMap(QWebEngineView):
    map_moved_signal = pyqtSignal(float, float)
    map_clicked_signal = pyqtSignal(float, float)
    map_right_clicked_signal = pyqtSignal(float, float)
    map_double_clicked_signal = pyqtSignal(float, float)

    marker_moved_signal = pyqtSignal(str, float, float)
    marker_clicked_signal = pyqtSignal(str)
    marker_double_clicked_signal = pyqtSignal(str)
    marker_right_clicked_signal = pyqtSignal(str)

    @trace
    def __init__(self, parent, debug=True):
        super(QGoogleMap, self).__init__(parent)
        self.initialized = False
        self.loadFinished.connect(self.onLoadFinished)

        web_channel = QWebChannel(self.page())
        self.page().setWebChannel(web_channel)
        web_channel.registerObject("qtWidget", self)

        base_path = os.path.abspath(os.path.dirname(__file__))
        url = 'file:///' + base_path + '/qgmap.html'
        url = str(url.replace("\\","/"))
        print (url)
        self.load(QUrl(url))

    @trace
    def onLoadFinished(self, ok):
        if self.initialized: return
        if not ok:
            print("Error initializing Google Maps")
        self.initialized = True
        self.centerAt(0, 0)
        self.setZoom(1)

    @trace
    def waitUntilReady(self):
        while not self.initialized:
            QApplication.processEvents()

    @trace
    def runScript(self, script):
        return self.page().runJavaScript(script)

    @trace
    def centerAt(self, latitude, longitude):
        self.runScript("gmap_setCenter({},{})".format(latitude, longitude))

    @trace
    def setZoom(self, zoom):
        self.runScript("gmap_setZoom({})".format(zoom))

    @trace
    def center(self):
        center = self.runScript("gmap_getCenter()")
        return center.lat, center.lng

    @trace
    def addMarker(self, key, latitude, longitude, cluster_number, **extra):
        return self.runScript(
            "gmap_addMarker("
            "key={!r}, "
            "latitude={}, "
            "longitude={}, "
            "cluster_number={}, "
            "{}"
            "); "
                .format(key, latitude, longitude, cluster_number, json.dumps(extra)))

    @trace
    def moveMarker(self, key, latitude, longitude):
        return self.runScript(
            "gmap_moveMarker({!r}, {}, {});".format(key, latitude, longitude))

    @trace
    def setMarkerOptions(self, keys, **extra):
        return self.runScript(
            "gmap_changeMarker("
            "key={!r}, "
            "{}"
            "); "
                .format(keys, json.dumps(extra)))

    @trace
    def deleteMarker(self, key):
        return self.runScript(
            "gmap_deleteMarker("
            "key={!r} "
            "); ".format(key))

    @trace
    def clearAllMarker(self):
        return self.runScript("deleteMarkers()")

    @trace
    def clearAllRoute(self):
        return self.runScript("clearAllRoute()")

    @trace
    def createRoute(self, list_marker, best_tour, cluster_number):
        return self.runScript(
            "displayAllRout({},{}, {});".format(list_marker, best_tour, cluster_number))

    @QtCore.pyqtSlot(str, float, float)
    def markerMoved(self, key, lat, long):
        self.marker_moved_signal.emit(key, lat, long)

    @QtCore.pyqtSlot(str)
    def markerClicked(self, str):
        self.marker_clicked_signal.emit(str)

    @QtCore.pyqtSlot(str)
    def markerDoubleClicked(self, str):
        self.marker_double_clicked_signal.emit(str)

    @QtCore.pyqtSlot(str)
    def markerRightClicked(self, str):
        self.marker_right_clicked_signal.emit(str)

    @QtCore.pyqtSlot(float, float)
    def mapMoved(self, lat, long):
        self.map_moved_signal.emit(lat, long)

    @QtCore.pyqtSlot(float, float)
    def mapClicked(self, lat, long):
        self.map_clicked_signal.emit(lat, long)

    @QtCore.pyqtSlot(float, float)
    def mapRightClicked(self, lat, long):
        self.map_right_clicked_signal.emit(lat, long)

    @QtCore.pyqtSlot(float, float)
    def mapDoubleClicked(self, lat, long):
        self.map_double_clicked_signal.emit(lat, long)