from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class SimAnnealTab(QWidget):

    def __init__(self):
        super().__init__()
        self.firstLayout = QGridLayout()
        self.secondLayout = QVBoxLayout()

        self.temperInit = QSpinBox()
        self.temperEnd = QSpinBox()
        self.firstLayout.addWidget(QLabel('T_0'),0,0)
        self.firstLayout.addWidget(self.temperInit, 0, 1)
        self.firstLayout.addWidget(QLabel('T_min'), 0, 2)
        self.firstLayout.addWidget(self.temperEnd, 0, 3)

        self.formContainer1 = QGroupBox()
        self.formLayout = QFormLayout()
        self.iterSpin = QSpinBox()
        self.iterSpin.setMinimum(0)
        self.iterSpin.setMaximum(100)
        self.iterSpin.setValue(1)
        self.formLayout.addRow(QLabel("Iter:"), self.iterSpin)
        self.betaSpin = QSpinBox()
        self.betaSpin.setMinimum(0)
        self.betaSpin.setMaximum(100)
        self.betaSpin.setValue(2)
        self.formLayout.addRow(QLabel("β:"), self.betaSpin)
        self.formContainer1.setLayout(self.formLayout)
        self.formContainer6 = QGroupBox("Clustering")
        self.formLayout5 = QFormLayout()
        self.Knum = QSpinBox()
        self.Knum.setMinimum(1)
        self.Knum.setValue(1)
        self.Knum.setMaximum(1000)
        self.formLayout5.addRow(QLabel("K nums:"), self.Knum)
        self.formContainer6.setLayout(self.formLayout5)
        self.secondLayout.addWidget(self.formContainer1)
        self.secondLayout.addWidget(self.formContainer6)

