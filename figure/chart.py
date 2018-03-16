import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt


class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.tight_layout()
        self.paths = {}
        self.points = []
        self.axes.set_axis_off()
        self.axes.autoscale_view()

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
                self.draw_path(prevPoint, points[i])
            prevPoint = points[i]
        if len(points) > 2:
            self.draw_line(points[-1], points[0])
        self.draw()

    def add_coord(self, point):
        self.axes.plot([point[0]], [point[1]], "ro")
        self.points.append(point)
        self.draw()

    def clear_graph(self):
        self.axes.clear()
        self.draw()

    def clear_all_line(self):
        for path in self.paths.values():
            path.remove()
        self.draw()

    def draw_path_by_tour(self, tour):
        for i in range(len(tour)):
            p1 = self.points[tour[i]]
            p2 = self.points[tour[0]]
            if i < (len(tour) - 1):
                p2 = self.points[tour[i+1]]
            self.draw_path(p1, p2)

    def draw_path(self, p1, p2):
        path, = self.axes.plot([p1[0], p2[0]], [p1[1], p2[1]], "b-")
        self.paths[(p1, p2)] = path
        self.draw()

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

        self.axes.autoscale()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_newest_line(self, x, y):
        if len(self.lines) == 0:
            return

        # Update line
        self.lines[-1].set_xdata(np.append(self.lines[-1].get_xdata(),[x]))
        self.lines[-1].set_ydata(np.append(self.lines[-1].get_ydata(),[y]))
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.draw()

    def add_new_line(self, xdata, ydata):
        # Add new line
        aline, = self.axes.plot(xdata, ydata)
        self.lines.append(aline)
        self.draw()
        return aline

    def clear_graph(self):
        self.lines.clear()
        self.axes.clear()