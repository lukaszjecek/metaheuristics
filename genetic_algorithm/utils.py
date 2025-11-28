import math

from genetic_algorithm.genetic import (
    one_point_crossover, two_point_crossover, uniform_crossover,
    mutate_single_gene, chromosome_all_gene_inversion, roulette_selection, ranking_selection, tournament_selection,
    calculate_fitness
)

def clear_number(text):
    return float(str(text).replace(" ", ""))

def auto_tournament_size(population_size):
    return max(2, int(math.log2(population_size)))

def selection(population, items, max_weight, method):
    population_size = len(population)

    fitness_values = [
        calculate_fitness(chromosome, items, max_weight)
        for chromosome in population
    ]

    if method == "roulette":
        return roulette_selection(population, fitness_values, population_size)
    elif method == "ranking":
        return ranking_selection(population, fitness_values, population_size)
    elif method == "tournament":
        ts = auto_tournament_size(population_size)
        return tournament_selection(population, fitness_values, population_size, ts)
    else:
        raise ValueError('Method must be one of "roulette", "ranking", "tournament"')

def crossover(parent1, parent2, method):
    if method == 'one_point':
        return one_point_crossover(parent1, parent2)
    elif method == 'two_point':
        return two_point_crossover(parent1, parent2)
    elif method == 'uniform':
        return uniform_crossover(parent1, parent2)
    else:
        raise ValueError('Method must be one of "one_point", "two_point", "uniform"')

def mutate(chromosome, method):
    if method == 'single_bit_flip':
        return mutate_single_gene(chromosome)
    elif method == 'all_bit_inversion':
        return chromosome_all_gene_inversion(chromosome)
    else:
        raise ValueError('Method must be one of "single_bit_flip", "all_bit_inversion"')