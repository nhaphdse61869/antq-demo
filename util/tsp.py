import re, math


class TSPFileReader:
    def __init__(self, tsp_file_name):
        self.tsp_file_name = tsp_file_name
        self.dimension = 0
        self.cities_set = []
        self.cities_tups = []
        self.cities_dict = {}

        # Read tsp file
        with open(self.tsp_file_name) as f:
            content = f.read().splitlines()
            data = [x.lstrip() for x in content if x != ""]

        # Get number dimension
        non_numeric = re.compile(r'[^\d]+')
        for element in data:
            if element.startswith("DIMENSION"):
                self.dimension = non_numeric.sub("", element)

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
            self.cities_tups.append((first_coord.strip(), second_coord.strip()))

        # Convert to city dictionary
        for city in range(1, len(self.cities_tups) + 1):
            self.cities_dict[city] = self.cities_tups[city - 1]

    def get_dist_matrix(self):
        dist_matrix = [[0 for x in range(self.dimension)] for y in range(self.dimension)]
        for i in range(self.dimension):
            for j in range(self.dimension):
                city1 = self.cities_tups[i]
                city2 = self.cities_tups[j]
                dist_matrix[i, j] = self.compute_distance(city1[0], city1[1], city2[0], city2[1])
        return dist_matrix

    def compute_distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2.0) + math.pow(y1 - y2, 2.0))
