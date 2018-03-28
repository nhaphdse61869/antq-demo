import sys

from PyQt5.QtCore import QThread, pyqtSignal

from antq.ant import Ant
import numpy as np


class AntQ(QThread):
    run_finished = pyqtSignal()
    def __init__(self, number_of_ants, num_of_iteration, graph, alpha=.1, gamma=.3, delta=1, beta=2, w=10, renderFunc=None, result_queue=None):
        QThread.__init__(self)
        self.number_of_ants = number_of_ants
        self.alpha = alpha
        self.gamma = gamma
        self.delta = delta
        self.beta = beta
        self.graph = graph
        self.num_of_iteration = num_of_iteration
        self.w = w
        self.best_tour = []
        self.best_tour_len = sys.maxsize
        self.best_ant = -1
        self.ants = []
        self.renderFunc = renderFunc
        self.list_best_tour = []
        self.list_best_len = []
        self.list_avg = []
        self.list_var = []
        self.list_dev = []
        self.result_queue = result_queue

    def delay_val(self):
        p_sum = 0
        for i in range(0, len(self.best_tour)):
            r = self.best_tour[i]
            if i < len(self.best_tour) - 1:
                s = self.best_tour[i+1]
            else:
                s = self.best_tour[0]
            p_sum += self.graph.distance(r, s)
        return self.w / p_sum

    def delay_ant_q(self):
        nodes_valid_from_r = self.best_tour[:]
        for i, node in enumerate(self.best_tour):
            r = node
            nodes_valid_from_r.remove(r)
            if i < len(self.best_tour) - 1:
                s = self.best_tour[i + 1]
                ant_q_val = (1 - self.alpha) * self.graph.antQ_val(r, s) + self.alpha * (
                        self.delay_val() + self.gamma * self.graph.max_aq(r, nodes_valid_from_r)[1])
            else:
                s = self.best_tour[0]
                ant_q_val = (1 - self.alpha) * self.graph.antQ_val(r, s) + self.alpha * self.delay_val()
            self.graph.aq_mat[r][s] = ant_q_val

    def create_ants(self):
        self.ants = []
        nodes = list(range(0, self.graph.num_node))
        starting_nodes = np.random.choice(nodes, self.number_of_ants)
        for i in range(0, self.number_of_ants):
            ant = Ant(i, self, starting_nodes[i])
            self.ants.append(ant)

    def iter_total(self):
        return sum(ant.tour_len for ant in self.ants)

    def iter_avg(self):
        return self.iter_total() / self.number_of_ants

    def local_variance(self, ant):
        return (ant.tour_len - self.iter_avg()) ** 2 / (self.number_of_ants - 1)

    def iter_variance(self):
        return sum(self.local_variance(ant) for ant in self.ants)

    def iter_deviation(self):
        variance = self.iter_variance()
        return np.math.sqrt(variance)

    def iter_run(self):
        self.create_ants()
        for j in range(0, self.graph.num_node):
            for ant in self.ants:
                ant.move()

        for ant in self.ants:
            if ant.tour_len < self.best_tour_len:
                self.best_tour = ant.tour
                self.best_tour_len = ant.tour_len
                self.best_ant = ant.id

        iter_avg = self.iter_avg()
        iter_variance = self.iter_variance()
        iter_deviation = self.iter_deviation()

        return iter_avg, iter_variance, iter_deviation

    def run(self):
        for i in range(0, self.num_of_iteration):
            print("Iteration[%s]" % i)
            iter_avg, iter_variance, iter_deviation = self.iter_run()
            self.delay_ant_q()

            #self.renderFunc(i, self.best_tour_len, self.best_tour, iter_avg, iter_variance, iter_deviation)
            #self.iteration_finished.emit(i, self.best_tour_len, self.best_tour, iter_avg, iter_variance, iter_deviation)
            aIter_result = {}
            aIter_result["iteration"] = i
            aIter_result["best_tour_len"] = self.best_tour_len
            aIter_result["best_tour"] = self.best_tour
            aIter_result["iter_avg"] = iter_avg
            aIter_result["iter_variance"] = iter_variance
            aIter_result["iter_deviation"] = iter_deviation
            self.result_queue.put(aIter_result)
            self.list_best_tour.append(self.best_tour)
            self.list_best_len.append(self.best_tour_len)
            self.list_avg.append(iter_avg)
            self.list_var.append(iter_variance)
            self.list_dev.append(iter_deviation)
        self.run_finished.emit()










