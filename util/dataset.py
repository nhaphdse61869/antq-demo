import re, math, json
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

        #Read distance data
        for item in data:
            row_distance = item.split()
            if len(row_distance) > 0 and row_distance[0].isdigit():
                distance_data.extend(row_distance)

        #Convert to dist matrix
        for i in range(self.dimension):
            self.dist_matrix.append(distance_data[self.dimension*i:self.dimension*(i+1)])

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

class TSPFileReader:
    def __init__(self, tsp_file_name):
        self.tsp_file_name = tsp_file_name
        self.dimension = 0
        self.cities_set = []
        self.cities_tups = []
        self.cities_dict = {}
        self.dist_matrix = []

        # Read tsp file
        with open(self.tsp_file_name) as f:
            content = f.read().splitlines()
            data = [x.lstrip() for x in content if x != ""]

        # Get number dimension
        non_numeric = re.compile(r'[^\d]+')
        for element in data:
            if element.startswith("DIMENSION"):
                self.dimension = non_numeric.sub("", element)
                self.dimension = int(self.dimension)
            if element.startswith("EDGE_WEIGHT_TYPE"):
                self.type = element.split(":")[1].strip()
            if element.startswith("EDGE_WEIGHT_FORMAT"):
                self.type_format = element.split(":")[1].strip()

        #Convert file follow type
        if self.type == "EUC_2D" or self.type == "ATT" or self.type == "GEO":
            self.readEuc2DType(data)
        elif self.type == "EXPLICIT":
            if self.type_format == "FULL_MATRIX":
                self.readFullMatrixType(data)
            elif self.type_format == "UPPER_ROW":
                self.readUpperRowType(data)

    def readEuc2DType(self, data):
        # Convert to list cities
        for item in data:
            for num in range(1, self.dimension + 1):
                if item.startswith(str(num)):
                    index, space, rest = item.partition(' ')
                    if rest not in self.cities_set:
                        self.cities_set.append(rest)

        # Convert to city tup
        for item in self.cities_set:
            first_coord, space, second_coord = item.partition(' ')
            self.cities_tups.append((float(first_coord.strip()), float(second_coord.strip())))

        # Convert to city dictionary
        for city in range(1, len(self.cities_tups) + 1):
            self.cities_dict[city] = self.cities_tups[city - 1]

        #Compute distance matrix
        self.dist_matrix = [[0 for x in range(self.dimension)] for y in range(self.dimension)]
        for i in range(self.dimension):
            for j in range(self.dimension):
                city1 = self.cities_tups[i]
                city2 = self.cities_tups[j]
                self.dist_matrix[i][j] = self.computeDistance(city1[0], city1[1], city2[0], city2[1])

    def readUpperRowType(self, data):
        self.dist_matrix = [[0 for x in range(self.dimension)] for y in range(self.dimension)]
        distance_temp = []
        end_matrix = False
        # Convert to dist matrix
        for item in data:
            if end_matrix == False:
                row_distance = item.split()
                if len(row_distance) > 0 and row_distance[0].isdigit():
                    distance_temp.append(row_distance)
                elif row_distance[0].strip() == "DISPLAY_DATA_SECTION":
                    end_matrix = True
                    #convert read distance to distance matrix
                    for i in range(self.dimension):
                        for j in range(self.dimension):
                            distance_temp_y = j - i - 1
                            if i == j:
                                self.dist_matrix[i][j] = 0
                            elif j < i:
                                self.dist_matrix[i][j] = float(self.dist_matrix[j][i])
                            else:
                                self.dist_matrix[i][j] = float(distance_temp[i][distance_temp_y])
            else:
                for num in range(1, self.dimension + 1):
                    if item.startswith(str(num)):
                        index, space, rest = item.partition(' ')
                        if rest not in self.cities_set:
                            self.cities_set.append(rest)

        # Convert to city tup
        for item in self.cities_set:
            first_coord, second_coord = item.strip().split()
            self.cities_tups.append((float(first_coord.strip()), float(second_coord.strip())))

        # Convert to city dictionary
        for city in range(1, len(self.cities_tups) + 1):
            self.cities_dict[city] = self.cities_tups[city - 1]

    def readFullMatrixType(self, data):
        number_of_distance = 0
        distance_data = []
        end_matrix = False
        # Convert to dist matrix
        for item in data:
            if end_matrix == False:
                row_distance = item.split()
                if len(row_distance) > 0 and row_distance[0].isdigit():

                    number_of_distance = number_of_distance + len(row_distance)
                    distance_data.extend(row_distance)
                    if number_of_distance >= int(self.dimension):
                        self.dist_matrix.append(distance_data)
                        number_of_distance = 0
                        distance_data = []
                elif row_distance[0].strip() == "DISPLAY_DATA_SECTION":
                    end_matrix = True
            else:
                for num in range(1, self.dimension + 1):
                    if item.startswith(str(num)):
                        index, space, rest = item.partition(' ')
                        if rest not in self.cities_set:
                            self.cities_set.append(rest)

        # Convert to city tup
        for item in self.cities_set:
            first_coord, second_coord = item.strip().split()
            self.cities_tups.append((float(first_coord.strip()), float(second_coord.strip())))

        # Convert to city dictionary
        for city in range(1, len(self.cities_tups) + 1):
            self.cities_dict[city] = self.cities_tups[city - 1]

        #Convert distance matrix string to float
        for i in range(len(self.dist_matrix)):
            for j in range(len(self.dist_matrix)):
                self.dist_matrix[i][j] = float(self.dist_matrix[i][j].strip())

    def computeDistance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2.0) + math.pow(y1 - y2, 2.0))


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
                    self.dist_matrix[i][j] = self.computeDistance(self.cities_tups[i][0], self.cities_tups[i][1],
                                                                  self.cities_tups[j][0], self.cities_tups[j][1])

        f.close()

    def computeDistance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2.0) + math.pow(y1 - y2, 2.0))