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


class GeoCoder(QNetworkAccessManager):
    class NotFoundError(Exception):
        pass

    @trace
    def __init__(self, parent):
        super(GeoCoder, self).__init__(parent)

    @trace
    def geocode(self, location):
        url = QUrl("http://maps.googleapis.com/maps/api/geocode/xml")

        query = QUrlQuery()
        query.addQueryItem("address", location)
        query.addQueryItem("sensor", "false")

        url.setQuery(query)
        """
        url = QUrl("http://maps.google.com/maps/geo/")
        url.addQueryItem("q", location)
        url.addQueryItem("output", "csv")
        url.addQueryItem("sensor", "false")
        """
        request = QNetworkRequest(url)
        reply = self.get(request)
        while reply.isRunning():
            QApplication.processEvents()

        reply.deleteLater()
        self.deleteLater()
        return self._parseResult(reply)

    @trace
    def _parseResult(self, reply):
        xml = reply.readAll()
        reader = QXmlStreamReader(xml)
        while not reader.atEnd():
            reader.readNext()
            if reader.name() != "geometry": continue
            reader.readNextStartElement()
            if reader.name() != "location": continue
            reader.readNextStartElement()
            if reader.name() != "lat": continue
            latitude = float(reader.readElementText())
            reader.readNextStartElement()
            if reader.name() != "lng": continue
            longitude = float(reader.readElementText())
            return latitude, longitude
        raise GeoCoder.NotFoundError


class QGoogleMap(QWebEngineView):
    mapMovedSignal = pyqtSignal(float, float)
    mapClickedSignal = pyqtSignal(float, float)
    mapRightClickedSignal = pyqtSignal(float, float)
    mapDoubleClickedSignal = pyqtSignal(float, float)

    markerMovedSignal = pyqtSignal(str, float, float)
    markerClickedSignal = pyqtSignal(str)
    markerDoubleClickedSignal = pyqtSignal(str)
    markerRightClickedSignal = pyqtSignal(str)

    @trace
    def __init__(self, parent, debug=True):
        super(QGoogleMap, self).__init__(parent)
        self.initialized = False
        self.loadFinished.connect(self.onLoadFinished)

        webchannel = QWebChannel(self.page())
        self.page().setWebChannel(webchannel)
        webchannel.registerObject("qtWidget", self)

        basePath = os.path.abspath(os.path.dirname(__file__))
        url = 'file:///' + basePath + '/qgmap.html'
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
    def geocode(self, location):
        return GeoCoder(self).geocode(location)

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
    def centerAtAddress(self, location):
        try:
            latitude, longitude = self.geocode(location)
        except GeoCoder.NotFoundError:
            return None, None
        self.centerAt(latitude, longitude)
        return latitude, longitude

    @trace
    def addMarkerAtAddress(self, location, **extra):
        if 'title' not in extra:
            extra['title'] = location
        try:
            latitude, longitude = self.geocode(location)
        except GeoCoder.NotFoundError:
            return None
        return self.addMarker(location, latitude, longitude, 0, **extra)

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
    def directss(self, listMarker, bestTour, cluster_number):
        return self.runScript(
            "displayAllRout({},{}, {});".format(listMarker,bestTour, cluster_number))

    @QtCore.pyqtSlot(str, float, float)
    def markerMoved(self, key, lat, long):
        self.markerMovedSignal.emit(key, lat, long)

    @QtCore.pyqtSlot(str)
    def markerClicked(self, str):
        self.markerClickedSignal.emit(str)

    @QtCore.pyqtSlot(str)
    def markerDoubleClicked(self, str):
        self.markerDoubleClickedSignal.emit(str)

    @QtCore.pyqtSlot(str)
    def markerRightClicked(self, str):
        self.markerRightClickedSignal.emit(str)

    @QtCore.pyqtSlot(float, float)
    def mapMoved(self, lat, long):
        self.mapMovedSignal.emit(lat, long)

    @QtCore.pyqtSlot(float, float)
    def mapClicked(self, lat, long):
        self.mapClickedSignal.emit(lat, long)

    @QtCore.pyqtSlot(float, float)
    def mapRightClicked(self, lat, long):
        self.mapRightClickedSignal.emit(lat, long)

    @QtCore.pyqtSlot(float, float)
    def mapDoubleClicked(self, lat, long):
        self.mapDoubleClickedSignal.emit(lat, long)

    def convertTo2DArray(self, listMarker):
        api_key = "AIzaSyCNHayAJYOTf-gi30fTgbA3SEXpjj3LDFM"
        gmaps = googlemaps.Client(key=api_key)

        dis_mat = [[1 for x in range(len(listMarker))] for y in range(len(listMarker))]
        for i in range(len(listMarker)):
            for j in range(len(listMarker)):
                if i == j :
                    dis_mat[i][j] = 0
                else :
                    duration = gmaps.distance_matrix(origins=(listMarker[i]['latitude'],listMarker[i]['longitude']),
                                                     destinations=(listMarker[j]['latitude'],listMarker[j]['longitude']),
                                                     mode="driving")
                    dis_mat[i][j] = duration['rows'][0]['elements'][0]['duration']['value']
                print(dis_mat)
        return dis_mat