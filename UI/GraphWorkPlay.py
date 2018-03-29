from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UI.AntQTab import *
from UI.SimAnnealTab import *
from UI.ACOTab import *
from figure.chart import LengthChartCanvas, GraphCanvas

class GraphWP(QWidget):

    def __init__(self):
        super().__init__()
        self.layout1 = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab3, "Ant-Q")
        self.tabs.addTab(self.tab1, "ACO")
        self.tabs.addTab(self.tab2, "Simulated Annealing")
        # Ant-Q Parameter layout-------------------------------------------------------------
        self.tab3.layout = QVBoxLayout()
        self.tab3.setLayout(self.tab3.layout)
        self.antQParam = AntQTab()
        self.tab3.layout.addLayout(self.antQParam.topParaLayout)
        self.tab3.layout.addLayout(self.antQParam.paraLayoutH)
        # -----------------------------------------------------------------------------
        self.tab2.layout = QVBoxLayout()
        self.tab2.setLayout(self.tab2.layout)
        self.simAnnealParam = SimAnnealTab()
        self.tab2.layout.addLayout(self.simAnnealParam.firstLayout)
        self.tab2.layout.addLayout(self.simAnnealParam.secondLayout)
        # -----------------------------------------------------------------------------
        self.tab1.layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1.layout)
        self.acoParam = ACOTab()

        self.tab1.layout.addLayout(self.acoParam.topParaLayout)
        self.tab1.layout.addLayout(self.acoParam.paraLayoutH)
        # ------------------------------------------------------------------------
        # Chart LINE
        self.tabGraphs = QTabWidget()
        self.tabG1 = QWidget()
        self.tabG2 = QWidget()
        self.tabG3 = QWidget()
        self.chartBestLength = LengthChartCanvas()
        self.chartMeanLength = LengthChartCanvas()
        self.chartVarianceLength = LengthChartCanvas()

        self.tabGraphs.addTab(self.tabG1, "Best Length")
        self.tabGraphs.addTab(self.tabG2, "Mean Length")
        self.tabGraphs.addTab(self.tabG3, "Variance Length")

        self.tabG1.layout = QVBoxLayout()
        self.tabG1.setLayout(self.tabG1.layout)
        self.paraSample = QScrollArea()
        self.paraSample.setWidgetResizable(True)
        self.tabG1.layout.addWidget(self.chartBestLength)
        self.tabG1.layout.addWidget(self.paraSample)

        self.tabG2.layout = QVBoxLayout()
        self.tabG2.setLayout(self.tabG2.layout)
        self.paraSample = QScrollArea()
        self.paraSample.setWidgetResizable(True)
        self.tabG2.layout.addWidget(self.chartMeanLength)
        self.tabG2.layout.addWidget(self.paraSample)

        self.tabG3.layout = QVBoxLayout()
        self.tabG3.setLayout(self.tabG3.layout)
        self.paraSample = QScrollArea()
        self.paraSample.setWidgetResizable(True)
        self.tabG3.layout.addWidget(self.chartVarianceLength)
        self.tabG3.layout.addWidget(self.paraSample)

        self.layout1.addWidget(self.tabGraphs)

        # Chart Graph

        self.subLayout = QVBoxLayout()
        self.lefButParaLayout = QVBoxLayout()
        self.ortherLayout = QHBoxLayout()
        self.topSubLayout = QHBoxLayout()
        self.topSubLayout.addWidget(self.tabs)
        self.topSubLayout.addLayout(self.lefButParaLayout)
        self.subLayout.addLayout(self.topSubLayout)
        # function buttons
        self.subLayout.addLayout(self.layout1)
        # self.btn1 = StateWidget()
        self.btn1 = QPushButton("Apply")
        self.btn2 = QPushButton("Run")
        self.btn4 = QPushButton("Generate")
        # self.btn2.setStyleSheet("background-color: red")
        self.formButCon1 = QGroupBox()
        self.butLayout1 = QFormLayout()
        self.butLayout1.addWidget(self.btn1)
        self.butLayout1.addWidget(self.btn2)
        self.butLayout2 = QFormLayout()
        self.butLayout2.addWidget(self.btn4)
        self.lefButParaLayout.addLayout(self.ortherLayout)
        self.ortherLayout.setStretch(10, 10)
        self.ortherLayout.addLayout(self.butLayout1)
        self.ortherLayout.addLayout(self.butLayout2)
        self.paramContainer = QGroupBox("Current Parameter")
        self.paramLayout = QFormLayout()
        self.paramContainer.setLayout(self.paramLayout)
        self.lefButParaLayout.addWidget(self.paramContainer)
        self.setLayout(self.subLayout)

