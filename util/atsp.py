import re, math
import networkx as nx
import numpy as np



class ATSPReader:
    def __init__(self, atsp_file_name):
        self.atsp_file_name = atsp_file_name
        self.dimension = 0
        self.dist_matrix = []
        self.cities_set = []
        self.cities_tups = []
        self.cities_dict = {}

        # Read atsp file
        with open(self.atsp_file_name) as f:
            content = f.read().splitlines()
            data = [x.lstrip() for x in content if x != ""]

        # Get number dimension
        non_numeric = re.compile(r'[^\d]+')
        for element in data:
            if element.startswith("DIMENSION"):
                self.dimension = non_numeric.sub("", element)

        self.dimension = int(self.dimension)
        number_of_distance = 0
        distance_data = []
        #Convert to dist matrix
        for item in data:
            row_distance = item.split()
            if len(row_distance) > 0 and row_distance[0].isdigit():
                number_of_distance = number_of_distance + len(row_distance)
                distance_data.extend(row_distance)
                if number_of_distance >= int(self.dimension):
                    self.dist_matrix.append(distance_data)
                    number_of_distance = 0
                    distance_data = []

        #Convert string to float
        for i in range(len(self.dist_matrix)):
            for j in range(len(self.dist_matrix)):
                self.dist_matrix[i][j] = float(self.dist_matrix[i][j].strip())

        #Convert distance matrix to list point
        G = nx.from_numpy_matrix(np.array(self.dist_matrix))
        pos = {0: (0,0)}
        pos = nx.spring_layout(G, pos=pos, fixed=[0])
        for i in range(self.dimension):
            self.cities_tups.append((pos[i][0], pos[i][1]))

if __name__ == "__main__":
    atsp = ATSPReader("ry48p.atsp")
    print(atsp.dist_matrix)
    print(atsp.cities_tups)