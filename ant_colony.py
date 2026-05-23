import numpy
import random

class AntColony:
    def __init__(self, distances, n_ants=20, n_iterations=100, alpha=1.0, beta=3.0, rho=0.4, Q=100, best_ant=2.0):
        self.distances = numpy.array(distances)
        self.n_cities = len(distances)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha          #sugerowanie się zapachem feromonu
        self.beta = beta            #sugerowanie się krótszą odległością miasta
        self.rho = rho              #współczynnik parowania feromonu
        self.Q = Q                  #pula feromonu do rozłożenia
        self.best_ant = best_ant    #premia dla najlepszej mrowki
        self.best_path = None
        self.best_length = float('inf') #nieskonczonosc

        self.pheromons_map = numpy.ones((self.n_cities, self.n_cities)) - numpy.eye(self.n_cities)
        #macierz feromonow z zerami na przekatnej zeby mrowka nie szla z miasta a do miasta a


    def _choose_next_city(self, current_city, visited):
        unvisited = [c for c in range(self.n_cities) if c not in visited]

        if not unvisited:
            return None

        weights = []
        for c in unvisited:
            tau = pow(self.pheromons_map[current_city][c], self.alpha) #patrzymy na mape feromonu
            eta = pow(1/self.distances[current_city][c], self.beta)     #patrzymy na odleglosci
            weights.append(tau * eta)
        #powinno sięto podzielic przez sumę wszystkich wag, ale jest to niepotrzebne z uwagi na to, że mianownik zawsze bedzie taki sam

        return random.choices(unvisited, weights=weights)[0]

    def calculate_distance(self, path):
        distance = 0
        for i in range(len(path)-1):
            distance += self.distances[path[i]][path[i+1]]
        distance += self.distances[path[-1]][path[0]]
        return distance

    def _build_path(self):
        start_city = random.randint(0, self.n_cities - 1)
        path = [start_city]
        visited = {start_city} #wartości unikalne

        while len(path) < self.n_cities:
            next_city = self._choose_next_city(path[-1], visited) #wybor nastepnego miasta
            path.append(next_city)
            visited.add(next_city)
        return path

    def run(self):
        for i in range(self.n_iterations):
            all_paths_and_distances = []

            for a in range(self.n_ants):
                path = self._build_path()
                distance = self.calculate_distance(path)
                all_paths_and_distances.append((path, distance))

                if distance < self.best_length: #czy mrowka ma krotszy rekord
                    self.best_path = path[:] #czym sie rozni
                    self.best_length = distance
            #po kazdym przejsciu mrowek paruje feromon
            self.pheromons_map *= 1 - self.rho

            #dodanie feromonu przez trase mrowki
            for(path, length) in all_paths_and_distances:
                deposit = self.Q/length

                for i in range(len(path) - 1):
                    x, y = path[i], path[i+1]
                    self.pheromons_map[x][y] += deposit
                    self.pheromons_map[y][x] += deposit

                start_city, end_city = path[0], path[-1]
                self.pheromons_map[start_city][end_city] += deposit
                self.pheromons_map[end_city][start_city] += deposit

            #dodanie feromonu dla trasy najlepszej mrowki z iteracji
            if self.best_ant > 0:
                extra_deposit = (self.Q/self.best_length) * self.best_ant

                for i in range(len(self.best_path) - 1):
                    a, b = self.best_path[i], self.best_path[i + 1]
                    self.pheromons_map[a][b] += extra_deposit
                    self.pheromons_map[b][a] += extra_deposit

                start, end = self.best_path[-1], self.best_path[0]
                self.pheromons_map[start][end] += extra_deposit
                self.pheromons_map[end][start] += extra_deposit

        return self.best_path, self.best_length