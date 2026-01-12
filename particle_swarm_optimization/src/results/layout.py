from __future__ import annotations

from pathlib import Path

from src.config import RunConfig
from src.utils.time_utils import timestamp_compact

def _safe_tag(tag: str | None) -> str:
    if not tag:
        return ""
    t = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in tag.strip())
    return f"_{t}" if t else ""

def make_single_run_output_dir(run_cfg: RunConfig) -> Path:
    ts = timestamp_compact()
    tag = _safe_tag(run_cfg.tag)
    p = run_cfg.pso
    name = (
        f"{ts}_single_{run_cfg.objective_name}_mode{run_cfg.mode}"
        f"_p{p.n_particles}_it{p.n_iterations}_w{p.w}_c1{p.c1}_c2{p.c2}{tag}"
    )
    return run_cfg.output_root / "single" / name

def make_experiment_output_dir(output_root: Path, tag: str | None) -> Path:
    ts = timestamp_compact()
    tag_s = _safe_tag(tag)
    return output_root / "experiments" / f"{ts}_experiments{tag_s}"

def make_config_dir_name(
    objective_name: str,
    mode: str,
    n_particles: int,
    n_iterations: int,
    w: float,
    c1: float,
    c2: float,
) -> str:
    return (
        f"{objective_name}_mode{mode}"
        f"_p{n_particles}_it{n_iterations}"
        f"_w{w}_c1{c1}_c2{c2}"
    )