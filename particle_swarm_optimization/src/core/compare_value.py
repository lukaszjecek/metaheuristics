from __future__ import annotations

from src.core.types import Mode

def is_strictly_better(new: float, old: float, mode: Mode, tol: float) -> bool:
    if mode == "min":
        return new < old - tol
    return new > old + tol