import random
import sys
import traceback
import math
from PyQt5.QtCore import QThread, pyqtSignal

class ACOGraph(object):
    def __init__(self, dist_matrix, mat_size):
        """
        :param cost_matrix:
        :param mat_size: size of the cost matrix
        """
        self.matrix = dist_matrix
        self.mat_size = mat_size
        # noinspection PyUnusedLocal
        self.pheromone = [[1 / (mat_size * mat_size) for j in range(mat_size)] for i in range(mat_size)]


class ACO(QThread):
    run_finished = pyqtSignal()
    def __init__(self, ant_count, generations, graph, alpha, beta, rho, q, strategy=2, result_queue=None):
        """
        :param ant_count:
        :param generations:
        :param alpha: relative importance of pheromone
        :param beta: relative importance of heuristic information
        :param rho: pheromone residual coefficient
        :param q: pheromone intensity
        :param strategy: pheromone update strategy. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
        """
        QThread.__init__(self)
        self.clusters_point = [list(range(graph.mat_size))]
        self.graph = graph
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count
        self.generations = generations
        self.update_strategy = strategy

        self.global_best_tour_len = sys.maxsize
        self.global_best_tour = []
        self.result_queue = result_queue
        self.iter_best_tour = []
        self.iter_best_tour_len = sys.maxsize
        self.list_best_tour = []
        self.list_best_len = []
        self.list_avg = []
        self.list_var = []
        self.list_dev = []

    def _updatePheromone(self, graph: ACOGraph, ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]

    # noinspection PyProtectedMember
    def iterRun(self):
        total_cost = 0
        avg_cost = 0
        best_cost = float('inf')
        best_solution = []
        ants = [_Ant(self, self.graph) for i in range(self.ant_count)]
        for ant in ants:
            for i in range(self.graph.mat_size - 1):
                ant._selectNext()
            ant.total_cost += self.graph.matrix[ant.tabu[-1]][ant.tabu[0]]
            total_cost += ant.total_cost
            if ant.total_cost < best_cost:
                best_cost = ant.total_cost
                best_solution = [] + ant.tabu
            # update pheromone
            ant._updatePheromoneDelta()
        avg_cost = total_cost / self.ant_count
        variance = 0
        for ant in ants:
            variance += ((ant.total_cost -avg_cost)**2 / (self.ant_count - 1))
        deviation = math.sqrt(variance)
        self._updatePheromone(self.graph, ants)
        return best_solution, best_cost, avg_cost, variance, deviation

    def run(self):
        for gen in range(self.generations):
            iter_best_tour, iter_best_len, iter_avg, iter_variance, iter_deviation = self.iterRun()


            self.iter_best_tour_len = iter_best_len
            self.iter_best_tour = iter_best_tour

            if self.global_best_tour_len > self.iter_best_tour_len:
                self.global_best_tour_len = self.iter_best_tour_len
                self.global_best_tour = self.iter_best_tour

            aIter_result = {}
            aIter_result["iteration"] = gen
            aIter_result["best_tour_len"] = self.global_best_tour_len
            aIter_result["best_tour"] = self.global_best_tour.copy()
            aIter_result["iter_avg"] = iter_avg
            aIter_result["iter_variance"] = iter_variance
            aIter_result["iter_deviation"] = iter_deviation
            self.result_queue.put(aIter_result)
            self.list_best_tour.append(self.global_best_tour)
            self.list_best_len.append(self.global_best_tour_len)
            self.list_avg.append(iter_avg)
            self.list_var.append(iter_variance)
            self.list_dev.append(iter_deviation)
        self.run_finished.emit()


class _Ant(object):
    def __init__(self, aco: ACO, graph: ACOGraph):
        self.colony = aco
        self.graph = graph
        self.total_cost = 0.0
        self.tabu = []  # tabu list
        self.pheromone_delta = []  # the local increase of pheromone
        self.allowed = [i for i in range(graph.mat_size)]  # nodes which are allowed for the next selection
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.mat_size)] for i in
                    range(graph.mat_size)]  # heuristic information
        start = random.randint(0, graph.mat_size - 1)  # start from any node
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start)

    def _selectNext(self):
        denominator = 0
        for i in self.allowed:
            denominator += self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][
                                                                                            i] ** self.colony.beta
        # noinspection PyUnusedLocal
        probabilities = [0 for i in range(self.graph.mat_size)]  # probabilities for moving to a node in the next step
        for i in range(self.graph.mat_size):
            try:
                self.allowed.index(i)  # test if allowed list contains i
                probabilities[i] = self.graph.pheromone[self.current][i] ** self.colony.alpha * \
                    self.eta[self.current][i] ** self.colony.beta / denominator
            except ValueError:
                pass
            except:
                traceback.print_exc()  # do nothing
        # select next node by probability roulette
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_cost += self.graph.matrix[self.current][selected]
        self.current = selected

    # noinspection PyUnusedLocal
    def _updatePheromoneDelta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.mat_size)] for i in range(self.graph.mat_size)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]
            if self.colony.update_strategy == 1:  # ant-quality system
                self.pheromone_delta[i][j] = self.colony.Q
            elif self.colony.update_strategy == 2:  # ant-density system
                # noinspection PyTypeChecker
                self.pheromone_delta[i][j] = self.colony.Q / self.graph.matrix[i][j]
            else:  # ant-cycle system
                self.pheromone_delta[i][j] = self.colony.Q / self.total_cost
