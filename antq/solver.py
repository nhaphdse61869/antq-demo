import pickle

import sys
import traceback

from antq.antQ import AntQ
from antq.antQGraph import AntQGraph

if __name__ == "__main__":
    tsp = pickle.load(open("ry48p.atsp", "rb"))
    cost_mat = tsp.get_dist_matrix()

    if len(sys.argv) > 1 and sys.argv[1]:
        num_nodes = int(sys.argv[1])
    else:
        num_nodes = len(cost_mat)

    if num_nodes <= 10:
        num_ants = 10
        num_iterations = 50
    else:
        num_ants = num_nodes
        num_iterations = 500

    try:
        if num_nodes < len(cost_mat):
            cost_mat = cost_mat[0:num_nodes]
            for i in range(0, num_nodes):
                cost_mat[i] = cost_mat[i][0:num_nodes]

        graph = AntQGraph(cost_mat)
        antQ = AntQ(num_ants, num_iterations, graph, alpha=.1, gamma=.3, delta=1, beta=2, w =10, global_best=False, result=None)
        antQ.run()
        best_path_vec = antQ.best_tour
        best_path_cost = antQ.best_tour_len

        print("\n------------------------------------------------------------")
        print("                     Results                                ")
        print("------------------------------------------------------------")
        print("\nBest path = %s, %s" % (best_path_vec, antQ.best_iter))
        # for node in best_path_vec:
        #     print(cities[node] + " ", end=' ')
        print("\nBest path cost = %s\n" % best_path_cost)

    except Exception as e:
        print("exception: " + str(e))
        traceback.print_exc()
