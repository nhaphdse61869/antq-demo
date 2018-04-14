import queue
import sys

from PyQt5.QtCore import QThread
from queue import Queue
import numpy as np

import random
import math


class AntQ(QThread):
    def __init__(self, number_of_ants, num_of_iteration, graph, alpha=.1, gamma=.3, delta=1, beta=2, w=10, global_best=True, result=None):
        QThread.__init__(self)
        self.number_of_ants = number_of_ants
        self.alpha = alpha
        self.gamma = gamma
        self.delta = delta
        self.beta = beta
        self.graph = graph
        self.num_of_iteration = num_of_iteration
        self.w = w
        self.best_tours = []
        self.best_tour = []
        self.best_tour_len = sys.maxsize
        self.best_ant = -1
        self.ants = []
        self.global_best = global_best
        self.best_lens = []
        self.list_avg = []
        self.list_var = []
        self.list_dev = []
        self.result = result
        self.best_iter = 0

    def computeDelayValue(self):
        p_sum = 0
        for i in range(0, len(self.best_tour)):
            r = self.best_tour[i]
            if i < len(self.best_tour) - 1:
                s = self.best_tour[i+1]
            else:
                s = self.best_tour[0]
            p_sum += self.graph.getDistance(r, s)
        if p_sum != 0:
            return self.w / p_sum
        else:
            return 0

    def updateDelayAntQ(self, tour):
        for i, node in enumerate(tour):
            r = node
            if i < len(tour) - 1:
                s = tour[i + 1]
            else:
                s = tour[0]
            ant_q_val = (1 - self.alpha) * self.graph.getAntQValue(r, s) + self.alpha * self.computeDelayValue()
            self.graph.aq_mat[r][s] = ant_q_val

    def createAnts(self):
        self.ants = []
        nodes = list(range(0, self.graph.num_node))
        starting_nodes = np.random.choice(nodes, self.number_of_ants)
        for i in range(0, self.number_of_ants):
            ant = Ant(i, self, starting_nodes[i])
            self.ants.append(ant)

    def computeIterTotal(self):
        return sum(ant.tour_len for ant in self.ants)

    def computeIterAvg(self):
        return self.computeIterTotal() / self.number_of_ants

    def computeLocalVariance(self, ant):
        return (ant.tour_len - self.computeIterAvg()) ** 2 / (self.number_of_ants - 1)

    def computeIterVariance(self):
        return sum(self.computeLocalVariance(ant) for ant in self.ants)

    def computeIterDeviation(self):
        variance = self.computeIterVariance()
        return np.math.sqrt(variance)

    def runIter(self, iter):
        iter_min = sys.maxsize
        iter_best = []
        self.createAnts()
        for j in range(0, self.graph.num_node):
            for ant in self.ants:
                ant.move()

        for ant in self.ants:
            if ant.tour_len < self.best_tour_len:
                self.best_tour = ant.tour
                self.best_tour_len = ant.tour_len
                print("ant tour: {}".format(ant.tour))
                print("ant len: {}".format(ant.tour_len))
                print("best tour: {}".format(self.best_tour))
                print("best len: {}".format(self.best_tour_len))
                self.best_ant = ant.id
                self.best_iter = iter

            if ant.tour_len < iter_min:
                iter_min = ant.tour_len
                iter_best = ant.tour

        iter_avg = self.computeIterAvg()
        iter_variance = self.computeIterVariance()

        return iter_avg, iter_variance, iter_best

    def run(self):
        for i in range(0, self.num_of_iteration):
            # print("Iteration[%s]" % i)
            iter_avg, iter_variance, iter_best = self.runIter(i)
            iter_deviation = np.math.sqrt(iter_variance)

            if self.global_best:
                update_tour = self.best_tour
            else:
                update_tour = iter_best

            self.updateDelayAntQ(update_tour)


            #self.renderFunc(i, self.best_tour_len, self.best_tour, iter_avg, iter_variance, iter_deviation)
            #self.iteration_finished.emit(i, self.best_tour_len, self.best_tour, iter_avg, iter_variance, iter_deviation)
            aIter_result = {}
            aIter_result["iteration"] = i
            aIter_result["best_tour_len"] = self.best_tour_len
            aIter_result["best_tour"] = self.best_tour
            aIter_result["iter_avg"] = iter_avg
            aIter_result["iter_variance"] = iter_variance
            aIter_result["iter_deviation"] = iter_deviation
            if self.result is None:
                self.result = Queue()
            self.result.put(aIter_result)
            # print("CLGT")
            self.best_tours.append(self.best_tour)
            self.best_lens.append(self.best_tour_len)
            self.list_avg.append(iter_avg)
            self.list_var.append(iter_variance)
            self.list_dev.append(iter_deviation)

