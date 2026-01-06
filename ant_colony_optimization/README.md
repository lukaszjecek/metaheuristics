# Ant Colony Optimization (ACO)

[Back to the main README](../README.md)

## What is included

An implementation of **Ant Colony Optimization (ACO)** for the **Traveling Salesman Problem (TSP)**.

Main components:

- **Data loading** (`src/aco/io.py`)
  - reads nodes from a text file (one node per line: `label x y`)
  - stores nodes as immutable `Node` records
- **TSP problem model** (`src/aco/problem.py`)
  - builds a full distance matrix (Euclidean distance)
  - computes tour length (optionally closing the cycle)
- **ACO solver** (`src/aco/solver.py`)
  - constructs tours using **roulette-wheel selection** based on pheromone level and a distance-based heuristic (shorter edges are preferred)
  - **pheromone evaporation** is controlled by `rho`
  - **each ant deposits pheromones** on the edges of its tour; the deposited amount is proportional to the tour quality (shorter tours deposit more)
  - `p_random` is the probability of **ignoring roulette selection** and choosing the next city **uniformly at random** (i.e., without using pheromones or the heuristic)
- **Plotting utilities** (`src/aco/plotting.py`)
  - best tour visualization (PNG)
  - convergence plots (PNG)
- **Experiment runner** (`src/experiment/run_experiments.py`)
  - multiple repetitions per configuration
  - exports CSV summaries and plots per configuration
  - generates a global `summary.csv` and parameter comparison plots

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
cd ant_colony_optimization
python -m src.main \
  --data_file data/A-n32-k5.txt \
  --out_dir results/demo \
  --m 20 --T 100 \
  --alpha 1.0 --beta 5.0 \
  --rho 0.3 --p_random 0.01
```

### Parameters (single run)

- `--data_file` – path to input data (`label x y` per line)
- `--out_dir` – output directory for CSV + PNG artifacts
- `--m` – number of ants per iteration
- `--T` – number of iterations
- `--alpha` – pheromone influence
- `--beta` – heuristic influence
- `--rho` – evaporation rate
- `--p_random` – probability of taking a random next step

### Output artifacts (single run)

Saved under `--out_dir`:

- `best_tour.csv` – best tour (labels) and its length
- `convergence.csv` – best length per iteration
- `best_tour.png` – plot of the best tour
- `convergence.png` – convergence plot
- `run_summary.csv` – one-row summary for the run

The program also prints:
- best length
- elapsed time
- best tour labels

## Experiments (optional)

The `src/experiment/run_experiments.py` script runs multiple configurations (lists of parameter values) and repeats each configuration several times.

### Running an experiment series

Example:

```bash
cd ant_colony_optimization
python -m src.experiment.run_experiments \
  --data_file data/A-n32-k5.txt \
  --out_dir results/experiments/A-n32-k5 \
  --repeats 5 \
  --m_list 10 20 50 \
  --T_list 50 100 \
  --alpha_list 1.0 \
  --beta_list 2.0 5.0 10.0 \
  --rho_list 0.1 0.3 \
  --p_random_list 0.0 0.01 0.05
```

### Output artifacts (experiments)

Under `--out_dir`:

1) **Per-configuration directory** named like:
`m{m}_T{T}_a{alpha}_b{beta}_rho{rho}_pr{p_random}`

Inside each configuration directory:
- `runs.csv` – per-run best length and time
- `history.csv` – best length per iteration for each run
- `population_history.csv` – per-iteration best/mean/worst (per run)
- `best_tour_run_<r>.csv` – best tour for run `r`
- `best_tour_overall.csv` – best tour among all repeats
- `best_tour.png` – best overall tour plot
- `convergence_mean_minmax.png` – mean convergence with min–max band

2) **Global outputs** in the experiment root directory:
- `summary.csv` – one row per configuration with aggregated statistics
- `compare_m.png`, `compare_T.png`, ... – parameter comparison plots
  (generated only if the parameter has more than one tested value)