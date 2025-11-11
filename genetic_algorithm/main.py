import pandas as pd
import argparse
import random

MAX_WEIGHT = 6_404_180

def generate_population(population_size, n_items):
    population = []
    for _ in range(population_size):
        chromosome = [random.randint(0, 1) for _ in range(n_items)]
        population.append(chromosome)
    return population

def calculate_fitness(chromosome, items):
    weight = 0
    value = 0
    for idx,gene in enumerate(chromosome):
        if gene == 1:
            weight += items[idx][2]
            value += items[idx][3]
    if weight <= MAX_WEIGHT:
        return value
    else:
        return 0

def roulette_selection(population, fitness_values, n_selected=1):
    total_fitness = sum(fitness_values)

    # if every chromosome in the generated population has 0 fitness function value
    # then every chromosome has equal 1/N probability to bo chosen
    if total_fitness == 0:
        probabilities = [1 / len(population)] * len(population)
    else:
        probabilities = [f / total_fitness for f in fitness_values]

    # creates array of intervals from 0 to 1 for each chromosome represented in the roulette wheel
    # f.e. 0.0 0.1, 0.1 0.4, 0.4 0.6 etc.
    intervals = []
    intervals_sum = 0
    for p in probabilities:
        intervals.append((intervals_sum, intervals_sum + p))
        intervals_sum += p

    #chooses random chromosome according to calculated probability
    selected = []
    for _ in range(n_selected):
        r = random.random()
        for idx, (low, high) in enumerate(intervals):
            if low <= r < high:
                selected.append(population[idx])
                break

    return selected

def clear_number(text):
    return float(str(text).replace(" ", ""))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--Pc', type=float, default=0.6, help="Prawdopodobieństwo krzyżowania")
    parser.add_argument('--Pm', type=float, default=0.05, help="Prawdopodobieństwo mutacji")
    parser.add_argument('--N', type=int, default=30, help="Wielkość populacji")
    parser.add_argument('--T', type=int, default=300, help="Liczba iteracji")
    parser.add_argument('--selection_method', type=str, choices=["roulette", "ranking", "tournament"],
                        help="Metoda selekcji nowego rodzica")
    parser.add_argument('--crossover_method', type=str, choices=["one_point", "two_point", "uniform"],
                        help="Metoda krzyżowania w procesie tworzenia potomstwa")
    parser.add_argument('--mutation_method', type=str, choices=["single_bit_flip", "all_bit_inversion"],
                        default="single_bit_flip", help="Metoda mutacji genów w chromosomie")
    parser.add_argument('--data_file', type=str, default="problem plecakowy dane CSV tabulatory.csv",
                        help="Plik csv z dostępnymi do włożenia do plecaka przedmiotami")

    args = parser.parse_args()

    if args.Pc < 0 or args.Pc > 1.0:
        parser.error("Prawdopodobieństwo krzyżowaniu musi być w zakresie [0, 1].")

    if args.Pm < 0 or args.Pm > 1.0:
        parser.error("Prawdopodobieństwo mutacji musi być w zakresie [0, 1].")

    if args.N <= 0:
        parser.error("Wielkość populacji musi być większa od 0.")

    if args.T <= 0:
        parser.error("Liczba iteracji musi być większa od 0.")

    data = pd.read_csv(args.data_file, sep='\t')
    data['Waga (kg)'] = data['Waga (kg)'].apply(clear_number)
    data['Wartość (zł)'] = data['Wartość (zł)'].apply(clear_number)
    print(f"Wczytano {len(data)} wierszy z pliku: {args.data_file}")
    print(data['Waga (kg)'])
    print(data['Wartość (zł)'])

    population = generate_population(args.N, data.shape[0])
    chromosome = [1 if i == 1 else 0 for i in range(26)]

    print("populacja: ", len(population))
    print("przystosowanie pierwszego chromosomu z populacji:", calculate_fitness(population[0], data.to_numpy()))
    print("fitness dla jednego przedmiotu w plecaku:", calculate_fitness(chromosome, data.to_numpy()))

    population = [
        [0, 1, 0, 1],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [1, 0, 1, 0],
        [1, 1, 1, 1]
    ]

    fitness_values = [10, 30, 20, 5, 1000]

    selected = roulette_selection(population, fitness_values)

    print("Fitnessy:", fitness_values)
    print("Wybrany chromosom:", selected[0])