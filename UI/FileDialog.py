import json
import codecs

from PyQt5.QtWidgets import *
from UI.MainUI import *
from util.tsp import TSPFileReader
from util.atsp import ATSPReader
from util.gmap import GMapDataReader

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
            self.is_googlemap = False
            self.graph.clear_graph_tour()
            if fileName.lower().endswith('.atsp'):
                #Read atsp file
                reader = ATSPReader(fileName.strip())
                self.listMarker = reader.cities_tups
                self.numMarker += len(self.listMarker)

                self.dist_matrix = reader.dist_matrix

                # Draw graph
                for i in range(len(self.listMarker)):
                    self.graph.add_coord(self.listMarker[i])
                self.graph.draw_graph()

            elif fileName.lower().endswith('.tsp'):
                #Reader tsp file
                reader = TSPFileReader(fileName.strip())
                self.listMarker = reader.cities_tups
                self.numMarker += len(self.listMarker)
                self.dist_matrix = reader.dist_matrix
                # Draw graph
                for i in range(len(self.listMarker)):
                    self.graph.add_coord(self.listMarker[i])
                self.graph.draw_graph()

            elif fileName.lower().endswith('.json'):
                self.is_googlemap = True
                #Reader tsp file
                reader = GMapDataReader(fileName.strip())
                self.listMarker = reader.cities_tups
                self.numMarker += len(self.listMarker)
                self.dist_matrix = reader.dist_matrix
                self.list_address = reader.list_address
                # Draw graph
                for i in range(len(self.listMarker)):
                    self.graph.add_coord(self.listMarker[i])
                self.graph.draw_graph()
