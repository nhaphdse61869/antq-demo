from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
                          QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QSizePolicy, QHeaderView)


class RouteFrame(QWidget):
    NO1, FROM, NO2, TO, CLUSTER = range(5)

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Treeview Example - pythonspot.com'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.dataGroupBox = QGroupBox("Result")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.model = self.createRouteTable(self)
        self.dataView.setModel(self.model)
        myQHeaderView = self.dataView.header()
        myQHeaderView.resizeSection(0, 25)
        myQHeaderView.resizeSection(1, 190)
        myQHeaderView.resizeSection(2, 25)
        myQHeaderView.resizeSection(3, 190)
        #self.addRoute(self.model, 'A', 'A')

        mainLayout = QVBoxLayout()
        self.clusterCb = QComboBox()
        self.clusterCb.addItem("All")
        mainLayout.addWidget(self.clusterCb)
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)
        #self.clusterCb.currentIndexChanged.connect(self.selectedCluster)
        self.show()

    def createRouteTable(self, parent):
        model = QStandardItemModel(0, 5, parent)
        model.setHeaderData(self.NO1, Qt.Horizontal, "No")
        model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        model.setHeaderData(self.NO2, Qt.Horizontal, "No")
        model.setHeaderData(self.TO, Qt.Horizontal, "To")
        model.setHeaderData(self.CLUSTER, Qt.Horizontal, "Cluster number")
        return model

    def addRoute(self, model, noFrom, routeFrom, noTo, routeTo, cluster_number):
        root = self.dataView.model()
        n = root.rowCount()
        model.insertRow(n)
        model.setData(model.index(n, self.NO1), noFrom)
        model.setData(model.index(n, self.FROM), routeFrom)
        model.setData(model.index(n, self.NO2), noTo)
        model.setData(model.index(n, self.TO), routeTo)
        model.setData(model.index(n, self.CLUSTER), cluster_number)

    def clearAllRecords(self):
        root = self.dataView.model()
        root.removeRows(0, root.rowCount())

    def selectedCluster(self, pos):
        print(pos)