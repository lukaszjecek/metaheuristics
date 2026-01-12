from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt

def _group_by(agg_rows: List[Dict[str, Any]], key_fields: Tuple[str, ...]) -> Dict[Tuple[Any, ...], List[Dict[str, Any]]]:
    g: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
    for row in agg_rows:
        key = tuple(row[k] for k in key_fields)
        g[key].append(row)
    return g

def plot_parameter_influence(agg_rows: List[dict], out_dir: Path, mode: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    by_obj = _group_by(agg_rows, ("objective_name", "mode"))
    for (objective_name, mode_val), rows in by_obj.items():
        for param in ("w", "c1", "c2", "n_particles", "n_iterations"):
            pts = []
            for r in rows:
                if param not in r:
                    continue
                pts.append((float(r[param]), float(r["final_mean"]), float(r["final_std"])))

            pts.sort(key=lambda t: t[0])
            dedup = {}
            for x, mean, std in pts:
                dedup.setdefault(x, (mean, std))
            xs = sorted(dedup.keys())
            ys = [dedup[x][0] for x in xs]
            es = [dedup[x][1] for x in xs]

            if len(xs) < 2:
                continue

            plt.figure()
            plt.plot(xs, ys, "-o")
            plt.xlabel(param)
            plt.ylabel("final_mean (across runs)")
            plt.title(f"Parameter influence | {objective_name} | mode={mode_val} | x={param}")
            plt.tight_layout()
            plt.savefig(out_dir / f"parameter_influence_{objective_name}_{mode_val}_{param}.png", dpi=150)
            plt.close()