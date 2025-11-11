# more of a demonstration than a test

import pandas as pd

from genetic import *
from utils import *

MAX_WEIGHT = 6_404_180

class Args:
    data_file = "data/problem plecakowy dane CSV tabulatory.csv"
    N = 30


args = Args()
data = pd.read_csv(args.data_file, sep='\t')
data['Waga (kg)'] = data['Waga (kg)'].apply(clear_number)
data['Wartość (zł)'] = data['Wartość (zł)'].apply(clear_number)

print("-" * 40)
print(f"Wczytano {len(data)} wierszy z pliku: {args.data_file}")
print("-" * 40)
print(data['Waga (kg)'])
print("-" * 40)
print(data['Wartość (zł)'])

population = generate_population(args.N, data.shape[0])
chromosome = [1 if i == 1 else 0 for i in range(26)]

print("-" * 40)
print("populacja: ", len(population))
print("przystosowanie pierwszego chromosomu z populacji:", calculate_fitness(population[0], data.to_numpy(), MAX_WEIGHT))
print("fitness dla jednego przedmiotu w plecaku:", calculate_fitness(chromosome, data.to_numpy(), MAX_WEIGHT))

population = [
    [0, 1, 0, 1],
    [1, 1, 0, 0],
    [0, 0, 1, 1],
    [1, 0, 1, 0],
    [1, 1, 1, 1]
]

fitness_values = [10, 30, 20, 5, 1000]

selected = roulette_selection(population, fitness_values)

print("-" * 40)
print("fitnessy:", fitness_values)
print("wybrany chromosom:", selected[0])

parent1 = [1, 0, 1, 0, 1, 0, 1, 0]
parent2 = [0, 1, 0, 1, 0, 1, 0, 1]

print("-" * 40)
print("rodzic 1:", parent1)
print("rodzic 2:", parent2)
print("-" * 40)

c1, c2 = one_point_crossover(parent1, parent2)
print("ONE-POINT CROSSOVER")
print("dziecko 1:", c1)
print("dziecko 2:", c2)
print("-" * 40)

c1, c2 = two_point_crossover(parent1, parent2)
print("TWO-POINT CROSSOVER")
print("dziecko 1:", c1)
print("dziecko 2:", c2)
print("-" * 40)

c1, c2 = uniform_crossover(parent1, parent2)
print("UNIFORM CROSSOVER")
print("dziecko 1:", c1)
print("dziecko 2:", c2)
print("-" * 40)