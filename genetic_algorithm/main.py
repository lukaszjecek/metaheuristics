import random

import pandas as pd

from genetic_algorithm.agrs_parse import parse_arguments
from genetic_algorithm.genetic import generate_population
from genetic_algorithm.utils import (
    clear_number, fitness, selection, crossover, mutate
)

MAX_WEIGHT = 6_404_180

if __name__ == "__main__":
    args = parse_arguments()

    items = pd.read_csv(args.data_file, sep='\t')
    items['Waga (kg)'] = items['Waga (kg)'].apply(clear_number)
    items['Wartość (zł)'] = items['Wartość (zł)'].apply(clear_number)
    items_array = items[['Waga (kg)', 'Wartość (zł)']].to_numpy()

    population = generate_population(args.N, len(items))
    fitness_values = fitness(population, items_array, MAX_WEIGHT)

    for _ in range(args.T):
        parents = selection(population, fitness_values, args.selection_method)
        children = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            # if there is odd number of specimens in the population, last specimen will reproduce with the first one
            # list wrapping
            parent2 = parents[(i + 1) % len(parents)]

            if random.random() < args.Pc:
                child1, child2 = crossover(parent1, parent2, args.crossover_method)
            else:
                child1, child2 = parent1[:], parent2[:]

            children.append(child1)
            children.append(child2)

        for i in range(len(children)):
            if random.random() < args.Pm:
                children[i] = mutate(children[i], args.mutation_method)

        population = children
        fitness_values = fitness(population, items, MAX_WEIGHT)