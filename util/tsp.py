import re, math


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
            self.euc_2d_type_reader(data)
        elif self.type == "EXPLICIT":
            if self.type_format == "FULL_MATRIX":
                self.full_matrix_type_reader(data)
            elif self.type_format == "UPPER_ROW":
                self.upper_row_type_reader(data)

    def euc_2d_type_reader(self, data):
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
                self.dist_matrix[i][j] = self.compute_distance(city1[0], city1[1], city2[0], city2[1])

    def upper_row_type_reader(self, data):
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
                            distance_temp_y = self.dimension - 1 - j
                            print(distance_temp_y)
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

    def full_matrix_type_reader(self, data):
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

    def get_dist_matrix(self):
        return self.dist_matrix

    def compute_distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2.0) + math.pow(y1 - y2, 2.0))


if __name__ == "__main__":
    reader = TSPFileReader("bayg29.tsp")
    print(reader.cities_tups)
    print(reader.dist_matrix)
    pass