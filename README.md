# Metaheuristics

This repository contains implementations of selected metaheuristic algorithms in Python.
It is intended for experimentation, comparison of methods, and educational purposes.

## Algorithms

- **Simulated Annealing (SA)** – simulated annealing for test functions + convergence plots.  
  See: [`simulated_annealing/README.md`](simulated_annealing/README.md)

- **Genetic Algorithm (GA)** – genetic algorithm for the knapsack problem.  
  See: [`genetic_algorithm/README.md`](genetic_algorithm/README.md)

- **Ant Colony Optimization (ACO)** – ant colony optimization for the Traveling Salesman Problem (TSP)
  + experiment runner (CSV summaries, convergence plots, tour visualization).  
  See: [`ant_colony_optimization/README.md`](ant_colony_optimization/README.md)

- **Particle Swarm Optimization (PSO)** – particle swarm optimization for 2D test functions (Booth, Ackley)
  + experiment runner (CSV summaries, convergence plots, swarm snapshot plots).  
  See: [`particle_swarm_optimization/README.md`](particle_swarm_optimization/README.md)

- **Vehicle Routing Problem with Time Windows (VRPTW)** – ant colony optimization for VRPTW (with 2-opt and relocate local search operators) using Solomon benchmark instances
  + experiment runner (CSV summaries, convergence plots, route visualization).  
  See: [`vrptw/README.md`](vrptw/README.md)

## Requirements

- Python 3.x
- Libraries: `numpy`, `matplotlib`, `pandas`

Minimal dependency installation:

```bash
python -m pip install numpy matplotlib pandas
```