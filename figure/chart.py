import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.paths = {}
        self.lines = []
        self.xmin = 0
        self.xmax = 10
        self.ymin = 0
        self.ymax = 10

        self.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax])

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def init_coord_data(self, points):
        prevPoint = points[0]
        for i in range(len(points)):
            self.add_coord(points[i])
            if i > 0:
                self.draw_line(prevPoint, points[i])
            prevPoint = points[i]

    def add_coord(self, point):
        # Update x, y min max
        if self.point[0] < self.xmin:
            self.xmin = self.point[0]
        if self.point[0] > self.xmax:
            self.xmax = self.point[0]
        if self.point[1] < self.ymin:
            self.ymin = self.point[1]
        if self.point[1] > self.ymax:
            self.ymax = self.point[1]

        # Update axis of axes
        self.axes.set_ylim(self.ymin, self.ymax)
        self.axes.set_xlim(self.xmin, self.xmax)

        #Draw marker
        self.axes.plot([self.point[0]], [self.point[1]], "ro")

    def clear_graph(self):
        self.axes.clear()

    def draw_line(self, p1, p2):
        path, = self.axes.plot([p1[0], p2[0]], [p1[1], p2[1]], "b-")
        self.paths[(p1, p2)] = path

    def change_path_apperance(self, p1, p2, alpha=None, color=None):
        if alpha != None:
            self.paths[(p1, p2)].set_alpha(alpha)
        if color != None:
            self.paths[(p1, p2)].set_color(color)
        self.draw()


class LengthChartCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.lines = []
        self.xmin = 0
        self.xmax = 10
        self.ymin = 0
        self.ymax = 10

        self.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax])

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_newest_line(self, x, y):
        if len(self.lines) == 0:
            return

        # Update x, y min max
        if x < self.xmin:
            self.xmin = x
        if x > self.xmax:
            self.xmax = x
        if y < self.ymin:
            self.ymin = y
        if y > self.ymax:
            self.ymax = y

        # Update axis of axes
        self.axes.set_ylim(self.ymin, self.ymax)
        self.axes.set_xlim(self.xmin, self.xmax)

        # Update line
        self.lines[-1].set_xdata(self.lines[-1].get_xdata(True).append(x))
        self.lines[-1].set_ydata(self.lines[-1].get_ydata(True).append(y))
        self.draw()

    def add_new_line(self, xdata, ydata):
        # Update x, y min max
        for i in range(len(xdata)):
            if xdata[i] < self.xmin:
                self.xmin = xdata[i]
            if xdata[i] > self.xmax:
                self.xmax = xdata[i]
        for i in range(len(ydata)):
            if ydata[i] < self.ymin:
                self.ymin = ydata[i]
            if ydata[i] > self.ymax:
                self.ymax = ydata[i]

        # Update axis of axes
        self.axes.set_ylim(self.ymin, self.ymax)
        self.axes.set_xlim(self.xmin, self.xmax)

        # Add new line
        aline, = self.axes.plot(xdata, ydata)
        self.lines.append(aline)
        return aline

    def clear_graph(self):
        self.lines.clear()
        self.axes.clear()
        self.xmin = 0
        self.xmax = 10
        self.ymin = 0
        self.ymax = 10
        self.axes.axis([self.xmin, self.xmax, self.ymin, self.ymax])