from PyQt5.QtGui import QIcon

from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
                          QTime)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QTreeView, QVBoxLayout,
                             QWidget)


class RouteFrame(QWidget):
    FROM, TO = range(2)

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Treeview Example - pythonspot.com'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.dataGroupBox = QGroupBox("Inbox")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.model = self.createRouteTable(self)
        self.dataView.setModel(self.model)
        self.addRoute(self.model, 'A', 'A')

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

        self.show()

    def createRouteTable(self, parent):
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        model.setHeaderData(self.TO, Qt.Horizontal, "TO")
        return model

    def addRoute(self, model, routeFrom, routeTo):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), routeFrom)
        model.setData(model.index(0, self.TO), routeTo)

    def clearAllRecords(self):
        root = self.dataView.model()
        root.removeRows(0, root.rowCount())