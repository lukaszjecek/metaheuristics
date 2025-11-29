import pandas as pd
import random
import time

from agrs_parse import parse_arguments
from genetic import generate_population
from utils import (
    clear_number, fitness, selection, crossover, mutate
)

MAX_WEIGHT = 6_404_180
RUNS = 5

def run_single(items_array, args):
    start = time.time()

    population = generate_population(args.N, len(items_array))
    fitness_values = fitness(population, items_array, MAX_WEIGHT)

    best_history = []
    avg_history = []
    worst_history = []

    for _ in range(args.T):
        parents = selection(population, fitness_values, args.selection_method)

        children = []
        for i in range(0, len(parents), 2):
            p1 = parents[i]
            p2 = parents[(i + 1) % len(parents)]

            if random.random() < args.Pc:
                c1, c2 = crossover(p1, p2, args.crossover_method)
            else:
                c1, c2 = p1[:], p2[:]

            children.append(c1)
            children.append(c2)

        for i in range(len(children)):
            if random.random() < args.Pm:
                children[i] = mutate(children[i], args.mutation_method)

        population = children
        fitness_values = fitness(population, items_array, MAX_WEIGHT)

        best_history.append(max(fitness_values))
        valid = [f for f in fitness_values if f > 0]
        if valid:
            avg_history.append(sum(valid) / len(valid))
        else:
            avg_history.append(0)
        valid = [f for f in fitness_values if f > 0]
        if valid:
            worst_history.append(min(valid))
        else:
            worst_history.append(0)

    best_idx = max(range(len(population)), key=fitness_values.__getitem__)
    best_value = fitness_values[best_idx]
    best_chrom = population[best_idx]

    valid = [(i, f) for i, f in enumerate(fitness_values) if f > 0]

    if valid:
        worst_idx, worst_value = min(valid, key=lambda x: x[1])
        worst_chrom = population[worst_idx]
    else:
        worst_value = 0
        worst_chrom = None

    exec_time = time.time() - start

    return {
        "best_value": best_value,
        "best_chrom": best_chrom,
        "worst_value": worst_value,
        "worst_chrom": worst_chrom,
        "best_history": best_history,
        "avg_history": avg_history,
        "worst_history": worst_history,
        "time": exec_time,
    }

if __name__ == "__main__":
    args = parse_arguments()

    items = pd.read_csv(args.data_file, sep='\t')
    items['Waga (kg)'] = items['Waga (kg)'].apply(clear_number)
    items['Wartość (zł)'] = items['Wartość (zł)'].apply(clear_number)
    items_array = items[['Waga (kg)', 'Wartość (zł)']].to_numpy()

    filename = (
        f"pc{args.Pc}_pm{args.Pm}_n{args.N}_t{args.T}_"
        f"{args.selection_method}_{args.crossover_method}_{args.mutation_method}.csv"
    )

    all_runs = []

    for r in range(RUNS):
        print(f"Run {r+1}/{RUNS} ...")
        res = run_single(items_array, args)
        all_runs.append(res)

    rows = []
    for i, r in enumerate(all_runs):
        rows.append([
            i + 1,
            r["best_value"],
            r["best_chrom"],
            r["worst_value"],
            r["worst_chrom"],
            r["time"],
            r["best_history"],
            r["avg_history"],
            r["worst_history"],
        ])

    df = pd.DataFrame(rows, columns=[
        "run",
        "best_value",
        "best_chromosome",
        "worst_value",
        "worst_chromosome",
        "time_seconds",
        "best_history",
        "avg_history",
        "worst_history",
    ])

    df.to_csv(filename, index=False)
    print("Zapisano:", filename)