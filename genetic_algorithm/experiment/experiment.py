import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import random
import time
import matplotlib.pyplot as plt

from agrs_parse import parse_arguments
from genetic import generate_population
from utils import (
    clear_number, fitness, selection, crossover, mutate
)

MAX_WEIGHT = 6_404_180
RUNS = 5

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def plot_progress(run_id, best_hist, avg_hist, worst_hist, outdir):
    plt.figure(figsize=(10, 6))
    plt.plot(best_hist, label="Best", linewidth=2)
    plt.plot(avg_hist, label="Average", linestyle="--")
    plt.plot(worst_hist, label="Worst", linestyle=":")
    plt.xlabel("Iteration")
    plt.ylabel("Fitness")
    plt.title(f"Run {run_id} – Progress")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"run_{run_id}_progress.png"))
    plt.close()

def plot_all_runs_best_histories(all_runs, outdir):
    plt.figure(figsize=(10, 6))
    for i, r in enumerate(all_runs):
        plt.plot(r["best_history"], label=f"Run {i+1}")
    plt.xlabel("Iteration")
    plt.ylabel("Fitness")
    plt.title("Best history – all runs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "all_runs_best_history.png"))
    plt.close()

def plot_boxplot_best_values(all_runs, outdir):
    best_values = [r["best_value"] for r in all_runs]
    plt.figure(figsize=(8, 6))
    plt.boxplot(best_values, vert=True)
    plt.ylabel("Best fitness value")
    plt.title("Best values – boxplot (5 runs)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "best_value_boxplot.png"))
    plt.close()

def plot_mean_best_history(all_runs, outdir):
    T = len(all_runs[0]["best_history"])
    mean_history = []

    for t in range(T):
        mean_history.append(
            sum(r["best_history"][t] for r in all_runs) / len(all_runs)
        )

    plt.figure(figsize=(10, 6))
    plt.plot(mean_history, linewidth=2)
    plt.xlabel("Iteration")
    plt.ylabel("Fitness")
    plt.title("Mean best history (average of 5 runs)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "mean_best_history.png"))
    plt.close()


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

        avg_history.append(sum(valid) / len(valid) if valid else 0)
        worst_history.append(min(valid) if valid else 0)

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

    items = pd.read_csv(args.data_file, sep="\t")
    items["Waga (kg)"] = items["Waga (kg)"].apply(clear_number)
    items["Wartość (zł)"] = items["Wartość (zł)"].apply(clear_number)
    items_array = items[["Waga (kg)", "Wartość (zł)"]].to_numpy()

    dirname = (
        f"pc{args.Pc}_pm{args.Pm}_n{args.N}_t{args.T}_"
        f"{args.selection_method}_{args.crossover_method}_{args.mutation_method}"
    )
    outdir = os.path.join("results", dirname)
    ensure_dir(outdir)

    print("Saving results to:", outdir)

    all_runs = []

    for r in range(RUNS):
        print(f"Run {r+1}/{RUNS} ...")
        res = run_single(items_array, args)
        all_runs.append(res)

        plot_progress(
            r + 1,
            res["best_history"],
            res["avg_history"],
            res["worst_history"],
            outdir,
        )

    plot_all_runs_best_histories(all_runs, outdir)
    plot_boxplot_best_values(all_runs, outdir)
    plot_mean_best_history(all_runs, outdir)

    rows = []
    for i, r in enumerate(all_runs):
        rows.append([
            args.Pc,
            args.Pm,
            args.N,
            args.T,
            args.selection_method,
            args.crossover_method,
            args.mutation_method,
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
        "Pc",
        "Pm",
        "N",
        "T",
        "selection_method",
        "crossover_method",
        "mutation_method",
        "run_id",
        "best_value",
        "best_chromosome",
        "worst_value",
        "worst_chromosome",
        "time_seconds",
        "best_history",
        "avg_history",
        "worst_history",
    ])

    csv_path = os.path.join(
        outdir,
        f"pc{args.Pc}_pm{args.Pm}_n{args.N}_t{args.T}_{args.selection_method}_{args.crossover_method}_{args.mutation_method}.csv"
    )

    df.to_csv(csv_path, index=False)
    print("CSV saved:", csv_path)