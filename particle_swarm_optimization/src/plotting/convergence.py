from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt

def _load_history(raw_history_csv: Path) -> Dict[int, List[Tuple[int, float]]]:
    by_run: Dict[int, List[Tuple[int, float]]] = {}
    with raw_history_csv.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            run_id = int(row["run_id"])
            it = int(row["iter"])
            val = float(row["gbest_val"])
            by_run.setdefault(run_id, []).append((it, val))
    for k in by_run:
        by_run[k].sort(key=lambda t: t[0])
    return by_run

def plot_convergence_all_runs(raw_history_csv: Path, out_path: Path, title: str) -> None:
    by_run = _load_history(raw_history_csv)

    plt.figure()
    for run_id, series in sorted(by_run.items(), key=lambda kv: kv[0]):
        xs = [t[0] for t in series]
        ys = [t[1] for t in series]
        plt.plot(xs, ys, label=f"run {run_id}")

    plt.xlabel("iteration")
    plt.ylabel("gbest_val")
    plt.title(title)
    plt.legend(loc="best", fontsize="small")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()

def plot_convergence_single_run(raw_history_csv: Path, run_id: int, out_path: Path, title: str) -> None:
    by_run = _load_history(raw_history_csv)
    if run_id not in by_run:
        raise KeyError(f"run_id={run_id} not found in {raw_history_csv}. Available: {sorted(by_run.keys())}")

    series = by_run[run_id]
    xs = [t[0] for t in series]
    ys = [t[1] for t in series]

    plt.figure()
    plt.plot(xs, ys)
    plt.xlabel("iteration")
    plt.ylabel("gbest_val")
    plt.title(title)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()