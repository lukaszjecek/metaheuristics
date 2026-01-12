from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Tuple, Literal

Mode = Literal["min", "max"]
Bounds = Tuple[Tuple[float, float], Tuple[float, float]]

class Objective2D(Protocol):
    name: str
    bounds: Bounds

    def evaluate(self, x: float, y: float) -> float: ...

@dataclass(frozen=True)
class VMax:
    vmax_x: float
    vmax_y: float