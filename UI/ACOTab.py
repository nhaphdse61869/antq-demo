from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from UI.Filter import Filter


class ACOTab(QWidget):

    def __init__(self):
        super().__init__()
        self.topParaLayout = QVBoxLayout()
        self.subTopParaLayoutUp = QHBoxLayout()
        self.subTopParaLayoutDown = QHBoxLayout()

        self.titleNum = QLabel("Number of Agents:")
        self.numOfAgents = Filter()
        self.numOfAgents.thresh_sld.valueChanged.connect(self.numOfAgents.changeValue)
        self.numText = self.numOfAgents.k_lbl
        self.subTopParaLayoutUp.addWidget(self.titleNum)
        self.subTopParaLayoutUp.addWidget(self.numText)
        self.subTopParaLayoutDown.addWidget(self.numOfAgents.thresh_sld)

        self.topParaLayout.addLayout(self.subTopParaLayoutUp)
        self.topParaLayout.addLayout(self.subTopParaLayoutDown)
        self.formContainer1 = QGroupBox("Weight Relative")
        self.formLayout = QFormLayout()
        self.deltaSpin = QSpinBox()
        self.deltaSpin.setMinimum(0)
        self.deltaSpin.setMaximum(101)
        self.deltaSpin.setValue(1)
        self.formLayout.addRow(QLabel("δ:"), self.deltaSpin)
        self.betaSpin = QSpinBox()
        self.betaSpin.setMinimum(0)
        self.betaSpin.setMaximum(100)
        self.betaSpin.setValue(2)
        self.formLayout.addRow(QLabel("β:"), self.betaSpin)
        self.formContainer1.setLayout(self.formLayout)

        self.formContainer2 = QGroupBox("Learning Rate")
        self.formLayout1 = QFormLayout()
        self.learningRate = QSpinBox()

        self.learningRate.setMinimum(0)
        self.learningRate.setMaximum(100)
        self.learningRate.setValue(10)
        self.formLayout1.addRow(QLabel("α:"), self.learningRate)
        self.formContainer2.setLayout(self.formLayout1)

        self.formContainer3 = QGroupBox("Discount Factor")
        self.formLayout2 = QFormLayout()
        self.discountFactor = QSpinBox()
        self.discountFactor.setMinimum(0)
        self.discountFactor.setMaximum(100)
        self.discountFactor.setValue(30)
        self.formLayout2.addRow(QLabel("ϒ:"), self.discountFactor)
        self.formContainer3.setLayout(self.formLayout2)

        self.formContainer4 = QGroupBox("Balance Rate")
        self.formLayout3 = QFormLayout()
        self.balanceRate = QSpinBox()
        self.balanceRate.setMinimum(0)
        self.balanceRate.setMaximum(100)
        self.balanceRate.setValue(90)
        self.formLayout3.addRow(QLabel("BR:"), self.balanceRate)
        self.formContainer4.setLayout(self.formLayout3)

        self.formContainer5 = QGroupBox("Iteration")
        self.formLayout4 = QFormLayout()
        self.iteration = QSpinBox()
        self.iteration.setMinimum(0)
        self.iteration.setMaximum(1000)
        self.iteration.setValue(200)
        self.formLayout4.addRow(QLabel("Iter:"), self.iteration)
        self.formContainer5.setLayout(self.formLayout4)

        self.formContainer6 = QGroupBox("Clustering")
        self.formLayout5 = QFormLayout()
        self.Knum = QSpinBox()
        self.Knum.setMinimum(1)
        self.Knum.setValue(1)
        self.Knum.setMaximum(1000)
        #self.Knum.setDisabled(True)
        #self.checkK = QCheckBox()

        #self.formLayout5.addRow(QLabel("Use:"), self.checkK)
        self.formLayout5.addRow(QLabel("K nums:"), self.Knum)
        self.formContainer6.setLayout(self.formLayout5)

        self.paraLayoutH = QHBoxLayout()
        self.paraLayoutLeft = QVBoxLayout()
        self.paraLayoutRight = QVBoxLayout()
        self.paraLayoutH.addLayout(self.paraLayoutLeft)
        self.paraLayoutH.addLayout(self.paraLayoutRight)
        self.paraLayoutLeft.addWidget(self.formContainer1)
        self.paraLayoutLeft.addWidget(self.formContainer2)
        self.paraLayoutLeft.addWidget(self.formContainer3)
        self.paraLayoutRight.addWidget(self.formContainer4)
        self.paraLayoutRight.addWidget(self.formContainer5)
        self.paraLayoutRight.addWidget(self.formContainer6)