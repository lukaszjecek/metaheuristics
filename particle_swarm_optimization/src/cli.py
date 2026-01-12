from __future__ import annotations

import argparse

def build_main_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="main.py",
    )

    p.add_argument("--objective", choices=["ackley", "booth"], required=True)
    p.add_argument("--mode", choices=["min", "max"], default="min")

    p.add_argument("--n-particles", type=int, default=50, dest="n_particles")
    p.add_argument("--n-iterations", type=int, default=200, dest="n_iterations")
    p.add_argument("--w", type=float, default=0.2)
    p.add_argument("--c1", type=float, default=0.35)
    p.add_argument("--c2", type=float, default=0.45)

    p.add_argument("--seed", type=int, default=None, help="Optional master seed for reproducibility.")
    p.add_argument("--output-root", type=str, default=None, help="Default: ./outputs")
    p.add_argument("--tag", type=str, default=None, help="Optional label appended to output directory name.")

    return p

def build_experiment_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="experiment.py",
    )

    p.add_argument("--objective", choices=["ackley", "booth", "all"], required=True)
    p.add_argument("--mode", choices=["min", "max"], default="min")

    p.add_argument(
        "--n-runs",
        type=int,
        default=5,
        dest="n_runs",
        help="Number of runs per configuration (>=5).",
    )

    p.add_argument(
        "--n-particles-list",
        type=int,
        nargs="+",
        required=True,
        help="List of particle counts.",
    )
    p.add_argument(
        "--n-iterations-list",
        type=int,
        nargs="+",
        required=True,
        help="List of iteration counts.",
    )
    p.add_argument(
        "--w-list",
        type=float,
        nargs="+",
        required=True,
        help="List of inertia weights w.",
    )
    p.add_argument(
        "--c1-list",
        type=float,
        nargs="+",
        required=True,
        help="List of cognitive coefficients c1.",
    )
    p.add_argument(
        "--c2-list",
        type=float,
        nargs="+",
        required=True,
        help="List of social coefficients c2.",
    )

    p.add_argument("--seed", type=int, default=None, help="Optional master seed (applies to all runs).")
    p.add_argument("--output-root", type=str, default=None, help="Default: ./outputs")
    p.add_argument("--tag", type=str, default=None, help="Optional label appended to output directory name.")

    return p