from __future__ import annotations

from typing import Tuple

import numpy as np

from src.core.types import Bounds, VMax

def compute_vmax(bounds: Bounds, fraction: float, eps: float) -> VMax:
    (xmin, xmax), (ymin, ymax) = bounds
    rx = float(xmax - xmin)
    ry = float(ymax - ymin)
    vmax_x = max(abs(fraction * rx), eps)
    vmax_y = max(abs(fraction * ry), eps)
    return VMax(vmax_x=vmax_x, vmax_y=vmax_y)

def clamp_with_reflect_damping(
    pos: np.ndarray,
    vel: np.ndarray,
    lo: float,
    hi: float,
    k: float,
) -> Tuple[np.ndarray, np.ndarray]:
    below = pos < lo
    above = pos > hi

    pos = np.where(below, lo, pos)
    pos = np.where(above, hi, pos)

    hit = below | above
    vel = np.where(hit, -k * vel, vel)
    return pos, vel


def make_meshgrid_on_bounds(bounds: Bounds, grid_size: int) -> tuple[np.ndarray, np.ndarray]:
    (xmin, xmax), (ymin, ymax) = bounds
    xs = np.linspace(xmin, xmax, grid_size)
    ys = np.linspace(ymin, ymax, grid_size)
    X, Y = np.meshgrid(xs, ys)
    return X, Y