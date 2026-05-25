import random
import math


class SimulatedAnnealing:
    def __init__(self, problem, initial_temp=1000.0, cooling_rate=0.99, min_temp=0.1):
        self.problem = problem#Obiekt klasy TSP
        self.T = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp

    def generate_initial_solution(self):
        route = list(range(self.problem.n_cities))
        random.shuffle(route)
        return route

    def generate_neighbor(self, route):
        neighbor = route[:]
        idx1, idx2 = random.sample(range(len(route)), 2)
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
        return neighbor

    def run(self):
        current_solution = self.generate_initial_solution()
        current_cost = self.problem.evaluate(current_solution)

        best_solution = current_solution[:]
        best_cost = current_cost

        #GŁÓWNA PĘTLA ALGORYTMU
        while self.T > self.min_temp:
            new_solution = self.generate_neighbor(current_solution)
            new_cost = self.problem.evaluate(new_solution)

            delta = new_cost - current_cost

            #Kryterium akceptacji
            if delta < 0:
                current_solution = new_solution
                current_cost = new_cost
            else:
                probability = math.exp(-delta / self.T)
                if random.random() < probability:
                    current_solution = new_solution
                    current_cost = new_cost

            #Zapis najlepszego wyniku
            if current_cost < best_cost:
                best_solution = current_solution[:]
                best_cost = current_cost

            self.T *= self.cooling_rate

        return best_solution, best_cost