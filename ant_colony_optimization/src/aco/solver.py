from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple

import time

from .problem import TSPProblem
from .ant import construct_tour, AntResult

@dataclass
class ACOConfig:
    m: int
    T: int
    alpha: float
    beta: float
    rho: float
    p_random: float
    tau0: float = 1.0
    deposit_q: float = 1.0

@dataclass
class ACOResult:
    best_tour: List[int]
    best_length: float
    best_history: List[float]
    elapsed_s: float
    iter_best: List[float]
    iter_mean: List[float]
    iter_worst: List[float]

class ACOSolver:
    def __init__(self, problem: TSPProblem, cfg: ACOConfig):
        self.problem = problem
        self.cfg = cfg
        n = problem.n
        self.pher = [[cfg.tau0] * n for _ in range(n)]
        self.best_tour: List[int] = []
        self.best_length: float = float("inf")
        self.best_history: List[float] = []

    def step(self) -> Tuple[List[AntResult], AntResult]:
        cfg = self.cfg
        p = self.problem

        ants: List[AntResult] = []
        iter_best: Optional[AntResult] = None

        for _ in range(cfg.m):
            tour = construct_tour(
                n=p.n,
                dist=p.dist,
                pher=self.pher,
                alpha=cfg.alpha,
                beta=cfg.beta,
                p_random=cfg.p_random,
            )
            length = p.tour_length(tour, close_cycle=True)
            ar = AntResult(tour=tour, length=length)
            ants.append(ar)
            if iter_best is None or ar.length < iter_best.length:
                iter_best = ar

        assert iter_best is not None

        evap = 1.0 - cfg.rho
        n = p.n
        for i in range(n):
            row = self.pher[i]
            for j in range(n):
                row[j] *= evap

        for ant in ants:
            delta = cfg.deposit_q / ant.length
            tour = ant.tour

            for k in range(len(tour) - 1):
                i, j = tour[k], tour[k + 1]
                self.pher[i][j] += delta
                self.pher[j][i] += delta

            i, j = tour[-1], tour[0]
            self.pher[i][j] += delta
            self.pher[j][i] += delta

        if iter_best.length < self.best_length:
            self.best_length = iter_best.length
            self.best_tour = list(iter_best.tour)

        self.best_history.append(self.best_length)
        return ants, iter_best

    def solve(self) -> ACOResult:
        t0 = time.perf_counter()

        iter_best: List[float] = []
        iter_mean: List[float] = []
        iter_worst: List[float] = []

        for _ in range(self.cfg.T):
            ants, _ = self.step()
            lengths = [a.length for a in ants]
            iter_best.append(min(lengths))
            iter_mean.append(sum(lengths) / len(lengths))
            iter_worst.append(max(lengths))

        elapsed = time.perf_counter() - t0

        return ACOResult(
            best_tour=self.best_tour,
            best_length=self.best_length,
            best_history=self.best_history,
            elapsed_s=elapsed,
            iter_best=iter_best,
            iter_mean=iter_mean,
            iter_worst=iter_worst,
        )