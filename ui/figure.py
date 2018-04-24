import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

import numpy as np
import time
import traceback
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

class AnimationGraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, animation_speed=1):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_off()
        self.axes.autoscale_view()

        self.draw_done = True
        self.max_frame = 0
        self.animation_speed = animation_speed

        self.list_point = []
        self.list_annotation = []
        self.scatter = self.axes.scatter([],[])
        self.animation_animation = None

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def initCoordData(self, list_point):
        try:
            self.list_point = list_point

            for i in range(len(list_point)):
                anno = self.axes.annotate(str(i + 1), list_point[i])
                self.list_annotation.append(anno)

            list_x, list_y = self.getListXListY(list_point)
            self.scatter = self.axes.scatter(list_x, list_y)
            self.draw()
        except:
            traceback.print_exc()

    def getListXListY(self, list_point):
        list_x = []
        list_y = []
        for i in range(len(list_point)):
            list_x.append(list_point[i][0])
            list_y.append(list_point[i][1])
        return list_x, list_y

    def updateCluster(self, clusters_point):
        self.clusters_point = clusters_point
        list_x, list_y = self.getListXListY(self.list_point)

        self.point_cluster = [0 for x in range(len(self.list_point))]
        for cluster_number in range(len(clusters_point)):
            for i in range(len(clusters_point[cluster_number])):
                self.point_cluster[clusters_point[cluster_number][i]] = cluster_number

        self.list_line = []
        for cluster_number in range(len(clusters_point)):
            line, = self.axes.plot([],[])
            self.list_line.append(line)
        self.scatter = self.axes.scatter(list_x, list_y, c=self.point_cluster)
        self.axes.set_axis_off()
        self.draw()

    def updateClusterGraph(self, clusters_best_tour, animate=False):
        try:
            self.max_frame = 0
            clusters_list_x = []
            clusters_list_y = []
            clusters_color = []
            self.draw_done = False
            for cluster_number in range(len(clusters_best_tour)):
                # Get cluster color
                c = self.scatter.to_rgba(cluster_number)
                # Get number of max point
                if len(clusters_best_tour[cluster_number]) > self.max_frame:
                    self.max_frame = len(clusters_best_tour[cluster_number])
                # Get best tour list
                list_x = []
                list_y = []
                for i in range(len(clusters_best_tour[cluster_number])):
                    # Color index
                    x = self.list_point[self.clusters_point[cluster_number][clusters_best_tour[cluster_number][i]]][0]
                    y = self.list_point[self.clusters_point[cluster_number][clusters_best_tour[cluster_number][i]]][1]
                    list_x.append(x)
                    list_y.append(y)

                x = self.list_point[self.clusters_point[cluster_number][clusters_best_tour[cluster_number][0]]][0]
                y = self.list_point[self.clusters_point[cluster_number][clusters_best_tour[cluster_number][0]]][1]
                list_x.append(x)
                list_y.append(y)

                clusters_list_x.append(list_x)
                clusters_list_y.append(list_y)
                clusters_color.append(c)

            self.max_frame += 2
            max_point = self.max_frame

            if animate:
                for num in range(max_point):
                    self.animateClusterGraph(num, clusters_list_x, clusters_list_y, clusters_color)
                    self.draw()
                    time.sleep(self.animation_speed/max_point)
            else:
                for i in range(len(clusters_list_x)):
                    self.list_line[i].set_data(clusters_list_x[i], clusters_list_y[i])
                    self.list_line[i].set_color(clusters_color[i])
                    self.draw_done = True
                    self.draw()

        except:
            traceback.print_exc()

    def animateClusterGraph(self, num, clusters_list_x, clusters_list_y, clusters_color):
        for i in range(len(clusters_list_x)):
            if (num <= len(clusters_list_x[i])):
                self.list_line[i].set_data(clusters_list_x[i][:num], clusters_list_y[i][:num])
                self.list_line[i].set_color(clusters_color[i])

        if num == self.max_frame - 1:
            self.draw_done = True

    def clearGraph(self):
        self.axes.clear()
        self.axes.set_axis_off()
        self.draw()

class SingleLineChart(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, title=""):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.lines = []
        self.axes.set_title(title)
        self.axes.autoscale()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateNewestLine(self, x, y):
        if len(self.lines) == 0:
            return

        # Update line
        self.lines[-1].set_xdata(np.append(self.lines[-1].get_xdata(),[x]))
        self.lines[-1].set_ydata(np.append(self.lines[-1].get_ydata(),[y]))
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.draw()

    def addNewLine(self, xdata, ydata):
        # Add new line
        aline, = self.axes.plot(xdata, ydata)
        self.lines.append(aline)
        self.draw()
        return aline

    def clearChart(self):
        self.lines.clear()
        self.axes.clear()

class MultiLineChart(FigureCanvas):
    def __init__(self, parent=None, number_of_chart=1, width=5, height=4, dpi=100, list_chart_name=[]):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.number_of_chart = number_of_chart
        self.list_axes = []

        for i in range(number_of_chart):
            axes = self.fig.add_subplot(1 , number_of_chart, i + 1)
            axes.autoscale()
            self.list_axes.append(axes)

        for i in range(len(list_chart_name)):
            self.list_axes[i].set_title(list_chart_name[i])

        self.axes_lines = [[] for i in range(number_of_chart)]

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def addNewLine(self, chart_index, xdata, ydata):
        # Add new line
        aline, = self.list_axes[chart_index].plot(xdata, ydata)
        self.axes_lines[chart_index].append(aline)
        self.draw()
        return aline

    def clearChart(self):
        for i in range(self.number_of_chart):
            self.list_axes[i].clear()
            self.axes_lines[i].clear()

    def setLegend(self, list_legend):
        self.fig.legend(self.axes_lines[0], list_legend)

class ColumnChart(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.autoscale_view()
        self.bar_width = 0.2

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def createColumn(self, number_of_dataset, data_of_algorithms, name_of_algorithms):
        #X axis
        x_label = []
        for i in range(number_of_dataset):
            x_label.append("Dataset {}".format((i+1)))

        number_of_dataset = np.arange(number_of_dataset)

        for i in range(len(data_of_algorithms)):
            self.axes.bar(number_of_dataset + self.bar_width * i, data_of_algorithms[i], width= self.bar_width, align='center', label=name_of_algorithms[i])

        self.axes.set_ylabel("Length")
        self.axes.set_xticks(number_of_dataset + (self.bar_width/2) * (len(name_of_algorithms) - 1))
        self.axes.set_xticklabels(x_label)
        self.axes.legend()
        self.draw()