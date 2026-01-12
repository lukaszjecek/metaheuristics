# Particle Swarm Optimization (PSO)

[Back to the main README](../README.md)

## What is included

An implementation of **Particle Swarm Optimization (PSO)** for **two-dimensional** objective functions.

The PSO algorithm is a population-based metaheuristic where a swarm of particles moves through the search space
to find an extremum of the objective function.

This implementation supports both **minimization** and **maximization** within predefined bounds.

Implemented objectives:

- `ackley` – [Ackley function](https://en.wikipedia.org/wiki/Ackley_function) on `x, y ∈ [-5, 5]`
- `booth` – [Booth function](https://en.wikipedia.org/wiki/File:Booth_contour.svg) on `x, y ∈ [-10, 10]`

Main components:

- **Objective definitions** (`src/objectives/`)
  - `ackley_function.py`, `booth_function.py`
- **PSO solver** (`src/core/solver.py`)
  - velocity update with inertia (`w`), cognitive (`c1`), and social (`c2`) terms
  - personal/global best updates with a numeric tolerance
  - boundary handling via clamping + reflected/damped velocity
- **Results export** (`src/results/`)
  - per-run CSV exports + JSON metadata
  - experiment aggregation (mean/median/std/best/worst)
- **Plotting utilities** (`src/plotting/`)
  - convergence plots (all runs + per-run)
  - swarm snapshots at iteration `0`, `T/2`, `T`
  - parameter influence plots from aggregated results
- **Experiment runner** (`experiment.py`)
  - full grid execution (Cartesian product) over provided parameter lists
  - `--n-runs` repetitions per configuration

## Requirements

- Python 3.x
- Libraries: `numpy`, `matplotlib`

Install from the repository root:

```bash
python -m pip install numpy matplotlib
```

## How to run

### 1) Run a single PSO execution

From the main repository directory:

```bash
cd particle_swarm_optimization

python main.py --objective ackley --mode min --n-particles 50 --n-iterations 200 --w 0.2 --c1 0.35 --c2 0.45 --output-root ./outputs --tag single_run
```

Optional reproducibility / output controls:

- `--seed <int>` – fixed seed (otherwise each run is randomized)
- `--output-root <path>` – output root directory (default: `./outputs`)
- `--tag <str>` – optional label appended to output directory names

### Parameters (single run)

- `--objective` – `{ackley, booth}` (required)
- `--mode` – `{min, max}` (default: `min`)
- `--n-particles` – `int > 0` (default: `50`)
- `--n-iterations` – `int > 0` (default: `200`)
- `--w` – inertia weight in `[0, 1]` (default: `0.2`)
- `--c1` – cognitive coefficient `>= 0` (default: `0.35`)
- `--c2` – social coefficient `>= 0` (default: `0.45`)
- `--seed` – optional master seed for reproducibility
- `--output-root` – output directory root (default: `./outputs`)
- `--tag` – optional label appended to output directory name

### Output artifacts (single run)

By default, results are saved under:

`outputs/single/<timestamp>_single_<objective>_mode<mode>_p<n>_it<T>_w<w>_c1<c1>_c2<c2>[_<tag>]/`

Saved files:

- `meta_config.json` – configuration + runtime metadata (including seed strategy and environment info)
- `raw_runs.csv` – one-row summary for the run (best value/position + elapsed time)
- `raw_history.csv` – best global value (**gbest**) per iteration
- `plots/convergence_all_runs.png` – convergence plot (all runs; for a single run this is a single curve)
- `plots/swarm_positions_0_mid_end.png` – 3-panel plot of swarm positions (iter `0`, `T/2`, `T`)

The program also prints:

- output directory
- best value and best position
- elapsed time

## Experiments (optional)

The `experiment.py` script runs a **full parameter grid** (Cartesian product of all provided lists) and repeats each configuration `--n-runs` times.

### Running an experiment series

Example:

```bash
cd particle_swarm_optimization

python experiment.py --objective all --mode min --n-runs 5 --n-particles-list 30 50 70 --n-iterations-list 75 --w-list 0.2 --c1-list 0.35 --c2-list 0.45 --output-root outputs --seed 987654321 --tag ofat_n_particles
```

### Output artifacts (experiments)

By default, results are saved under:

`outputs/experiments/<timestamp>_experiments[_<tag>]/`

1) **Per-configuration outputs** in:

`configs/<objective>_mode<mode>_p<n>_it<T>_w<w>_c1<c1>_c2<c2>/`

Inside each configuration directory:

- `meta_config.json` – config + list of run seeds
- `raw_runs.csv` – one row per run (final best + elapsed time)
- `raw_history.csv` – best global value (**gbest**) per iteration per run
- `agg_summary.csv` – aggregated statistics across runs:
  - `final_best`, `final_worst`, `final_mean`, `final_median`, `final_std`, `mean_elapsed_s`, ...
- `plots/convergence_all_runs.png` – all-runs convergence plot
- `plots/runs/run_<id>/convergence.png` – per-run convergence plot
- `plots/runs/run_<id>/swarm_positions_0_mid_end.png` – per-run swarm snapshots (0 / mid / end)

2) **Global outputs** in the experiment root directory:

- `agg_summary_all.csv` – one row per configuration (aggregated statistics)
- `plots/parameter_influence_<objective>_<mode>_<param>.png` – parameter influence plots  
  Generated only when at least **two distinct values** were tested for the given parameter.

## Implementation notes (fixed constants)

Some PSO details are fixed in the implementation (not exposed as CLI parameters):

- **Initial velocity** is `(0, 0)` for every particle.
- **Velocity clamping**: `vmax` is computed as a fraction of the search-range per axis (`vmax_fraction = 0.1`).
- **Boundary handling**: position is clamped to bounds; when a particle hits a boundary, the velocity component on that axis is reflected and damped (`k = 0.5`).
- **Comparison tolerance**: best-value comparisons use a small tolerance (`compare_tol = 1e-12`) to reduce numerical noise effects.

## Notes

- For `--mode max`, the algorithm searches for the **maximum within the predefined bounds** (not necessarily a global maximum)).
- `--n-runs` is validated to be `>= 5` in the experiment runner.
- If you omit `--seed`, runs are non-deterministic by design (each run uses an internally generated seed).