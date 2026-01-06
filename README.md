# Metaheuristics

This repository contains implementations of selected metaheuristic algorithms in Python.
It is intended for experimentation, comparison of methods, and educational purposes.

Some algorithms are still under development.

## Algorithms

- **Simulated Annealing (SA)** – simulated annealing for test functions + convergence plots.  
  See: [`simulated_annealing/README.md`](simulated_annealing/README.md)

- **Genetic Algorithm (GA)** – genetic algorithm for the knapsack problem.  
  See: [`genetic_algorithm/README.md`](genetic_algorithm/README.md)

- **Ant Colony Optimization (ACO)** – ant colony optimization for the Traveling Salesman Problem (TSP)
  + experiment runner (CSV summaries, convergence plots, tour visualization).  
  See: [`ant_colony_optimization/README.md`](ant_colony_optimization/README.md)

### Work in progress / planned

- **Particle Swarm Optimization (PSO)** – planned
- **Vehicle Routing Problem with Time Windows (VRPTW)**  
  To be solved using a selected metaheuristic (to be determined)

## Requirements

- Python 3.x
- Libraries: `numpy`, `matplotlib`, `pandas`

Minimal dependency installation:

```bash
python -m pip install numpy matplotlib pandas
```
