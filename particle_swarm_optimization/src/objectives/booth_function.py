from __future__ import annotations

from dataclasses import dataclass

from src.core.types import Bounds

@dataclass(frozen=True)
class BoothFunction:
    name: str = "booth"
    bounds: Bounds = ((-10.0, 10.0), (-10.0, 10.0))

    def evaluate(self, x: float, y: float) -> float:
        t1 = x + 2.0 * y - 7.0
        t2 = 2.0 * x + y - 5.0
        return t1 * t1 + t2 * t2