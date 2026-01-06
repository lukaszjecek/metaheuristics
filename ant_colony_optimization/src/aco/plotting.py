from __future__ import annotations
from pathlib import Path
from typing import List
import matplotlib.pyplot as plt

from .problem import TSPProblem

def plot_tour(problem: TSPProblem, tour: List[int], out_path: str | Path, title: str = "") -> None:
    xs = [problem.nodes[i].x for i in tour] + [problem.nodes[tour[0]].x]
    ys = [problem.nodes[i].y for i in tour] + [problem.nodes[tour[0]].y]

    plt.figure()
    plt.plot(xs, ys, marker="o")
    for i in tour:
        node = problem.nodes[i]
        plt.text(node.x, node.y, str(node.label))
    if title:
        plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_convergence(best_history: List[float], out_path: str | Path, title: str = "") -> None:
    plt.figure()
    plt.plot(best_history)
    if title:
        plt.title(title)
    plt.xlabel("iteracja")
    plt.ylabel("najlepsza długość trasy")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_convergence_band(
    histories: List[List[float]],
    out_path: str | Path,
    title: str = "",
    band: str = "minmax",
) -> None:
    import math
    T = len(histories[0])
    for h in histories:
        if len(h) != T:
            raise ValueError("Różne długości historii")

    mean = []
    lo = []
    hi = []

    for t in range(T):
        vals = [h[t] for h in histories]
        m = sum(vals) / len(vals)
        mean.append(m)

        if band == "minmax":
            lo.append(min(vals))
            hi.append(max(vals))
        elif band == "std":
            var = sum((x - m) ** 2 for x in vals) / len(vals)
            s = math.sqrt(var)
            lo.append(m - s)
            hi.append(m + s)
        else:
            raise ValueError("band must be 'minmax' or 'std'")

    plt.figure()
    plt.plot(mean)
    plt.fill_between(range(T), lo, hi, alpha=0.2)
    if title:
        plt.title(title)
    plt.xlabel("iteracja")
    plt.ylabel("najlepsza długość trasy")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
