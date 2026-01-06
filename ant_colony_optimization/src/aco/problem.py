from __future__ import annotations
from dataclasses import dataclass
from typing import List

import math

from .io import Node

@dataclass(frozen=True)
class TSPProblem:
    nodes: List[Node]
    dist: List[List[float]]

    @property
    def n(self) -> int:
        return len(self.nodes)

    def tour_length(self, tour: List[int], close_cycle: bool = True) -> float:
        total = 0.0
        for i in range(1, len(tour)):
            total += self.dist[tour[i - 1]][tour[i]]
        if close_cycle and len(tour) > 1:
            total += self.dist[tour[-1]][tour[0]]
        return total

def build_problem(nodes: List[Node]) -> TSPProblem:
    n = len(nodes)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = nodes[i].x, nodes[i].y
        for j in range(i + 1, n):
            xj, yj = nodes[j].x, nodes[j].y
            d = math.hypot(xi - xj, yi - yj)
            dist[i][j] = d
            dist[j][i] = d
    return TSPProblem(nodes=nodes, dist=dist)