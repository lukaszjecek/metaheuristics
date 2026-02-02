# Vehicle Routing Problem with Time Windows (VRPTW)

[Back to the main README](../README.md)

## What is included

An implementation of **Ant Colony Optimization (ACO)** for the **Vehicle Routing Problem with Time Windows (VRPTW)**.

The goal is to minimize the number of vehicles first, then minimize the total travel distance while respecting:
- **Time windows** – each customer must be visited within their specified time window
- **Vehicle capacity** – total demand on each route cannot exceed vehicle capacity

Main components:

- **Data loading** (`src/aco/io.py`)
  - reads [Solomon benchmark instances](https://www.sintef.no/projectweb/top/vrptw/100-customers/) (VRPTW standard format)
  - parses customer locations, demands, time windows, and service times
- **VRPTW problem model** (`src/aco/problem.py`)
  - builds distance matrix (Euclidean distance)
  - evaluates solutions (number of vehicles, total distance, constraint violations)
  - scoring uses lexicographic ordering: minimize vehicles, then minimize penalized distance
- **ACO solver** (`src/aco/solver.py`)
  - constructs feasible routes using **roulette-wheel selection** based on pheromone and distance heuristic
  - **local search** applied to improve solutions:
    - **2-opt** – edge-swap optimization within routes
    - **relocate** – removes one route and attempts to insert its customers into remaining routes
  - **pheromone evaporation** controlled by `rho`
  - **pheromone deposit** proportional to solution quality (fewer vehicles and shorter distance = more pheromone)
  - `p_random` is the probability of choosing the next customer **uniformly at random** (ignoring pheromones/heuristic)
  - `alpha` controls pheromone influence, `beta` controls distance heuristic influence
- **Plotting utilities** (`src/aco/plotting.py`)
  - best solution visualization (PNG) showing routes and depot
  - convergence plots (PNG)
- **Experiment runner** (`src/experiment/run_experiments.py`)
  - multiple repetitions per configuration
  - exports CSV summaries and plots per configuration
  - generates a global `summary.csv` with aggregated statistics

## Requirements

- Python 3.x
- `matplotlib`

Install from the repository root:

```bash
python -m pip install matplotlib
```

## How to run

### 1) Run a single ACO execution

From the main repository directory:

```bash
cd vrptw
python -m src.main --instance "data/solomon-100/In/c204.txt" --out_dir "results/demo_c204" --seed 123123123 --m 80 --T 300 --alpha 1.0 --beta 5.0 --rho 0.5 --p_random 0.001
```

### Parameters (single run)

- `--instance` – path to Solomon instance file
- `--out_dir` – output directory for CSV + PNG artifacts
- `--seed` – random seed for reproducibility
- `--m` – number of ants per iteration
- `--T` – number of iterations
- `--alpha` – pheromone influence
- `--beta` – heuristic influence (distance)
- `--rho` – evaporation rate
- `--p_random` – probability of taking a random next step

### Output artifacts (single run)

Saved under `--out_dir`:

- `best_solution.csv` – best solution details (vehicles, distance, routes)
- `convergence.csv` – best cost per iteration
- `best_solution.png` – plot of the best solution (routes visualization)
- `convergence.png` – convergence plot
- `run_summary.csv` – one-row summary for the run

The program also prints:
- best number of vehicles
- best total distance
- time window and capacity violations
- elapsed time

## Experiments (optional)

The `src/experiment/run_experiments.py` script runs multiple configurations (lists of parameter values) and repeats each configuration several times.

### Running an experiment series

```bash
cd vrptw
python -m src.experiment.run_experiments --instances c204.txt --in_dir data/solomon-100/In --out_dir results/experiments_c204_m --repeats 5 --base_seed 987654321 --m_list 75 100 125 --T_list 500 750 --alpha_list 2.0 3.0 --beta_list 5.0 7.0 --rho_list 0.5 0.7 --p_random_list 0.0 0.001
```

1) **Per-instance directory** named like the instance (e.g., `c204/`)

Inside each instance directory:

- **Per-configuration subdirectory** named like:
  `m{m}_T{T}_a{alpha}_b{beta}_rho{rho}_pr{p_random}`

  Inside each configuration directory:
  - `runs.csv` – per-run results (vehicles, distance, time)
  - `history.csv` – best cost per iteration for each run
  - `population_history.csv` – per-iteration best/mean/worst across runs
  - `selected_runs.csv` – detailed info for best/median/worst runs
  - `best_solution_overall.csv` – best solution among all repeats
  - `solution_best_overall.png` – best overall solution plot
  - `solution_best.png` – best solution from the best run
  - `solution_median.png` – best solution from the median run
  - `solution_worst.png` – best solution from the worst run
  - `convergence_mean_minmax.png` – mean convergence with min–max band

2) **Global summary** in the instance directory:
- `summary.csv` – one row per configuration with aggregated statistics (min/mean/median/std/max for cost, distance, vehicles)

3) **Global comparison plots** in the instance directory (if parameter has more than one value):
- `compare_m.png`, `compare_T.png`, `compare_alpha.png`, etc.

## Notes

- Solutions are evaluated using **lexicographic ordering**: first minimize the number of vehicles, then minimize total distance
- **Current implementation**: Ants construct only **feasible routes** (respecting time windows and capacity constraints during construction)
- The code already includes constraint violation evaluation mechanisms and is ready for refactoring toward a **penalty-based approach** if needed
- **Local search operators**:
  - **2-opt**: Improves route quality by swapping edges within a single route
  - **Relocate**: Attempts to reduce the number of vehicles by dismantling one route and inserting its customers into other routes
- The Solomon benchmark instances are widely used for VRPTW testing and are available in `data/solomon-100/In/`