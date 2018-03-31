import numpy as np


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

    def antQ_val(self, r, s):
        return self.aq_mat[r][s]

    def distance(self, r, s):
        return self.dis_mat[r][s]

    def heu_val(self, r, s):
        distance = 1.0 / self.distance(r, s)
        return distance

    def max_aq(self, r, nodes_to_visit):
        max_val = -1
        max_node = -1
        for s in nodes_to_visit:
            ant_q_val = self.antQ_val(r, s)
            if ant_q_val > max_val:
                max_val = ant_q_val
                max_node = s
        return max_node, max_val
