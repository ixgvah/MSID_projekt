import random


class GeneticAlgorithm:


    def __init__(
        self,
        problem,
        population_size = 100,   # liczba tras w jednym pokoleniu
        n_generations   = 300,   # liczba iteracji (pokoleń) algorytmu
        crossover_rate  = 0.85,  # prawdopodobieństwo krzyżowania dwóch rodziców
        mutation_rate   = 0.02,  # prawdopodobieństwo mutacji jednego miasta
        tournament_size = 5,     # ilu kandydatów bierze udział w turnieju selekcji
        elite_count     = 2,     # ile najlepszych tras kopiujemy bez zmian do kolejnego pokolenia
    ):
        self.problem         = problem
        self.city_count      = problem.n_cities   # liczba miast do odwiedzenia
        self.distance_matrix = problem.distances  # macierz odległości między miastami

        self.population_size = population_size
        self.n_generations   = n_generations
        self.crossover_rate  = crossover_rate
        self.mutation_rate   = mutation_rate
        self.tournament_size = tournament_size
        self.elite_count     = elite_count

    #inicjalizacja populacji

    def _random_route(self):
        route = list(range(self.city_count))
        random.shuffle(route)
        return route

    def _initial_population(self):
        return [self._random_route() for _ in range(self.population_size)]

    #ocena populacji

    def _score_population(self, population):
    
        scored = [(self.problem.evaluate(route), route) for route in population]
        scored.sort(key=lambda entry: entry[0])
        return scored

    #selekcja

    def _tournament_select(self, scored_population):

        competitors = random.sample(scored_population, self.tournament_size)
        winner      = min(competitors, key=lambda entry: entry[0])
        return winner[1]   # zwracamy samą trasę (bez dystansu)

   #krzyżowanie

    def _order_crossover(self, parent_a, parent_b):
        
        size = self.city_count

        seg_start, seg_end = sorted(random.sample(range(size), 2))   # granice segmentu

        child = [-1] * size
        child[seg_start : seg_end + 1] = parent_a[seg_start : seg_end + 1]  # krok 1

        inherited_cities  = set(child[seg_start : seg_end + 1])              # miasta już wstawione
        remaining_cities  = [city for city in parent_b if city not in inherited_cities]  # krok 2
        empty_positions   = [pos for pos in range(size) if child[pos] == -1]

        for position, city in zip(empty_positions, remaining_cities):
            child[position] = city

        return child

    
    #mutacja przez zmiane

    def _swap_mutation(self, route):
       
        mutated_route = route[:]   # kopia, żeby nie modyfikować oryginału

        for index in range(self.city_count):
            if random.random() < self.mutation_rate:
                swap_index                        = random.randint(0, self.city_count - 1)
                mutated_route[index], mutated_route[swap_index] = (
                    mutated_route[swap_index], mutated_route[index]
                )

        return mutated_route

   #głowna pętla ewolucji

    def run(self):
        """
        Uruchamia algorytm genetyczny.

        Schemat każdego pokolenia:
          1. Oceń całą populację (oblicz dystanse, posortuj).
          2. Zapisz elitę — najlepsze trasy przechodzą bez zmian.
          3. Uzupełnij nowe pokolenie:
             selekcja turniejowa → krzyżowanie OX → mutacja swap.
          4. Powtarzaj przez 'n_generations' pokoleń.

        Zwraca: (najlepsza_trasa, najlepszy_dystans)
        """
        population    = self._initial_population()
        best_route    = None
        best_distance = float('inf')

        for _ in range(self.n_generations):

            scored_population = self._score_population(population)

            # aktualizacja globalnie najlepszego wyniku
            top_distance, top_route = scored_population[0]
            if top_distance < best_distance:
                best_distance = top_distance
                best_route    = top_route[:]

            # elityzm — najlepsze trasy kopiujemy wprost do nowego pokolenia
            next_generation = [route for (_, route) in scored_population[:self.elite_count]]

            # tworzenie reszty nowego pokolenia
            while len(next_generation) < self.population_size:
                parent_a = self._tournament_select(scored_population)
                parent_b = self._tournament_select(scored_population)

                if random.random() < self.crossover_rate:
                    child = self._order_crossover(parent_a, parent_b)  # krzyżowanie
                else:
                    child = parent_a[:]                                  # klon rodzica

                child = self._swap_mutation(child)                       # mutacja
                next_generation.append(child)

            population = next_generation

        return best_route, best_distance