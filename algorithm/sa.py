import math
import random
from util.dataset import TSPFileReader
from PyQt5.QtCore import QThread, pyqtSignal

class SimAnneal(QThread):
    run_finished = pyqtSignal()
    def __init__(self, dist_matrix, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1, result_queue=None):
        QThread.__init__(self)

        self.N = len(dist_matrix)
        self.T = math.sqrt(self.N) if T == -1 else T
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 0.00000001 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1

        self.dist_matrix = dist_matrix
        self.result_queue = result_queue
        self.nodes = range(self.N)

        self.clusters_point = [list(range(len(dist_matrix)))]
        self.best_tours = []
        self.best_lens = []
        self.list_avg = []
        self.list_var = []
        self.list_dev = []
        self.list_iter = []

        self.cur_solution = self.initSolution()
        self.best_tour = list(self.cur_solution)

        self.cur_fitness = self.fitness(self.cur_solution)
        self.initial_fitness = self.cur_fitness
        self.best_tour_len = self.cur_fitness

        self.fitness_list = [self.cur_fitness]


    def initSolution(self):
        """
        Greedy algorithm to get an initial solution (closest-neighbour)
        """
        cur_node = random.choice(self.nodes)
        solution = [cur_node]

        free_list = list(self.nodes)
        free_list.remove(cur_node)

        while free_list:
            #Find minimum distance
            min_distance = self.dist_matrix[cur_node][free_list[0]]
            min_node = free_list[0]
            for j in free_list:
                temp_distance = self.dist_matrix[cur_node][j]
                if temp_distance < min_distance:
                    min_node = j
            cur_node = min_node
            free_list.remove(cur_node)
            solution.append(cur_node)
        return solution

    def fitness(self, sol):
        """ Objective value of a solution """
        return sum([self.dist_matrix[sol[i - 1]][sol[i]] for i in range(1, self.N)]) \
               + self.dist_matrix[sol[0]][sol[self.N - 1]]

    def computeAcceptP(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current
        Depends on the current temperature and difference between candidate and current
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current
        Accept with probabilty p_accept(..) if candidate is worse
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_tour_len:
                self.best_tour_len = candidate_fitness
                self.best_tour = candidate
        else:
            if random.random() < self.computeAcceptP(candidate_fitness):
                self.cur_fitness = candidate_fitness
                self.cur_solution = candidate

    def run(self):
        """
        Execute simulated annealing algorithm
        """
        print("Start nào")
        while self.T >= self.stopping_temperature and self.iteration <= self.stopping_iter:
            print("Iteration thứ {}".format(self.iteration))
            candidate = list(self.cur_solution)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
            self.accept(candidate)
            self.list_iter.append(self.iteration - 1)
            self.best_tours.append(self.cur_solution)
            self.best_lens.append(self.cur_fitness)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)

            #Add result to queue
            aIter_result = {}
            aIter_result["iteration"] = self.iteration - 1
            aIter_result["best_tour_len"] = self.cur_fitness
            aIter_result["best_tour"] = self.cur_solution
            self.result_queue.put(aIter_result)
        self.run_finished.emit()

        #print('Best fitness obtained: ', self.best_fitness)
        #print('Improvement over greedy heuristic: ',
              #round((self.initial_fitness - self.best_fitness) / (self.initial_fitness), 4))