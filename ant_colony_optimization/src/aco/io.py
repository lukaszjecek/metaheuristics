from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass(frozen=True)
class Node:
    idx: int
    label: int
    x: float
    y: float

def load_nodes(path: str | Path) -> List[Node]:
    path = Path(path)
    nodes: List[Node] = []
    with path.open("r", encoding="utf-8") as f:
        for internal_idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"Zły format linii: {line}")
            label = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            nodes.append(Node(idx=internal_idx, label=label, x=x, y=y))
    return nodes