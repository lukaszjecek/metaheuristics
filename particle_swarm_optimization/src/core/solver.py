from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from src.config import PSOConfig
from src.core.compare_value import is_strictly_better
from src.core.types import Objective2D, VMax
from src.results.models import RunResult
from src.utils.math_utils import compute_vmax, clamp_with_reflect_damping
from src.utils.time_utils import perf_counter_s

class PSOSolver:
    def __init__(self, objective: Objective2D, pso: PSOConfig):
        self.objective = objective
        self.pso = pso
        self.pso.validate()

    def run(self, seed: int | None) -> RunResult:
        rng = np.random.default_rng(seed)

        (xmin, xmax), (ymin, ymax) = self.objective.bounds
        vmax = compute_vmax(self.objective.bounds, fraction=self.pso.vmax_fraction, eps=self.pso.eps)

        n = self.pso.n_particles
        iters = self.pso.n_iterations

        x = rng.uniform(xmin, xmax, size=n)
        y = rng.uniform(ymin, ymax, size=n)
        vx = np.zeros(n, dtype=float)
        vy = np.zeros(n, dtype=float)

        vals = np.array([self.objective.evaluate(float(xi), float(yi)) for xi, yi in zip(x, y)], dtype=float)
        pbest_x = x.copy()
        pbest_y = y.copy()
        pbest_val = vals.copy()

        gbest_idx = int(np.argmin(vals) if self.pso.mode == "min" else np.argmax(vals))
        gbest_x = float(x[gbest_idx])
        gbest_y = float(y[gbest_idx])
        gbest_val = float(vals[gbest_idx])

        history: List[Tuple[int, float]] = [(0, gbest_val)]

        snapshot_iters = {0, iters // 2, iters}
        snapshots: Dict[int, np.ndarray] = {}
        if 0 in snapshot_iters:
            snapshots[0] = np.column_stack([x.copy(), y.copy()])

        t0 = perf_counter_s()
        for i in range(1, iters + 1):
            r1x = rng.random(n)
            r1y = rng.random(n)
            r2x = rng.random(n)
            r2y = rng.random(n)

            vx = (
                self.pso.w * vx
                + self.pso.c1 * r1x * (pbest_x - x)
                + self.pso.c2 * r2x * (gbest_x - x)
            )
            vy = (
                self.pso.w * vy
                + self.pso.c1 * r1y * (pbest_y - y)
                + self.pso.c2 * r2y * (gbest_y - y)
            )

            vx = np.clip(vx, -vmax.vmax_x, vmax.vmax_x)
            vy = np.clip(vy, -vmax.vmax_y, vmax.vmax_y)

            x = x + vx
            y = y + vy

            x, vx = clamp_with_reflect_damping(x, vx, xmin, xmax, k=self.pso.boundary_reflect_damping_k)
            y, vy = clamp_with_reflect_damping(y, vy, ymin, ymax, k=self.pso.boundary_reflect_damping_k)

            vals = np.array([self.objective.evaluate(float(xi), float(yi)) for xi, yi in zip(x, y)], dtype=float)

            tol = self.pso.compare_tol
            for idx in range(n):
                v = float(vals[idx])
                if is_strictly_better(v, float(pbest_val[idx]), self.pso.mode, tol):
                    pbest_val[idx] = v
                    pbest_x[idx] = x[idx]
                    pbest_y[idx] = y[idx]

                if is_strictly_better(v, gbest_val, self.pso.mode, tol):
                    gbest_val = v
                    gbest_x = float(x[idx])
                    gbest_y = float(y[idx])

            history.append((i, gbest_val))

            if i in snapshot_iters:
                snapshots[i] = np.column_stack([x.copy(), y.copy()])

        elapsed = perf_counter_s() - t0

        return RunResult(
            run_id=0,
            seed=seed,
            elapsed_s=elapsed,
            final_gbest_val=gbest_val,
            final_gbest_x=gbest_x,
            final_gbest_y=gbest_y,
            history=history,
            snapshots=snapshots,
            pso_config=self.pso,
            objective_name=self.objective.name,
            bounds=self.objective.bounds,
            mode=self.pso.mode,
        )

    def run_multiple(self, n_runs: int, master_seed: int | None) -> List[RunResult]:
        master_rng = np.random.default_rng(master_seed)
        run_seeds = [int(master_rng.integers(0, 2**32 - 1)) for _ in range(n_runs)]

        results: List[RunResult] = []
        for run_id, seed in enumerate(run_seeds):
            rr = self.run(seed=seed)
            rr.run_id = run_id
            results.append(rr)
        return results