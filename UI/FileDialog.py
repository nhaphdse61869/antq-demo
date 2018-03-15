import json
import codecs

from PyQt5.QtWidgets import *
from UI.MainUI import *

class OpenFileDialog(QWidget):

    def __init__(self, listMarker, numMarker, graph, gmap):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.listMarker = listMarker
        self.numMarker = numMarker
        self.graph = graph
        self.gmap = gmap
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
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
                #self.numOfAgents.changeMax(UIThread.numMarker)