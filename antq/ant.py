import random
import math
import numpy as np


class Ant:
    def __init__(self, id, ant_q, start_node, q0=0.7):
        self.id = id
        self.start_node = start_node
        nodes_map = {}
        self.tour = []
        self.curr_node = start_node
        self.q0 = q0
        self.ant_q = ant_q
        self.tour_len = 0.0
        for i in range(0, self.ant_q.graph.num_node):
            if i != self.start_node:
                nodes_map[i] = i
        self.nodes_to_visit = list(nodes_map.values())

    def end(self):
        return not self.nodes_to_visit

        # described in report -- determines next node to visit after curr_node

    def move(self):
        q = random.random()

        if not self.end():
            max_node, max_val = self.max_aq()
            if q <= self.q0:
                print("Exploitation")
                next_node = max_node
            else:
                print("Exploration")
                p = self.next_nodes_probabilities()
                if not p:
                    p = [1.0 / len(self.nodes_to_visit)] * len(self.nodes_to_visit)
                    print("p[all] = %s" % p[0])

                next_node = np.random.choice(self.nodes_to_visit, 1, replace=False, p=p)[0]

            if next_node == -1:
                raise Exception("next_node < 0")

            self.update_ant_q(next_node, max_val)
            print("next node: %s" % (next_node, ))
            self.tour_len += self.ant_q.graph.distance(self.curr_node, next_node)
            self.tour.append(next_node)
            self.curr_node = next_node
            self.nodes_to_visit.remove(next_node)

        else:
            self.tour_len += self.ant_q.graph.distance(self.tour[-1], self.tour[0])

    def update_ant_q(self, next_node, max_val):
        r = self.curr_node
        s = next_node
        alpha = self.ant_q.alpha
        gamma = self.ant_q.gamma
        graph = self.ant_q.graph
        ant_q_val = (1 - alpha) * graph.antQ_val(r, s) + alpha * gamma * max_val
        graph.aq_mat[r][s] = ant_q_val

    def next_nodes_probabilities(self):
        r = self.curr_node
        probabilities = []
        heu_sum = self.heuristic_sum()
        if heu_sum != 0:
            for node in self.nodes_to_visit:
                p = self.heuristic_val(r, node) / heu_sum
                print("p[%s] = %s" % (node, p,))
                probabilities.append(p)
        return probabilities

    def max_aq(self):
        max_val = -1
        max_node = -1
        r = self.curr_node
        for s in self.nodes_to_visit:
            ant_q_val = self.ant_q.graph.antQ_val(r, s)
            if ant_q_val > max_val:
                max_val = ant_q_val
                max_node = s
        return max_node, max_val

    def heuristic_val(self, r, s):
        return math.pow(self.ant_q.graph.antQ_val(r, s), self.ant_q.delta) * math.pow(self.ant_q.graph.heu_val(r, s), self.ant_q.beta)

    def heuristic_max(self):
        max_val = -1
        max_node = -1
        r = self.curr_node
        for s in self.nodes_to_visit:
            if self.heuristic_val(r, s) > max_val:
                max_val = self.heuristic_val(r, s)
                max_node = s
        return max_node, max_val

    def heuristic_sum(self):
        h_sum = 0
        r = self.curr_node
        for s in self.nodes_to_visit:
            h_sum += self.heuristic_val(r, s)
        return h_sum
