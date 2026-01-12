from __future__ import annotations

from typing import Dict

from src.objectives.ackley_function import AckleyFunction
from src.objectives.booth_function import BoothFunction
from src.core.types import Objective2D

_REGISTRY: Dict[str, Objective2D] = {
    "ackley": AckleyFunction(),
    "booth": BoothFunction(),
}

def list_objectives() -> list[str]:
    return sorted(_REGISTRY.keys())

def get_objective(name: str) -> Objective2D:
    key = name.strip().lower()
    if key not in _REGISTRY:
        raise KeyError(f"Unknown objective: {name}. Available: {list_objectives()}")
    return _REGISTRY[key]