import time
from MSID_projekt.TSP import *
from MSID_projekt.ant_colony import *

if __name__ == "__main__":
    problem = TSP(n_cities=40, seed=4444)

    print(f"Algorytm Mrówkowy (ACO) dla {problem.n_cities} miast")

    iter_number = 30
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

    best_time = min(distances)
    average_result = sum(distances) / iter_number
    average_time = sum(executions) / iter_number

    print("\nWYNIKI DO TABELI W RAPORCIE")
    print(f"Algorytm:           Ant Colony Optimization (EAS)")
    print(f"Najlepszy wynik:    {best_time:.2f}")
    print(f"Średni wynik:       {average_result:.2f}")
    print(f"Średni czas:        {average_time:.4f} s")