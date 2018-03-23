import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from UI.MainUI import *
from UI.LogUI import *


class App(QMainWindow):
    LOG, MAIN = range(2)
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 menu - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.MAIN = UIThread()
        self.LOG = UILog()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        viewMenu = mainMenu.addMenu('View')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+E')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        self.mainUI = QAction(QIcon('exit24.png'), 'Main', self)
        self.mainUI.setShortcut('Ctrl+M')
        self.mainUI.setDisabled(True)
        self.logUI = QAction(QIcon('img_418727.png'), 'Log', self)
        self.logUI.setShortcut('Ctrl+L')
        fileMenu.addAction(exitButton)
        viewMenu.addAction(self.mainUI)
        viewMenu.addAction(self.logUI)

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.MAIN)
        self.Stack.addWidget(self.LOG)

        self._widget = QWidget()
        self.layout = QVBoxLayout(self._widget)
        self.layout.addWidget(self.Stack)
        self.setCentralWidget(self._widget)
        self.logUI.triggered.connect(self.changeView)
        self.mainUI.triggered.connect(self.changeView)
        self.showMaximized()

    def changeView(self):
        if self.mainUI.isEnabled() == False:
            self.Stack.setCurrentIndex(1)
            self.mainUI.setDisabled(False)
            self.logUI.setDisabled(True)
        else:
            self.Stack.setCurrentIndex(0)
            self.mainUI.setDisabled(True)
            self.logUI.setDisabled(False)