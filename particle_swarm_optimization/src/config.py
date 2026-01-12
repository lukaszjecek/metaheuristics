from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Tuple

Mode = Literal["min", "max"]
Bounds = Tuple[Tuple[float, float], Tuple[float, float]]

@dataclass(frozen=True)
class PSOConfig:
    n_particles: int
    n_iterations: int
    w: float
    c1: float
    c2: float
    mode: Mode
    vmax_fraction: float = 0.1
    eps: float = 1e-9
    boundary_reflect_damping_k: float = 0.5
    compare_tol: float = 1e-12

    def validate(self) -> None:
        if self.n_particles <= 0:
            raise ValueError("n_particles must be > 0")
        if self.n_iterations <= 0:
            raise ValueError("n_iterations must be > 0")
        if not (0.0 <= self.w <= 1.0):
            raise ValueError("w should be in [0, 1]")
        if self.c1 < 0 or self.c2 < 0:
            raise ValueError("c1 and c2 must be >= 0")
        if self.vmax_fraction <= 0:
            raise ValueError("vmax_fraction must be > 0")
        if self.eps <= 0:
            raise ValueError("eps must be > 0")
        if not (0.0 < self.boundary_reflect_damping_k <= 1.0):
            raise ValueError("boundary_reflect_damping_k must be in (0, 1].")

@dataclass(frozen=True)
class RunConfig:
    objective_name: str
    bounds: Bounds
    mode: Mode
    pso: PSOConfig
    seed: int | None
    output_root: Path
    tag: str | None = None