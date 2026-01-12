from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np

from src.config import PSOConfig
from src.core.types import Bounds, Mode

@dataclass
class RunResult:
    run_id: int
    seed: int | None
    elapsed_s: float

    final_gbest_val: float
    final_gbest_x: float
    final_gbest_y: float

    history: List[Tuple[int, float]]

    snapshots: Dict[int, np.ndarray] = field(default_factory=dict)

    pso_config: PSOConfig | None = None
    objective_name: str | None = None
    bounds: Bounds | None = None
    mode: Mode | None = None