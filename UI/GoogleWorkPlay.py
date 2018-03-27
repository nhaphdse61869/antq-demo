from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from UI.RouteFrame import *
from UI.ResultFrame import *


class GoogkeWP(QWidget):

    def __init__(self):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.botLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.botLayout)
        self.paramContainer = QGroupBox("Parameter")
        self.paramLayout = QFormLayout()
        self.paramContainer.setLayout(self.paramLayout)
        self.topLeftLayout = QVBoxLayout()
        self.paramContainer.setFixedHeight(400)
        self.paramContainer.setFixedWidth(200)
        self.topRightLayout = QVBoxLayout()
        self.topLeftLayout.addWidget(self.paramContainer)
        self.rsFrame = ResultFrame(self)
        self.viewLogListBtn = QPushButton("View Logs")
        self.showRoute = QPushButton("Run")
        self.topRightLayout.addWidget(self.rsFrame)
        self.topRightLayout.addWidget(self.showRoute)
        self.topLayout.addLayout(self.topLeftLayout)
        self.topLayout.addLayout(self.topRightLayout)
        self.routeFrame = RouteFrame()
        self.botLayout.addWidget(self.routeFrame)
        self.setLayout(self.mainLayout)

