import sys
from antq.ant import Ant
import numpy as np
from PyQt5.QtCore import QThread

class AntQ(QThread):
    def __init__(self, number_of_ants, num_of_iteration, graph, aqchart, aqgraph, alpha=.1, gamma=.3, delta=1, beta=2, w=10):
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
        self.aqchart = aqchart
        self.aqgraph = aqgraph

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
        for i in range(0, len(self.best_tour)):
            r = self.best_tour[i]
            if i < len(self.best_tour) - 1:
                s = self.best_tour[i+1]
            else:
                s = self.best_tour[0]
            ant_q_val = (1 - self.alpha) * self.graph.antQ_val(r, s) + self.alpha * self.delay_val()
            self.graph.aq_mat[r][s] = ant_q_val

    def create_ants(self):
        nodes = list(range(0, self.graph.num_node))
        starting_nodes = np.random.choice(nodes, self.number_of_ants, replace=False)
        for i in range(0, self.number_of_ants):
            ant = Ant(i, self, starting_nodes[i])
            self.ants.append(ant)

    def run(self):
        for i in range(0, self.num_of_iteration):
            print("Iteration[%s]" % i)
            self.create_ants()
            for j in range(0, self.graph.num_node):
                for ant in self.ants:
                    ant.move()

            for ant in self.ants:
                if ant.tour_len < self.best_tour_len:
                    self.best_tour = ant.tour
                    self.best_tour_len = ant.tour_len
                    self.best_ant = ant.id
            self.delay_ant_q()
            # Init chart line
            if i == 0:
                self.aqchart.add_new_line([i+1],[self.best_tour_len])
            else:
                self.aqchart.update_newest_line((i + 1), self.best_tour_len)
            print("Iteration best: %s, %s, %s" % (self.best_tour, self.best_tour_len, self.best_ant,))
        self.aqgraph.draw_path_by_tour(self.best_tour)










