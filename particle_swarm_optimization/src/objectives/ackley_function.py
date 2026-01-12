from __future__ import annotations

import math
from dataclasses import dataclass

from src.core.types import Bounds

@dataclass(frozen=True)
class AckleyFunction:
    name: str = "ackley"
    bounds: Bounds = ((-5.0, 5.0), (-5.0, 5.0))

    def evaluate(self, x: float, y: float) -> float:
        a = 20.0
        b = 0.2
        c = 2.0 * math.pi

        d = 2.0
        sum_sq = x * x + y * y
        sum_cos = math.cos(c * x) + math.cos(c * y)

        term1 = -a * math.exp(-b * math.sqrt(sum_sq / d))
        term2 = -math.exp(sum_cos / d)
        return term1 + term2 + a + math.e