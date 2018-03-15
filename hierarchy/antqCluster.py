from antq.antQ import AntQ
from antq.antQGraph import AntQGraph
from cluster.kmeans import KMean
import random as rand


class AntQClustering:
    def __init__(self, points, dist_matrix, k):
        self.points = points
        self.dist_matrix = dist_matrix
        self.k = k
        self.best_tour = []

    def run(self):
        #clustering all point by using k-means algorithms
        kmean = KMean(points=self.points, dist_matrix=self.dist_matrix, k=self.k)
        kmean.run()
        clusters_point = []
        clusters_best_tour = []

        # use antq for each cluster
        for i in range(self.k):
            #convert get all point index in cluster i
            cluster_point = []
            for j in range(len(self.dist_matrix)):
                if kmean.clusters[j] == i:
                    cluster_point.append(j)

            # convert distance matrix to cluster distance matrix
            cluster_dist_matrix = [[0 for x in range(len(self.cluster_point))] for y in range(len(self.cluster_point))]
            for z in range(len(cluster_point)):
                for w in range(len(cluster_point)):
                    cluster_dist_matrix[z][w] = self.dist_matrix[cluster_point[z]][cluster_point[w]]

            #use antq algorithm

            #save best tour and cluster points
            best_tour = []
            clusters_best_tour.append(best_tour)
            clusters_point.append(cluster_point)

        #merge all cluster
        #use ant q to find best tour for all center points
        center_best_tour = []

        #random start cluster
        start_cluster = rand.randint(0, len(kmean.centers))


        #find next cluster
        next_cluster = 0
        new_best_center_tour = []

        for i in range(len(center_best_tour)):
            if center_best_tour[i] == start_cluster:
                if i < (len(center_best_tour) -1):
                    next_cluster = center_best_tour[i + 1]
                else:
                    next_cluster = center_best_tour[0]
                new_best_center_tour.extend(center_best_tour[:i])
                new_best_center_tour.extend(center_best_tour[(i + 2):])


        #find minimum edge between 2 cluster
        min_dist = self.dist_matrix[kmean.centers[start_cluster]][kmean.centers[next_cluster]]
        q = 0
        r = 0
        for i in range(len(clusters_point[start_cluster])):
            for j in range(len(clusters_point[next_cluster])):
                distance = self.dist_matrix[clusters_point[start_cluster][i]][clusters_point[next_cluster][j]]
                if distance < min_dist:
                    q = i
                    r = j
                    min_dist = distance

        #select start point in start cluster
        new_best_cluster_tour = []
        start_cluster_point_index = 0
        for i in range(len(clusters_best_tour[start_cluster])):
            if clusters_best_tour[start_cluster][i] == q:
                if i == len(clusters_best_tour[start_cluster]) - 1:
                    start_cluster_point_index = 0
                else:
                    start_cluster_point_index = i + 1

        #reorder base on start point
        new_best_cluster_tour.extend(clusters_best_tour[start_cluster][start_cluster_point_index:])
        new_best_cluster_tour.extend(clusters_best_tour[start_cluster][:start_cluster_point_index])

        #add start cluster point to best tour
        self.best_tour.append(clusters_point[start_cluster][start_cluster_point_index])

        #add start cluster tour to best tour
        for i in range(len(new_best_cluster_tour)):
            self.best_tour.append(clusters_point[start_cluster][new_best_cluster_tour[i]])

        #add start point of next cluster
        self.best_tour.append(clusters_point[next_cluster][r])

        #add next cluster tour to best tour
        new_best_cluster_tour = []
        for i in range(len(clusters_best_tour[next_cluster])):
            if (clusters_best_tour[next_cluster][i]) == r:
                if i == 0:
                    new_best_cluster_tour.extend(clusters_best_tour[next_cluster])
                else:
                    new_best_cluster_tour.extend(clusters_best_tour[next_cluster][i:])
                    new_best_cluster_tour.extend(clusters_best_tour[next_cluster][:i])

        for i in range(len(new_best_cluster_tour)):
            self.best_tour.append(clusters_point[next_cluster][new_best_cluster_tour[i]])

        #add other cluster tour

        #new cluster best tour
        prev_cluster = next_cluster
        prev_cluster_last_point = clusters_best_tour[next_cluster][-1]
        for i in range(len(new_best_center_tour)):
            next_cluster = new_best_center_tour[i]
            next_cluster_first_point = clusters_best_tour[next_cluster][0]
            min_dist = self.dist_matrix[clusters_point[prev_cluster][prev_cluster_last_point]][clusters_point[next_cluster][next_cluster_first_point]]
            first_point = 0
            #find min edge from prev cluster to next cluster
            for j in range(1, len(clusters_best_tour[next_cluster])):
                next_cluster_temp_point = clusters_best_tour[next_cluster][j]
                dist = self.dist_matrix[clusters_point[prev_cluster][prev_cluster_last_point]][
                    clusters_point[next_cluster][next_cluster_temp_point]]
                if dist < min_dist:
                    first_point = j
                    min_dist = dist

            #create new best tour of next cluster
            new_best_cluster_tour = []
            new_best_cluster_tour.extend(clusters_best_tour[next_cluster][first_point:])
            new_best_cluster_tour.extend(clusters_best_tour[next_cluster][:first_point])
            clusters_best_tour[next_cluster] = new_best_cluster_tour

            #assign tour to best tour
            for i in range(len(new_best_cluster_tour)):
                self.best_tour.append(clusters_point[next_cluster][new_best_cluster_tour[i]])

            prev_cluster = next_cluster
            prev_cluster_last_point = clusters_best_tour[next_cluster][-1]






