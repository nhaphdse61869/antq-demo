from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QGroupBox, QTreeView, QHBoxLayout, QVBoxLayout


class ResultFrame(QWidget):
    FROM, TO, TIME = range(3)
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(1345, 0, 300, 680)
        self.dataGroupBox = QGroupBox("Result")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        model = self.createLogModel(self)
        self.dataView.setModel(model)
        self.addLog(model, 'A', 'B', '2h')
        self.addLog(model, 'B', 'C', '30m')
        self.addLog(model, 'C', 'D', '5m')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

    def createLogModel(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        model.setHeaderData(self.TO, Qt.Horizontal, "To")
        model.setHeaderData(self.TIME, Qt.Horizontal, "Time")
        return model

    def addLog(self, model, cofrom, to, time):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), cofrom)
        model.setData(model.index(0, self.TO), to)
        model.setData(model.index(0, self.TIME), time)