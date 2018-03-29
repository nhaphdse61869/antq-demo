from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
                          QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget, QSizePolicy, QHeaderView)


class RouteFrame(QWidget):
    NO1, FROM, NO2, TO = range(4)

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
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

        self.show()

    def createRouteTable(self, parent):
        model = QStandardItemModel(0, 4, parent)
        model.setHeaderData(self.NO1, Qt.Horizontal, "No")
        model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        model.setHeaderData(self.NO2, Qt.Horizontal, "No")
        model.setHeaderData(self.TO, Qt.Horizontal, "To")
        return model

    def addRoute(self, model, routeFrom, routeTo):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), routeFrom)
        model.setData(model.index(0, self.TO), routeTo)

    def clearAllRecords(self):
        root = self.dataView.model()
        root.removeRows(0, root.rowCount())