class Ant:
    def __init__(self, id, ant_q, start_node, q0=0.9):
        self.id = id
        self.start_node = start_node
        nodes_map = {}
        self.tour = [self.start_node]
        self.curr_node = start_node
        self.q0 = q0
        self.ant_q = ant_q
        self.tour_len = 0.0
        for i in range(0, self.ant_q.graph.num_node):
            if i != self.start_node:
                nodes_map[i] = i
        self.nodes_to_visit = list(nodes_map.values())

    def isEnd(self):
        return not self.nodes_to_visit

        # described in report -- determines next node to visit after curr_node

    def move(self):
        q = random.random()

        if not self.isEnd():
            max_node, max_val = self.ant_q.graph.getMaxAntQ(self.curr_node, self.nodes_to_visit)
            if q <= self.q0:
                # print("Exploitation")
                next_node = max_node
            else:
                # print("Exploration")
                p = self.getNextNodesProbabilities()
                if not p:
                    p = [1.0 / len(self.nodes_to_visit)] * len(self.nodes_to_visit)
                    # print("p[all] = %s" % p[0])

                next_node = np.random.choice(self.nodes_to_visit, 1, replace=False, p=p)[0]

            if next_node == -1:
                raise Exception("next_node < 0")

            self.updateAntQ(self.curr_node, next_node, max_val)
            # print("next node: %s" % (next_node, ))
            self.tour_len += self.ant_q.graph.getDistance(self.curr_node, next_node)
            self.tour.append(next_node)
            self.curr_node = next_node
            self.nodes_to_visit.remove(next_node)

        else:
            curr_node = self.tour[-1]
            next_node = self.tour[0]
            aq_val = self.ant_q.graph.getAntQValue(curr_node, next_node)
            self.updateAntQ(curr_node, next_node, aq_val)
            self.tour_len += self.ant_q.graph.getDistance(curr_node, next_node)

    def updateAntQ(self, curr_node, next_node, max_val):
        r = curr_node
        s = next_node
        alpha = self.ant_q.alpha
        gamma = self.ant_q.gamma
        graph = self.ant_q.graph
        ant_q_val = (1 - alpha) * graph.getAntQValue(r, s) + alpha * gamma * max_val
        graph.aq_mat[r][s] = ant_q_val

    def getNextNodesProbabilities(self):
        r = self.curr_node
        probabilities = []
        heu_sum = self.getHeuristicSum()
        if heu_sum != 0:
            for node in self.nodes_to_visit:
                p = self.getHeuristicValue(r, node) / heu_sum
                # print("p[%s] = %s" % (node, p,))
                probabilities.append(p)
        return probabilities

    def getHeuristicValue(self, r, s):
        return math.pow(self.ant_q.graph.getAntQValue(r, s), self.ant_q.delta) * math.pow(self.ant_q.graph.getHeuristicValue(r, s), self.ant_q.beta)

    def getHeuristicMax(self):
        max_val = -1
        max_node = -1
        r = self.curr_node
        for s in self.nodes_to_visit:
            if self.getHeuristicValue(r, s) > max_val:
                max_val = self.getHeuristicValue(r, s)
                max_node = s
        return max_node, max_val

    def getHeuristicSum(self):
        h_sum = 0
        r = self.curr_node
        for s in self.nodes_to_visit:
            h_sum += self.getHeuristicValue(r, s)
        return h_sum

class AntQGraph:
    def __init__(self, dis_mat, aq_mat=None):
        self.aq_mat = aq_mat
        self.dis_mat = dis_mat
        if aq_mat is None:
            self.aq_mat = [[1.0/999999 for x in range(len(self.dis_mat))] for y in range(len(self.dis_mat))]
            # for i in range(0, len(self.dis_mat)):
            #     for j in range(0, len(self.dis_mat[i])):
            #         if self.dis_mat[i][j] != 0:
            #             self.aq_mat[i][j] = 1 / (self.dis_mat[i][j])
        self.num_node = len(self.aq_mat)

    def getAntQValue(self, r, s):
        return self.aq_mat[r][s]

    def getDistance(self, r, s):
        return self.dis_mat[r][s]

    def getHeuristicValue(self, r, s):
        distance = 1.0 / self.getDistance(r, s)
        return distance

    def getMaxAntQ(self, r, nodes_to_visit):
        max_val = -1
        max_node = -1
        for s in nodes_to_visit:
            ant_q_val = self.getAntQValue(r, s)
            if ant_q_val > max_val:
                max_val = ant_q_val
                max_node = s
        return max_node, max_val


