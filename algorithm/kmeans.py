import random as rand
import math as math

import numpy as np

class KMean:
    def __init__(self, points, dist_matrix, k):
        self.dist_matrix = dist_matrix
        self.k = k
        self.clusters = [-1 for x in range(len(self.dist_matrix))]  #clusters of nodes
        self.centers = []     #center point index
        self.points = points  #list of point dictionary

    def isCenter(self, index):
        for i in range(len(self.centers)):
            if index == self.centers[i]:
                return True
        return False

    #this method returns the next random node
    def getNextCenterPoint(self):
        #init total dist
        total_dist = []
        for i in range(len(self.dist_matrix)):
            total_dist.append(0)

        #compute total distance from a point to all center
        for i in range(len(self.dist_matrix)):
            if not self.isCenter(i):
                for mean in self.centers:
                    total_dist[i] = total_dist[i] + self.dist_matrix[mean][i]

        #get max point index
        max_dist = 0
        max_index = 0
        for i in range(len(total_dist)):
            if total_dist[i] > max_dist:
                max_index = i
        return max_index

    def initCenters(self):
        #pick the first node at random
        node_index = rand.randint(0,len(self.dist_matrix) - 1)
        self.centers.append(node_index)
        print(node_index)
        print(len(self.dist_matrix))
        print(len(self.clusters))
        self.clusters[node_index] = 0

        #now let's pick k-1 more random points
        for i in range(1, self.k):
            node_index = self.getNextCenterPoint()
            self.centers.append(node_index)
            self.clusters[node_index] = i

    def computeDistance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2,2.0) + math.pow(y1 - y2,2.0))

    def computeCenters(self):
        centers = []
        for cluster_index in range(len(self.centers)):
            center_x = 0
            center_y = 0
            number_point = 0
            for i in range(len(self.dist_matrix)):
                number_point += 1
                #check if it is in cluster
                if self.clusters[i] == cluster_index:
                    center_x += self.points[i][0]
                    center_y += self.points[i][1]
            #compute center x, y
            center_x = center_x/number_point
            center_y = center_y/number_point
            #check which point is nearest new center
            min_dist = -1
            min_center = self.centers[cluster_index]
            for i in range(len(self.dist_matrix)):
                if self.clusters[i] == cluster_index:
                    dist = self.computeDistance(center_x, center_y, self.points[i][0], self.points[i][1])
                    if min_dist < 0 or dist < min_dist:
                        min_dist = dist
                        min_center = i
            centers.append(min_center)
        return centers

    #this method assign nodes to the cluster with the smallest mean
    def assignPoints(self):
        for i in range(len(self.dist_matrix)):
            #check if point is center
            if not self.isCenter(i):
                #compare distance from point to center point
                min_center = 0
                min_dist = self.dist_matrix[self.centers[0]][i]
                for j in range(1, len(self.centers)):
                    if self.dist_matrix[self.centers[j]][i] < min_dist:
                        min_dist = self.dist_matrix[self.centers[j]][i]
                        min_center = j
                #assign cluster to point
                self.clusters[i] = min_center

    def isSameCenters(self, centers):
        #check the current mean with the previous one to see if we should stop
        for i in range(len(centers)):
            have_center = False
            for j in range(len(self.centers)):
                if centers[i] == self.centers[j]:
                    have_center = True
            if not have_center:
                return False
        return True

    #k_means algorithm
    def run(self):
        #compute the initial means
        self.initCenters()
        stop = False
        while not stop:
            self.assignPoints()

            centers = self.computeCenters()

            stop = self.isSameCenters(centers)
            if not stop:
                self.centers = centers
        return 0