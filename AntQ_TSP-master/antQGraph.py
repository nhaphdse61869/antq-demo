import numpy as np


class AntQGraph:
    def __init__(self, dis_mat, aq_mat=None):
        self.aq_mat = aq_mat
        self.dis_mat = dis_mat
        if aq_mat is None:
            self.aq_mat = [[0 for x in range(len(self.dis_mat))] for y in range(len(self.dis_mat))]
            for i in range(0, len(self.dis_mat)):
                for j in range(0, len(self.dis_mat[i])):
                    if self.dis_mat[i][j] != 0:
                        self.aq_mat[i][j] = 1 / (self.dis_mat[i][j])
        self.num_node = len(self.aq_mat)

    def antQ_val(self, r, s):
        return self.aq_mat[r][s]

    def distance(self, r, s):
        return self.dis_mat[r][s]

    def heu_val(self, r, s):
        distance = 1.0 / self.distance(r, s)
        return distance
