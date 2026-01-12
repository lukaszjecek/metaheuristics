from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.core.particle import Particle
from src.core.position import Position

@dataclass
class Swarm:
    particles: List[Particle]
    gbest_pos: Position
    gbest_val: float