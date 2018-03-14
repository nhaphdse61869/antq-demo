import json
from PyQt5.QtWidgets import *
from UI.MainUI import UIThread
import codecs

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
            data = json.load(codecs.open(fileName, 'r', 'utf-8-sig'))
            listMarker = UIThread.listMarker
            numMarker = UIThread.numMarker
            numOfAgents = UIThread.numOfAgents
            graph = UIThread.graph
            for coord in data:
                numMarker += 1
                marker = {"latitude": coord['latitude'], "longitude": coord['longitude']}
                listMarker.append(marker)
                gmap = UIThread.gmap
                gmap.addMarker(str(numMarker), marker['latitude'], marker['longitude'], **dict(
                    title="Move me!"
                ))
                graph.add_coord((marker['latitude'],  marker['longitude']))
            numOfAgents.changeMax(numMarker)