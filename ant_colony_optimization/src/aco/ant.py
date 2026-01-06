from __future__ import annotations
from dataclasses import dataclass
from typing import List, Sequence

import random

@dataclass
class AntResult:
    tour: List[int]
    length: float

def _roulette_choice(items: Sequence[int], weights: Sequence[float]) -> int:
    total = 0.0
    for w in weights:
        total += w
    if total <= 0.0:
        return random.choice(list(items))
    r = random.random() * total
    acc = 0.0
    for item, w in zip(items, weights):
        acc += w
        if r <= acc:
            return item
    return items[-1]

def construct_tour(
    n: int,
    dist: List[List[float]],
    pher: List[List[float]],
    alpha: float,
    beta: float,
    p_random: float,
) -> List[int]:
    start = random.randrange(n)
    tour = [start]
    visited = [False] * n
    visited[start] = True

    while len(tour) < n:
        i = tour[-1]
        candidates = [j for j in range(n) if not visited[j]]

        if p_random > 0.0 and random.random() < p_random:
            nxt = random.choice(candidates)
            tour.append(nxt)
            visited[nxt] = True
            continue

        weights: List[float] = []
        for j in candidates:
            d = dist[i][j]
            inv_d = 1.0 / d if d > 0.0 else 1e9
            w = (pher[i][j] ** alpha) * (inv_d ** beta)
            weights.append(w)

        nxt = _roulette_choice(candidates, weights)
        tour.append(nxt)
        visited[nxt] = True

    return tour