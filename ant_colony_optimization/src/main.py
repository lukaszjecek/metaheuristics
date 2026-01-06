from __future__ import annotations
from pathlib import Path

import argparse
import csv

from src.aco.io import load_nodes
from src.aco.problem import build_problem
from src.aco.solver import ACOConfig, ACOSolver
from src.aco.plotting import plot_tour, plot_convergence

def save_history_csv(path: Path, history: list[float]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["iter", "best_length"])
        for i, v in enumerate(history):
            w.writerow([i, v])

def save_best_tour_csv(path: Path, labels: list[int], length: float) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["best_length", length])
        w.writerow(["tour_labels"])
        w.writerow(labels)
        
def save_runs_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_file", type=str, default="data/A-n32-k5.txt")
    ap.add_argument("--out_dir", type=str, default="results/demo")
    ap.add_argument("--m", type=int, default=20)
    ap.add_argument("--T", type=int, default=100)
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--beta", type=float, default=5.0)
    ap.add_argument("--rho", type=float, default=0.3)
    ap.add_argument("--p_random", type=float, default=0.01)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes = load_nodes(args.data_file)
    problem = build_problem(nodes)

    cfg = ACOConfig(
        m=args.m,
        T=args.T,
        alpha=args.alpha,
        beta=args.beta,
        rho=args.rho,
        p_random=args.p_random,
    )
    solver = ACOSolver(problem, cfg)
    res = solver.solve()

    labels = [problem.nodes[i].label for i in res.best_tour]
    save_best_tour_csv(out_dir / "best_tour.csv", labels, res.best_length)
    save_history_csv(out_dir / "convergence.csv", res.best_history)

    plot_tour(problem, res.best_tour, out_dir / "best_tour.png",
              title=f"Best length = {res.best_length:.3f}")
    plot_convergence(res.best_history, out_dir / "convergence.png",
                     title="Convergence")

    print(f"Best length: {res.best_length:.6f}")
    print(f"Elapsed [s]: {res.elapsed_s:.3f}")
    print(f"Best tour (labels): {labels}")

    run_summary = {
        "data_file": args.data_file,
        "m": args.m,
        "T": args.T,
        "alpha": args.alpha,
        "beta": args.beta,
        "rho": args.rho,
        "p_random": args.p_random,
        "best_length": res.best_length,
        "elapsed_s": res.elapsed_s,
    }
    save_runs_csv(out_dir / "run_summary.csv", [run_summary])

if __name__ == "__main__":
    main()