from __future__ import annotations

import csv
import json
import platform
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from src.config import RunConfig
from src.results.models import RunResult
from src.utils.time_utils import iso_timestamp

class ResultsWriter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def write_meta_config_single(self, run_cfg: RunConfig, result: RunResult) -> None:
        meta = self._build_meta_base(run_cfg)
        meta["randomness"]["seed_strategy"] = "fixed" if run_cfg.seed is not None else "auto"
        meta["randomness"]["master_seed"] = run_cfg.seed
        meta["randomness"]["run_seeds"] = [result.seed]
        meta["run_info"]["timestamp_start"] = iso_timestamp()
        meta["run_info"]["output_dir"] = str(self.output_dir)
        meta["run_info"]["paths"] = self._paths_dict()

        self._write_json(self.output_dir / "meta_config.json", meta)

    def write_meta_config_experiment(self, run_cfg: RunConfig, run_results: List[RunResult]) -> None:
        meta = self._build_meta_base(run_cfg)
        meta["randomness"]["seed_strategy"] = "fixed" if run_cfg.seed is not None else "auto"
        meta["randomness"]["master_seed"] = run_cfg.seed
        meta["randomness"]["run_seeds"] = [r.seed for r in run_results]
        meta["run_info"]["timestamp_start"] = iso_timestamp()
        meta["run_info"]["output_dir"] = str(self.output_dir)
        meta["run_info"]["paths"] = self._paths_dict()
        self._write_json(self.output_dir / "meta_config.json", meta)

    def write_raw_runs(self, run_cfg: RunConfig, run_results: List[RunResult]) -> None:
        path = self.output_dir / "raw_runs.csv"
        rows: List[Dict[str, Any]] = []
        for r in run_results:
            rows.append(
                {
                    "run_id": r.run_id,
                    "seed": r.seed,
                    "objective_name": run_cfg.objective_name,
                    "mode": run_cfg.mode,
                    "bounds": str(run_cfg.bounds),
                    "n_particles": run_cfg.pso.n_particles,
                    "n_iterations": run_cfg.pso.n_iterations,
                    "w": run_cfg.pso.w,
                    "c1": run_cfg.pso.c1,
                    "c2": run_cfg.pso.c2,
                    "elapsed_s": f"{r.elapsed_s:.9f}",
                    "final_gbest_val": r.final_gbest_val,
                    "final_gbest_x": r.final_gbest_x,
                    "final_gbest_y": r.final_gbest_y,
                }
            )
        self._write_csv(path, rows)

    def write_raw_history(self, run_cfg: RunConfig, run_results: List[RunResult]) -> None:
        path = self.output_dir / "raw_history.csv"
        rows: List[Dict[str, Any]] = []
        for r in run_results:
            for it, val in r.history:
                rows.append(
                    {
                        "run_id": r.run_id,
                        "seed": r.seed,
                        "objective_name": run_cfg.objective_name,
                        "mode": run_cfg.mode,
                        "iter": it,
                        "gbest_val": val,
                    }
                )
        self._write_csv(path, rows)

    def write_agg_summary(self, agg_row: Dict[str, Any]) -> None:
        path = self.output_dir / "agg_summary.csv"
        self._write_csv(path, [agg_row])

    def write_agg_summary_all(self, agg_rows: List[Dict[str, Any]], out_path: Path) -> None:
        self._write_csv(out_path, agg_rows)

    def _paths_dict(self) -> Dict[str, str]:
        return {
            "meta_config.json": str(self.output_dir / "meta_config.json"),
            "raw_runs.csv": str(self.output_dir / "raw_runs.csv"),
            "raw_history.csv": str(self.output_dir / "raw_history.csv"),
            "agg_summary.csv": str(self.output_dir / "agg_summary.csv"),
            "plots_dir": str(self.output_dir / "plots"),
        }

    def _build_meta_base(self, run_cfg: RunConfig) -> Dict[str, Any]:
        p = run_cfg.pso
        return {
            "problem": {
                "objective_name": run_cfg.objective_name,
                "dimension": 2,
                "bounds": [list(run_cfg.bounds[0]), list(run_cfg.bounds[1])],
                "mode": run_cfg.mode,
            },
            "pso": {
                "n_particles": p.n_particles,
                "n_iterations": p.n_iterations,
                "w": p.w,
                "c1": p.c1,
                "c2": p.c2,
                "velocity_init": 0,
                "vmax_policy": "fraction_of_range",
                "vmax_fraction": p.vmax_fraction,
                "eps": p.eps,
                "boundary_handling": "clamp_reflect_damping",
                "boundary_reflect_damping_k": p.boundary_reflect_damping_k,
                "compare_tol": p.compare_tol,
            },
            "randomness": {
                "rng_library": "numpy.random.default_rng",
            },
            "run_info": {
                "timestamp_start": None,
                "output_dir": None,
                "paths": {},
                "python_version": platform.python_version(),
                "platform": platform.platform(),
                "numpy_version": np.__version__,
            },
        }

    def _write_json(self, path: Path, obj: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    def _write_csv(self, path: Path, rows: List[Dict[str, Any]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not rows:
            path.write_text("", encoding="utf-8")
            return

        fieldnames = list(rows[0].keys())
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)