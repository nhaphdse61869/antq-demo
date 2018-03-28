from antq.antQ import AntQ
from antq.antQGraph import AntQGraph
from PyQt5.QtCore import QThread, pyqtSignal
from cluster.kmeans import KMean
import random as rand
import sys

class AntQClustering(QThread):
    run_finished = pyqtSignal()

    def __init__(self, points, dist_matrix, k, number_of_agent,
                 number_of_iteration, learning_rate=.1, discount_factor=.3,
                 delta=1, beta=2, merge_cluster = True, result_queue=None):
        QThread.__init__(self)
        self.points = points
        self.dist_matrix = dist_matrix
        self.k = k
        self.number_of_agent = number_of_agent
        self.number_of_iteration = number_of_iteration
        self.LR = learning_rate
        self.DF = discount_factor
        self.delta = delta
        self.beta = beta
        self.merge_cluster = merge_cluster
        self.best_tour = []
        self.best_tour_len = sys.maxsize
        self.list_best_tour = []
        self.list_best_len = []
        self.list_avg = []
        self.list_var = []
        self.list_dev = []
        self.clusters_point = []
        self.clusters_best_tour = [[] for x in range(self.k)]
        print(self.clusters_best_tour)
        self.clusters_dist_matrix = []
        self.clusters_antq = []
        self.center_points = []
        self.center_best_tour = []
        self.center_dist_matrix = []
        self.center_antq = None
        self.result_queue = result_queue

    def initial_algorithm(self):
        #Divide graph into k cluster
        kmean = KMean(points=self.points, dist_matrix=self.dist_matrix, k=self.k)
        kmean.run()

        #For each cluster
        for i in range(self.k):
            #Get points and distance matrix of cluster
            cluster_point, cluster_dist_matrix = self.get_cluster_points_and_dist_matrix(kmean, i)
            self.clusters_point.append(cluster_point)
            self.clusters_dist_matrix.append(cluster_dist_matrix)

            #Create AntQ for cluster
            algGraphEx = AntQGraph(cluster_dist_matrix)
            antq = AntQ(self.number_of_agent, self.number_of_iteration, algGraphEx,
                        self.LR, self.DF, self.delta, self.beta)
            self.clusters_antq.append(antq)

        #For center
        #Get point and distance matrix of center
        self.center_points, self.center_dist_matrix = self.get_centers_points_and_dist_matrix(kmean)
        #Create AntQ for centers
        algGraphEx = AntQGraph(self.center_dist_matrix)
        self.center_antq = AntQ(self.number_of_agent, self.number_of_iteration, algGraphEx,
                                self.LR, self.DF, self.delta, self.beta)

    def get_cluster_points_and_dist_matrix(self, kmean, cluster_index):
        cluster_point = []
        # Get all point in cluster_index
        for i in range(len(self.dist_matrix)):
            if kmean.clusters[i] == cluster_index:
                cluster_point.append(i)

        cluster_dist_matrix = [[0 for x in range(len(cluster_point))] for y in range(len(cluster_point))]
        # Get distance matrix of cluster_index
        for i in range(len(cluster_point)):
            for j in range(len(cluster_point)):
                cluster_dist_matrix[i][j] = self.dist_matrix[cluster_point[i]][cluster_point[j]]

        return cluster_point, cluster_dist_matrix

    def get_centers_points_and_dist_matrix(self, kmean):
        center_point = kmean.centers
        center_dist_matrix = [[0 for x in range(len(center_point))] for y in range(len(center_point))]

        for i in range(len(center_point)):
            for j in range(len(center_point)):
                center_dist_matrix[i][j] = self.dist_matrix[center_point[i]][center_point[j]]
        return center_point, center_dist_matrix

    def cluster_antq_iter_run(self, cluster_index):
        iter_avg, iter_variance, iter_deviation = self.clusters_antq[cluster_index].iter_run()
        self.clusters_antq[cluster_index].delay_ant_q()
        return self.clusters_antq[cluster_index].best_tour, iter_avg, iter_variance, iter_deviation

    def center_antq_iter_run(self):
        iter_avg, iter_variance, iter_deviation = self.center_antq.iter_run()
        self.center_antq.delay_ant_q()
        return self.center_antq.best_tour, iter_avg, iter_variance, iter_deviation

    def get_min_dist_two_cluster_point(self, current_cluster_index, next_cluster_index, current_cluster_point_index=None):

        current_cluster_points = self.clusters_point[current_cluster_index]
        next_cluster_points = self.clusters_point[next_cluster_index]
        next_cluster_point_index = 0

        if current_cluster_point_index == None:
            current_cluster_point_index = 0
            min_dist = self.dist_matrix[current_cluster_points[current_cluster_point_index]][
                next_cluster_points[next_cluster_point_index]]
            for i in range(len(current_cluster_points)):
                for j in range(len(next_cluster_points)):
                    temp_dist = self.dist_matrix[current_cluster_points[i]][next_cluster_points[j]]
                    if temp_dist < min_dist:
                        current_cluster_point_index = i
                        next_cluster_point_index = j
                        min_dist = temp_dist
        else:
            min_dist = self.dist_matrix[current_cluster_points[current_cluster_point_index]][
                next_cluster_points[next_cluster_point_index]]
            for j in range(len(next_cluster_points)):
                temp_dist = self.dist_matrix[current_cluster_points[current_cluster_point_index]][next_cluster_points[j]]
                if temp_dist < min_dist:
                    next_cluster_point_index = j
                    min_dist = temp_dist
        return current_cluster_point_index, next_cluster_point_index

    def reorder_list(self, origin_list, start_index):
        new_list = []
        new_list.extend(origin_list[start_index:])
        if start_index > 0:
            new_list.extend(origin_list[:start_index])
        return new_list

    def cluster_best_tour_to_graph_best_tour(self, cluster_index):
        graph_best_tour = []
        for i in range(len(self.clusters_best_tour[cluster_index])):
            cluster_point_index = self.clusters_best_tour[cluster_index][i]
            graph_best_tour.append(self.clusters_point[cluster_index][cluster_point_index])
        return graph_best_tour

    def iteration_run(self):
        #Get best tour of each cluster
        iteration_variance = 0
        iteration_avg = 0
        iteration_deviation = 0
        for i in range(self.k):
            self.clusters_best_tour[i], iter_avg, iter_variance, iter_deviation = self.cluster_antq_iter_run(i)
            iteration_variance += iter_variance
            iteration_avg += iter_avg
            iteration_deviation += iter_deviation

        iteration_variance = iteration_variance/self.k
        iteration_deviation = iter_deviation/self.k

        if self.merge_cluster:
            #Get best tour of center
            self.center_best_tour, iter_avg, iter_variance, iter_deviation = self.center_antq_iter_run()

            iteration_avg += iter_avg

            #Random to get which cluster is start cluster
            center_best_tour_start_point_index = rand.randint(0, len(self.center_best_tour))

            #Reorder center best to with previous start point
            self.center_best_tour = self.reorder_list(self.center_best_tour, center_best_tour_start_point_index)

            #Add từng best tour vào self.best_tour
            current_cluster_index = self.center_best_tour[0]
            for i in range(1, len(self.center_best_tour)):
                next_cluster_index = self.center_best_tour[i]
                if i==1:
                    #Find min edge between 2 cluster
                    current_cluster_end_point_index, next_cluster_start_point_index = self.get_min_dist_two_cluster_point(current_cluster_index, next_cluster_index)

                    #Get start point index of best tour of current cluster
                    current_cluster_best_tour_start_point_index = 0
                    for j in range(len(self.clusters_best_tour[current_cluster_index])):
                        if self.clusters_best_tour[current_cluster_index][j] == current_cluster_end_point_index:
                            if j == (len(self.clusters_best_tour[current_cluster_index]) - 1):
                                current_cluster_best_tour_start_point_index = 0
                            else:
                                current_cluster_best_tour_start_point_index = j + 1

                    #Reorder best tour of current cluster
                    self.clusters_best_tour[current_cluster_index] = self.reorder_list(
                        self.clusters_best_tour[current_cluster_index], current_cluster_best_tour_start_point_index)

                    #Add best tour of current cluster to graph best tour
                    current_cluster_graph_best_tour = self.cluster_best_tour_to_graph_best_tour(current_cluster_index)
                    self.best_tour.extend(current_cluster_graph_best_tour)
                else:
                    #Find min edge between 2 clusters with current cluster end point index
                    current_cluster_end_point_index, next_cluster_start_point_index = self.get_min_dist_two_cluster_point(
                        current_cluster_index, next_cluster_index, current_cluster_end_point_index)

                #Get start point index of best tour of next cluster
                next_cluster_best_tour_start_point_index = 0
                for j in range(len(self.clusters_best_tour[next_cluster_index])):
                    if self.clusters_best_tour[next_cluster_index][j] == next_cluster_start_point_index:
                        next_cluster_best_tour_start_point_index = j

                #Reorder best tour of next cluster
                self.clusters_best_tour[next_cluster_index] = self.reorder_list(
                    self.clusters_best_tour[next_cluster_index], next_cluster_best_tour_start_point_index)

                #Add best tour of next cluster to graph best tour
                next_cluster_graph_best_tour = self.cluster_best_tour_to_graph_best_tour(next_cluster_index)
                self.best_tour.extend(next_cluster_graph_best_tour)

                #Reassign current cluster
                current_cluster_index = next_cluster_index
                current_cluster_end_point_index = self.clusters_best_tour[next_cluster_index][-1]
        return iteration_variance, iteration_avg, iteration_deviation


    def run(self):
        #Divide graph into cluster and initial algorithm
        try:
            self.initial_algorithm()
            prev_iter_best_tour = []
            prev_iter_best_len = sys.maxsize
            # Run each iteration
            for i in range(0, self.number_of_iteration):
                print("Iteration {}".format(i))
                iteration_variance, iteration_avg, iteration_deviation = self.iteration_run()
                self.best_tour_len = 0

                # Calculate best length
                for j in range(len(self.best_tour) - 1):
                    self.best_tour_len += self.dist_matrix[self.best_tour[j]][self.best_tour[j + 1]]

                self.best_tour_len += self.dist_matrix[self.best_tour[-1]][self.best_tour[0]]

                # Do not show larger graph
                if prev_iter_best_len > self.best_tour_len:
                    prev_iter_best_len = self.best_tour_len
                    prev_iter_best_tour = self.best_tour
                else:
                    self.best_tour_len = prev_iter_best_len
                    self.best_tour = prev_iter_best_tour

                # Add result to queue

                aIter_result = {}
                aIter_result["iteration"] = i
                aIter_result["best_tour_len"] = self.best_tour_len
                aIter_result["best_tour"] = self.best_tour
                aIter_result["iter_avg"] = iteration_avg
                aIter_result["iter_variance"] = iteration_variance
                aIter_result["iter_deviation"] = iteration_deviation
                self.result_queue.put(aIter_result)
                self.list_best_tour.append(self.best_tour)
                self.list_best_len.append(self.best_tour_len)
                self.list_avg.append(iteration_avg)
                self.list_var.append(iteration_variance)
                self.list_dev.append(iteration_deviation)

            self.run_finished.emit()
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)
