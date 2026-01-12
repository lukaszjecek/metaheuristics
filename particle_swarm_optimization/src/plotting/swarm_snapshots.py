from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import matplotlib.pyplot as plt

from src.core.types import Bounds, Objective2D
from src.utils.math_utils import make_meshgrid_on_bounds

def plot_swarm_snapshots_0_mid_end(
    objective: Objective2D,
    bounds: Bounds,
    snapshots: Dict[int, np.ndarray],
    n_iterations: int,
    out_path: Path,
    title: str,
    grid_size: int = 200,
) -> None:
    it0 = 0
    it_mid = n_iterations // 2
    it_end = n_iterations

    for it in (it0, it_mid, it_end):
        if it not in snapshots:
            raise KeyError(f"Missing snapshot for iter={it}. Present keys: {sorted(snapshots.keys())}")

    X, Y = make_meshgrid_on_bounds(bounds, grid_size=grid_size)
    Z = np.empty_like(X, dtype=float)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = objective.evaluate(float(X[i, j]), float(Y[i, j]))

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True, sharey=True)
    fig.suptitle(title)

    panels = [
        (it0, "iter = 0"),
        (it_mid, f"iter = {it_mid}"),
        (it_end, f"iter = {it_end}"),
    ]

    for ax, (it, subtitle) in zip(axes, panels):
        ax.contourf(X, Y, Z, levels=30)
        pts = snapshots[it]
        ax.scatter(pts[:, 0], pts[:, 1], s=12, c="red")
        ax.set_title(subtitle)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close(fig)