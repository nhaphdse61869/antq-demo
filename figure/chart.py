import matplotlib

# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
import networkx as nx
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.tight_layout()
        self.points = []
        self.axes.set_axis_off()
        self.axes.autoscale_view()
        self.tour_edges = []
        self.G = nx.Graph()
        self.pos = {}
        self.pos_layout = {}

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def init_coord_data(self, points):
        for point in points:
            self.add_coord(point)

        self.draw_graph()

    def draw_graph(self):
        # Draw to network
        nx.draw_networkx_nodes(self.G, pos=self.pos_layout, node_size=20, node_color="red", ax=self.axes)
        nx.draw_networkx_edges(self.G, pos=self.pos_layout, alpha=0.1, ax=self.axes)
        # Draw to screen
        self.draw()

    def clear_graph_tour(self):
        self.axes.clear()
        self.axes.set_axis_off()
        self.draw()

    def add_coord(self, point):
        #Add point
        self.points.append((point[0], point[1]))
        self.G.add_node(str(len(self.points) - 1), pos=(point[0], point[1]))

        #Update position
        self.pos[str(len(self.points) - 1)] = (point[0], point[1])
        self.pos_layout = nx.spring_layout(G=self.G, pos=self.pos)

        #Add edge
        for i in range(len(self.points) - 1):
            self.G.add_edge(str(i), str(len(self.points) - 1))

    def draw_tour(self, tour):
        self.tour_edges = []
        # Add tour edge
        for i in range(len(tour) - 1):
            self.tour_edges.append((str(tour[i]), str(tour[i + 1])))
        self.tour_edges.append((str(tour[-1]), str(tour[0])))

        #Draw background graph
        nx.draw_networkx_nodes(self.G, pos=self.pos_layout, node_size=20, node_color="red", ax=self.axes)
        nx.draw_networkx_edges(self.G, pos=self.pos_layout, alpha=0.1, ax=self.axes)

        #Draw graph tour
        nx.draw_networkx_edges(self.G, pos=self.pos_layout, edgelist=self.tour_edges, alpha=1,
                               edge_color='blue', ax=self.axes)
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

class MultiLengthChartCanvas(FigureCanvas):
    def __init__(self, parent=None, number_of_chart=1, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.number_of_chart = number_of_chart
        self.list_axes = []

        for i in range(number_of_chart):
            axes = fig.add_subplot(1 , number_of_chart, i + 1)
            axes.autoscale()
            self.list_axes.append(axes)

        self.axes_lines = [[] for i in range(number_of_chart)]

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def add_new_line(self, chart_index ,xdata, ydata):
        # Add new line
        aline, = self.list_axes[chart_index].plot(xdata, ydata)
        self.axes_lines[chart_index].append(aline)
        self.draw()
        return aline

    def clear_graph(self):
        for i in range(self.number_of_chart):
            self.list_axes[i].clear()
            self.axes_lines[i].clear()

class ColumnChartCanvas(FigureCanvas):
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

    def create_bar(self, number_of_dataset, data_of_algorithms, name_of_algorithms):
        #X axis
        x_label = []
        for i in range(number_of_dataset):
            x_label.append("Dataset {}".format((i+1)))

        number_of_dataset = np.arange(number_of_dataset)

        for i in range(len(data_of_algorithms)):
            self.axes.bar(number_of_dataset + self.bar_width * i, data_of_algorithms[i], width= self.bar_width, align='center', label=name_of_algorithms[i])

        self.axes.set_xlabel("Algorithm")
        self.axes.set_ylabel("Length")
        self.axes.set_xticks(number_of_dataset + (self.bar_width/2) * (len(name_of_algorithms) - 1))
        self.axes.set_xticklabels(x_label)
        self.axes.legend()
        self.draw()