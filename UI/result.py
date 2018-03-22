from PyQt5.QtCore import QThread
from queue import Empty
import time

class ResultHandler(QThread):
    def __init__(self, graph, charts, algorithm, result_queue):
        QThread.__init__(self)
        self.graph = graph
        self.charts = charts
        self.algorithm = algorithm
        self.result_queue = result_queue

    def show_antq_result(self, result):
        #Get result parameter
        iteration = result["iteration"]
        best_tour_len = result["best_tour_len"]
        best_tour = result["best_tour"]
        iter_avg = result["iter_avg"]
        iter_variance = result["iter_variance"]
        iter_deviation = result["iter_deviation"]

        #Draw Graph
        self.graph.clear_all_line()
        self.graph.draw_path_by_tour(best_tour)

        #Draw chart
        if iteration == 0:
            #add new lines
            self.charts["bestLength"].add_new_line(iteration, best_tour_len)
            self.charts["meanLength"].add_new_line(iteration, iter_avg)
            self.charts["varianceLength"].add_new_line(iteration, iter_variance)
        else:
            #update lines
            self.charts["bestLength"].update_newest_line(iteration, best_tour_len)
            self.charts["meanLength"].update_newest_line(iteration, iter_avg)
            self.charts["varianceLength"].update_newest_line(iteration, iter_variance)

    def run(self):
        while True:
            try:
                result = self.result_queue.get(block=False, timeout=2)
                if self.algorithm == "antq":
                    self.show_antq_result(result)
            except Empty:
                pass




