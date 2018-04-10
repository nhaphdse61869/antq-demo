import json
import math

class GMapDataReader:

    def __init__(self, file_name):
        self.file_name = file_name
        self.dimension = 0
        self.cities_set = []
        self.cities_tups = []
        self.cities_dict = {}
        self.dist_matrix = []
        self.list_address = []

        f = open(file_name, encoding="utf-8-sig")
        data = json.load(f)
        #Load list point and list address
        self.dimension = len(data["list_point"])
        for i in range(len(data["list_point"])):
            lat = data["list_point"][i]["latitude"]
            long = data["list_point"][i]["longitude"]
            address = data["list_point"][i]["address"]

            self.cities_tups.append((lat,long))
            self.list_address.append(address)

        #Load distance matrix
        self.dist_matrix = data["dist_matrix"]
        if len(self.dist_matrix) == 0:
            self.dist_matrix = [[0 for y in range(self.dimension)] for x in range(self.dimension)]
            for i in range(self.dimension):
                for j in range(self.dimension):
                    self.dist_matrix[i][j] = self.compute_distance(self.cities_tups[i][0],self.cities_tups[i][1],
                                                                   self.cities_tups[j][0],self.cities_tups[j][1])

        f.close()

    def compute_distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2.0) + math.pow(y1 - y2, 2.0))