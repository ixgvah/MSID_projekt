import time
from TSP import *
from ant_colony import *
from simulated_annealing import *
from genetic_algorithm import *


if __name__ == "__main__":
    problem = TSP(n_cities=40, seed=4444)

    print(f"Algorytm Mrówkowy (ACO) dla {problem.n_cities} miast")

    iter_number = 15
    distances = []
    executions = []

    for i in range(iter_number):
        start_time = time.time()
        ant_colony = AntColony(distances=problem.distances, n_ants=20, n_iterations=50, alpha=1.0, beta=3.0, rho=0.4, Q=100, best_ant=2.0)

        best_path, best_distance = ant_colony.run()

        end_time = time.time()
        execution_time = end_time - start_time

        distances.append(best_distance)
        executions.append(execution_time)

        print(f"Test {i + 1}/{iter_number} | Dystans: {best_distance:.2f} | Czas: {execution_time:.2f} s")

    print(f"Symulowane Wyżarzanie (SA) dla {problem.n_cities} miast")
    sa_distances = []
    sa_executions = []

    for i in range(iter_number):
        start_time = time.time()

        sa = SimulatedAnnealing(problem, initial_temp=1000.0, cooling_rate=0.999, min_temp=0.1)
        best_path, best_distance = sa.run()

        end_time = time.time()
        execution_time = end_time - start_time

        sa_distances.append(best_distance)
        sa_executions.append(execution_time)
        print(f"Test {i + 1}/{iter_number} | Dystans: {best_distance:.2f} | Czas: {execution_time:.2f} s")


    print(f"\nAlgorytm Genetyczny (GA) dla {problem.n_cities} miast")
    ga_distances = []
    ga_executions = []
    for i in range(iter_number):
        start_time = time.time()
        ga = GeneticAlgorithm(
            problem=problem,
            population_size=100,   # liczba tras w populacji
            n_generations=300,     # liczba pokoleń
            crossover_rate=0.85,   # szansa na krzyżowanie
            mutation_rate=0.02,    # szansa mutacji na gen
            tournament_size=5,     # rozmiar turnieju selekcji
            elite_count=2          # ile najlepszych kopiujemy bez zmian
        )
        best_path, best_distance = ga.run()
        end_time = time.time()
        execution_time = end_time - start_time
        ga_distances.append(best_distance)
        ga_executions.append(execution_time)
        print(f"Test {i + 1}/{iter_number} | Dystans: {best_distance:.2f} | Czas: {execution_time:.2f} s")

    #Wyniki ACO
    print(f"Algorytm:           Ant Colony Optimization (ACO)")
    print(f"Najlepszy wynik:    {min(distances):.2f}")
    print(f"Średni wynik:       {sum(distances) / iter_number:.2f}")
    print(f"Średni czas:        {sum(executions) / iter_number:.4f} s\n")

    #Wyniki SA
    print(f"Algorytm:           Simulated Annealing (SA)")
    print(f"Najlepszy wynik:    {min(sa_distances):.2f}")
    print(f"Średni wynik:       {sum(sa_distances) / iter_number:.2f}")
    print(f"Średni czas:        {sum(sa_executions) / iter_number:.4f} s")

    #Wyniki GA
    print(f"Algorytm:           Genetic Algorithm (GA)")
    print(f"Najlepszy wynik:    {min(ga_distances):.2f}")
    print(f"Średni wynik:       {sum(ga_distances) / iter_number:.2f}")
    print(f"Średni czas:        {sum(ga_executions) / iter_number:.4f} s")