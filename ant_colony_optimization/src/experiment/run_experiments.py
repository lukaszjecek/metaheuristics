from __future__ import annotations
from pathlib import Path
from typing import Dict, List

import argparse
import csv
import time
import statistics
import matplotlib.pyplot as plt

from ..aco.io import load_nodes
from ..aco.problem import build_problem, TSPProblem
from ..aco.solver import ACOConfig, ACOSolver, ACOResult
from ..aco.plotting import plot_tour, plot_convergence_band

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def cfg_to_tag(cfg: ACOConfig) -> str:
    return (
        f"m{cfg.m}_T{cfg.T}_a{cfg.alpha}_b{cfg.beta}"
        f"_rho{cfg.rho}_pr{cfg.p_random}"
    )

def save_runs_csv(path: Path, rows: List[Dict]) -> None:
    if not rows:
        return
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

def save_history_csv(path: Path, histories: List[List[float]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["iter", "run_id", "best_length"])
        for run_id, hist in enumerate(histories):
            for it, val in enumerate(hist):
                w.writerow([it, run_id, val])

def save_population_history_csv(path: Path, results: List[ACOResult]) -> None:
    ensure_dir(path.parent)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["iter", "run_id", "iter_best", "iter_mean", "iter_worst"])
        for run_id, res in enumerate(results):
            T = len(res.iter_best)
            for it in range(T):
                w.writerow([it, run_id, res.iter_best[it], res.iter_mean[it], res.iter_worst[it]])

def save_best_tour_csv(path: Path, problem: TSPProblem, tour: List[int], length: float) -> None:
    ensure_dir(path.parent)
    labels = [problem.nodes[i].label for i in tour]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["best_length", length])
        w.writerow(["tour_labels"])
        w.writerow(labels)

def compute_stats(values: List[float]) -> Dict[str, float]:
    mean = statistics.fmean(values)
    median = statistics.median(values)
    std = statistics.pstdev(values) if len(values) > 1 else 0.0
    return {
        "best_min": min(values),
        "best_mean": mean,
        "best_median": median,
        "best_std": std,
        "best_max": max(values),
    }

def run_one(problem: TSPProblem, cfg: ACOConfig) -> ACOResult:
    solver = ACOSolver(problem, cfg)
    return solver.solve()

def plot_param_comparisons(summary_rows: List[Dict], out_dir: Path) -> None:
    params = ["m", "T", "alpha", "beta", "rho", "p_random"]
    y_key = "best_mean"

    for p in params:
        xs = sorted(set(row[p] for row in summary_rows))
        if len(xs) <= 1:
            continue

        x_to_vals: Dict[float, List[float]] = {x: [] for x in xs}
        for row in summary_rows:
            x_to_vals[row[p]].append(row[y_key])

        x_plot: List[float] = []
        y_plot: List[float] = []
        for x in xs:
            x_plot.append(x)
            y_plot.append(statistics.fmean(x_to_vals[x]))

        plt.figure()
        plt.plot(x_plot, y_plot, marker="o")
        plt.xlabel(p)
        plt.ylabel(y_key)
        plt.title(f"Porównanie parametru {p} względem {y_key}")
        plt.tight_layout()
        plt.savefig(out_dir / f"compare_{p}.png")
        plt.close()

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_file", type=str, required=True)
    ap.add_argument("--out_dir", type=str, default="results/experiments")
    ap.add_argument("--repeats", type=int, default=5)

    ap.add_argument("--m_list", type=int, nargs="+", default=[10, 20, 50])
    ap.add_argument("--T_list", type=int, nargs="+", default=[50, 100])
    ap.add_argument("--alpha_list", type=float, nargs="+", default=[1.0])
    ap.add_argument("--beta_list", type=float, nargs="+", default=[5.0])
    ap.add_argument("--rho_list", type=float, nargs="+", default=[0.3])
    ap.add_argument("--p_random_list", type=float, nargs="+", default=[0.01])

    args = ap.parse_args()

    nodes = load_nodes(args.data_file)
    problem = build_problem(nodes)

    base_out = Path(args.out_dir)
    ensure_dir(base_out)

    configs: List[ACOConfig] = []
    for m in args.m_list:
        for T in args.T_list:
            for alpha in args.alpha_list:
                for beta in args.beta_list:
                    for rho in args.rho_list:
                        for pr in args.p_random_list:
                            configs.append(ACOConfig(m=m, T=T, alpha=alpha, beta=beta, rho=rho, p_random=pr))

    print(f"Configurations: {len(configs)} | repeats: {args.repeats}")

    summary_rows: List[Dict] = []

    for cfg in configs:
        tag = cfg_to_tag(cfg)
        cfg_dir = base_out / tag
        ensure_dir(cfg_dir)

        run_rows: List[Dict] = []
        histories: List[List[float]] = []
        results: List[ACOResult] = []

        best_overall_len = float("inf")
        best_overall_tour: List[int] = []

        for r in range(args.repeats):
            t0 = time.perf_counter()
            res = run_one(problem, cfg)
            elapsed = time.perf_counter() - t0

            results.append(res)
            histories.append(res.best_history)

            save_best_tour_csv(cfg_dir / f"best_tour_run_{r}.csv", problem, res.best_tour, res.best_length)

            if res.best_length < best_overall_len:
                best_overall_len = res.best_length
                best_overall_tour = res.best_tour

            run_rows.append(
                {
                    "run_id": r,
                    "best_length": res.best_length,
                    "elapsed_s": elapsed,
                    "m": cfg.m,
                    "T": cfg.T,
                    "alpha": cfg.alpha,
                    "beta": cfg.beta,
                    "rho": cfg.rho,
                    "p_random": cfg.p_random,
                }
            )

            print(f"{tag} | run {r+1}/{args.repeats}: best={res.best_length:.3f} time={elapsed:.3f}s")

        save_runs_csv(cfg_dir / "runs.csv", run_rows)
        save_history_csv(cfg_dir / "history.csv", histories)
        save_population_history_csv(cfg_dir / "population_history.csv", results)
        save_best_tour_csv(cfg_dir / "best_tour_overall.csv", problem, best_overall_tour, best_overall_len)

        plot_convergence_band(
            histories=histories,
            out_path=cfg_dir / "convergence_mean_minmax.png",
            title=f"Średnia z {args.repeats} uruchomień (min–max) | {tag}",
            band="minmax",
        )
        plot_tour(
            problem=problem,
            tour=best_overall_tour,
            out_path=cfg_dir / "best_tour.png",
            title=f"Najlepsza trasa overall = {best_overall_len:.3f} | {tag}",
        )

        best_lengths = [row["best_length"] for row in run_rows]
        stats = compute_stats(best_lengths)

        summary_row = {
            "config_dir": str(cfg_dir),
            "tag": tag,
            "n_runs": args.repeats,
            "m": cfg.m,
            "T": cfg.T,
            "alpha": cfg.alpha,
            "beta": cfg.beta,
            "rho": cfg.rho,
            "p_random": cfg.p_random,
            **stats,
            "mean_elapsed_s": statistics.fmean([row["elapsed_s"] for row in run_rows]),
        }
        summary_rows.append(summary_row)

    save_runs_csv(base_out / "summary.csv", summary_rows)
    plot_param_comparisons(summary_rows, base_out)

    print("DONE")


if __name__ == "__main__":
    main()