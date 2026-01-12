from __future__ import annotations

from statistics import mean, median, pstdev
from typing import Dict, List

from src.config import RunConfig
from src.core.types import Mode
from src.results.models import RunResult

def _best_worst(values: List[float], mode: Mode) -> tuple[float, float]:
    if mode == "min":
        return min(values), max(values)
    return max(values), min(values)

def aggregate_config_results(run_cfg: RunConfig, run_results: List[RunResult]) -> Dict:
    vals = [r.final_gbest_val for r in run_results]
    times = [r.elapsed_s for r in run_results]

    best, worst = _best_worst(vals, run_cfg.mode)

    row = {
        "config_id": "",
        "objective_name": run_cfg.objective_name,
        "mode": run_cfg.mode,
        "n_runs": len(run_results),
        "n_particles": run_cfg.pso.n_particles,
        "n_iterations": run_cfg.pso.n_iterations,
        "w": run_cfg.pso.w,
        "c1": run_cfg.pso.c1,
        "c2": run_cfg.pso.c2,
        "final_best": float(best),
        "final_worst": float(worst),
        "final_min": float(min(vals)),
        "final_max": float(max(vals)),
        "final_mean": float(mean(vals)),
        "final_median": float(median(vals)),
        "final_std": float(pstdev(vals)) if len(vals) > 1 else 0.0,
        "mean_elapsed_s": float(mean(times)),
    }
    return row