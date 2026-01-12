from __future__ import annotations

from dataclasses import dataclass

from src.core.position import Position
from src.core.velocity import Velocity

@dataclass
class Particle:
    pos: Position
    vel: Velocity
    pbest_pos: Position
    pbest_val: float