import pickle

import sys
import traceback

from antQ import AntQ
from antQGraph import AntQGraph

if __name__ == "__main__":
    stuff = pickle.load(open("citiesAndDistances.pickled", "rb"))
    cities = stuff[0]
    cost_mat = stuff[1]

    if len(sys.argv) > 1 and sys.argv[1]:
        num_nodes = int(sys.argv[1])
    else:
        num_nodes = len(cities)

    if num_nodes <= 10:
        num_ants = 10
        num_iterations = 50
    else:
        num_ants = num_nodes
        num_iterations = 200

    try:
        if num_nodes < len(cost_mat):
            cost_mat = cost_mat[0:num_nodes]
            for i in range(0, num_nodes):
                cost_mat[i] = cost_mat[i][0:num_nodes]

        graph = AntQGraph(cost_mat)
        antQ = AntQ(num_ants, num_iterations, graph)
        antQ.run()
        best_path_vec = antQ.best_tour
        best_path_cost = antQ.best_tour_len

        print("\n------------------------------------------------------------")
        print("                     Results                                ")
        print("------------------------------------------------------------")
        print("\nBest path = %s" % best_path_vec)
        for node in best_path_vec:
            print(cities[node] + " ", end=' ')
        print("\nBest path cost = %s\n" % best_path_cost)

    except Exception as e:
        print("exception: " + str(e))
        traceback.print_exc()
