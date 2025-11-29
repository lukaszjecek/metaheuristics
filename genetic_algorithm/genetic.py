import random

def generate_population(population_size, n_items):
    population = []
    for _ in range(population_size):
        chromosome = [random.randint(0, 1) for _ in range(n_items)]
        population.append(chromosome)
    return population

def calculate_fitness(chromosome, items, max_weight):
    weight = 0
    value = 0
    for idx,gene in enumerate(chromosome):
        if gene == 1:
            weight += items[idx][0]
            value += items[idx][1]
    if weight <= max_weight:
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
        else:
            # protection against missing selection due to numerical instability
            selected.append(population[-3])

    return selected

def ranking_selection(population, fitness_values, n_selected=1):
    indexed = list(zip(population, fitness_values))
    indexed.sort(key=lambda x: x[1])

    ranks = list(range(1, len(indexed) + 1))
    total_rank = sum(ranks)

    probabilities = [r / total_rank for r in ranks]
    intervals = []
    s = 0
    for p in probabilities:
        intervals.append((s, s + p))
        s += p

    selected = []
    for _ in range(n_selected):
        r = random.random()
        for idx, (low, high) in enumerate(intervals):
            if low <= r < high:
                selected.append(indexed[idx][0])
                break
        else:
            selected.append(indexed[-1][0])

    return selected

def tournament_selection(population, fitness_values, n_selected=1, tournament_size=4):
    selected = []
    for _ in range(n_selected):
        participants_idx = random.sample(range(len(population)), tournament_size)
        best_idx = max(participants_idx, key=fitness_values.__getitem__)
        selected.append(population[best_idx])
    return selected

def one_point_crossover(parent1, parent2):
    pivot = random.randint(1, len(parent1) - 1)
    child1 = parent1[:pivot] + parent2[pivot:]
    child2 = parent2[:pivot] + parent1[pivot:]
    return child1, child2

def two_point_crossover(parent1, parent2):
    pivot1, pivot2 = sorted(random.sample(range(1, len(parent1)), 2))
    child1 = parent1[:pivot1] + parent2[pivot1:pivot2] + parent1[pivot2:]
    child2 = parent2[:pivot1] + parent1[pivot1:pivot2] + parent2[pivot2:]
    return child1, child2

def uniform_crossover(parent1, parent2):
    mask = [random.randint(0, 1) for _ in range(len(parent1))]
    child1, child2 = parent1[:], parent2[:]
    for i in range(len(parent1)):
        if mask[i] == 1:
            child1[i] = parent2[i]
            child2[i] = parent1[i]

    return child1, child2

def mutate_single_gene(chromosome):
    idx = random.randrange(len(chromosome))
    chromosome[idx] = 1 - chromosome[idx]
    return chromosome

def chromosome_all_gene_inversion(chromosome):
    for idx in range(len(chromosome)):
        chromosome[idx] = 1 - chromosome[idx]
    return chromosome