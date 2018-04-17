from ui.main.mainwindow import *
from ui.log.logwindow import *


class App(QMainWindow):
    log_window, main_window = range(2)
    def __init__(self):
        super().__init__()
        self.title = 'Ant-Q Demo Application'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.main_window = MainWindow()
        self.log_window = LogWindow()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        view_menu = main_menu.addMenu('View')

        exit_button = QAction(QIcon('exit24.png'), 'Exit', self)
        exit_button.setShortcut('Ctrl+E')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(self.close)
        self.main_ui_action = QAction(QIcon('exit24.png'), 'Main', self)
        self.main_ui_action.setShortcut('Ctrl+M')
        self.main_ui_action.setDisabled(True)
        self.log_ui_action = QAction(QIcon('img_418727.png'), 'Log', self)
        self.log_ui_action.setShortcut('Ctrl+L')
        file_menu.addAction(exit_button)
        view_menu.addAction(self.main_ui_action)
        view_menu.addAction(self.log_ui_action)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.main_window)
        self.stack.addWidget(self.log_window)

        self._widget = QWidget()
        self.layout = QVBoxLayout(self._widget)
        self.layout.addWidget(self.stack)
        self.setCentralWidget(self._widget)
        self.log_ui_action.triggered.connect(self.changeView)
        self.main_ui_action.triggered.connect(self.changeView)
        self.showMaximized()

    def changeView(self):
        if self.main_ui_action.isEnabled() == False:
            self.stack.setCurrentIndex(1)
            self.main_ui_action.setDisabled(False)
            self.log_ui_action.setDisabled(True)
            self.log_window.log_list_tree.loadListLog()
        else:
            self.stack.setCurrentIndex(0)
            self.main_ui_action.setDisabled(True)
            self.log_ui_action.setDisabled(False)