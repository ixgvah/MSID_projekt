import numpy

class TSP:
    def __init__(self, n_cities, seed = 20):
        numpy.random.seed(seed)
        self.coords = numpy.random.rand(n_cities, 2) * 100 #wspolrzedne
        self.n_cities = n_cities
        self.distances = numpy.zeros((n_cities, n_cities))
        #inicjalizacja macierzy odległości
        for i in range(n_cities):
            for j in range(n_cities):
                if i != j:
                    self.distances[i][j] = numpy.linalg.norm(self.coords[i] - self.coords[j])

    #funkcja celu: obliczenie dlugosci calej trasy
    def evaluate(self, path):
        total_distance = 0
        for i in range(len(path) - 1):
            current_city = path[i]
            next_city = path[i + 1]
            total_distance += self.distances[current_city][next_city]

        last_city = path[-1]
        first_city = path[0]
        total_distance += self.distances[last_city][first_city]
        return total_distance
