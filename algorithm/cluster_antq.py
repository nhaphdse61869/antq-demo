from algorithm.ant_q import AntQ
from algorithm.ant_q import AntQGraph
from algorithm.kmeans import KMean

from PyQt5.QtCore import QThread, pyqtSignal

import math
import sys

class AntQClustering(QThread):
    run_finished = pyqtSignal()

    def __init__(self, list_point, dist_matrix, k, number_of_agent,
                 number_of_iteration, learning_rate=.1, discount_factor=.3,
                 delta=1, beta=2, global_best=False, result_queue=None):
        QThread.__init__(self)
        #Algorithm input
        self.list_point = list_point
        self.dist_matrix = dist_matrix

        #Algorithm parameter
        self.k = k
        self.number_of_agent = number_of_agent
        self.number_of_iteration = number_of_iteration
        self.LR = learning_rate
        self.DF = discount_factor
        self.delta = delta
        self.beta = beta
        self.global_best = global_best

        #Cluster Information
        self.clusters_point = []
        self.clusters_dist_matrix = []
        self.clusters_antq = []

        #Result Output
        self.clusters_best_tour = [[] for x in range(self.k)]
        self.clusters_best_len = [0 for x in range(self.k)]

        #Statistic Output
        self.best_len = 0
        self.list_clusters_best_tour = []
        self.list_clusters_best_len = []
        self.list_avg_best_length = []
        self.list_avg_mean_length = []
        self.list_avg_var = []
        self.list_avg_dev = []

        #Draw chart queue
        self.result_queue = result_queue

        # Divide graph into clusters and init cluster information
        self.initClusters()

    def initClusters(self):
        #Divide graph into k cluster
        kmean = KMean(points=self.list_point, dist_matrix=self.dist_matrix, k=self.k)
        kmean.run()

        #For each cluster
        for i in range(self.k):
            #Get points and distance matrix of cluster
            cluster_point, cluster_dist_matrix = self._getClusterPointsAndDistMatrix(kmean, i)
            self.clusters_point.append(cluster_point)
            self.clusters_dist_matrix.append(cluster_dist_matrix)

            #Create AntQ for cluster
            algGraphEx = AntQGraph(cluster_dist_matrix)
            antq = AntQ(self.number_of_agent, self.number_of_iteration, algGraphEx,
                        self.LR, self.DF, self.delta, self.beta)
            self.clusters_antq.append(antq)

    def _getClusterPointsAndDistMatrix(self, kmean, cluster_index):
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

    def runIterClusterAntq(self, cluster_index, iter_num):
        iter_avg, iter_variance, iter_best_tour = self.clusters_antq[cluster_index].runIter(iter_num)

        if self.global_best:
            iter_best_tour = self.clusters_antq[cluster_index].best_tour

        self.clusters_antq[cluster_index].updateDelayAntQ(iter_best_tour)

        return iter_best_tour,\
               self.clusters_antq[cluster_index].best_tour_len,\
               iter_avg, iter_variance

    def getGraphBestTour(self, cluster_index):
        graph_best_tour = []
        for i in range(len(self.clusters_best_tour[cluster_index])):
            cluster_point_index = self.clusters_best_tour[cluster_index][i]
            graph_best_tour.append(self.clusters_point[cluster_index][cluster_point_index])
        return graph_best_tour

    def runIter(self, iter_num):
        iter_avg_best_length = 0
        iter_avg_variance = 0
        iter_avg_mean_length = 0
        iter_avg_deviation = 0

        for i in range(self.k):
            #Run all cluster antq
            self.clusters_best_tour[i], self.clusters_best_len[i],\
            iter_avg, iter_variance = self.runIterClusterAntq(i, iter_num)

            #Calculate total statistic variable
            iter_avg_best_length += self.clusters_best_len[i]
            iter_avg_variance += iter_variance
            iter_avg_mean_length += iter_avg

        iter_avg_best_length = iter_avg_best_length/self.k
        iter_avg_variance = iter_avg_variance/self.k
        iter_avg_mean_length = iter_avg_mean_length/self.k

        return iter_avg_best_length, iter_avg_variance, iter_avg_mean_length

    def run(self):
        try:
            prev_iter_best_tour = []
            prev_iter_best_len = sys.maxsize
            # Run each iteration
            for i in range(0, self.number_of_iteration):
                print("Iteration {}".format(i))
                iter_best_length, iter_variance, iter_avg = self.runIter(i)

                iter_deviation = math.sqrt(iter_variance)

                # Do not show larger graph
                if prev_iter_best_len > iter_best_length:
                    prev_iter_best_len = iter_best_length
                    prev_iter_best_tour = self.clusters_best_tour
                else:
                    iter_best_length = prev_iter_best_len
                    self.clusters_best_tour = prev_iter_best_tour


                    self.best_len = iter_best_length
                #Add result to queue
                aIter_result = {}
                aIter_result["iteration"] = i
                aIter_result["best_tour_len"] = iter_best_length
                aIter_result["best_tour"] = self.clusters_best_tour.copy()
                aIter_result["iter_avg"] = iter_avg
                aIter_result["iter_variance"] = iter_variance
                aIter_result["iter_deviation"] = iter_deviation
                self.result_queue.put(aIter_result)

                #Save iteration result
                self.list_clusters_best_tour.append(self.clusters_best_tour)
                self.list_clusters_best_len.append(iter_best_length)
                self.list_avg_best_length.append(iter_best_length)
                self.list_avg_mean_length.append(iter_avg)
                self.list_avg_var.append(iter_variance)
                self.list_avg_dev.append(iter_deviation)

            self.run_finished.emit()
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)
