# Simulated Annealing (SA)

[Back to the main README](../README.md)

## What is included

An implementation of the **Simulated Annealing** (SA) algorithm in Python.

The SA algorithm is a metaheuristic used to approximately find the global extremum of a function, especially when many local extrema exist. In each iteration, a random neighbor of the current solution is generated and (with a certain probability dependent on the temperature) a worse solution may also be accepted — which helps to “escape” from local extrema.

In this implementation, SA is used to **find the global extremum** of two test functions:

- `--function 1` – a one-dimensional function (example 1 from [the article by Stanisław Kowalik](https://www.researchgate.net/publication/305489442))
- `--function 5` – a two-dimensional function (example 5 from [the article by Stanisław Kowalik](https://www.researchgate.net/publication/305489442))

The program prints results to the console and plots convergence graphs (Matplotlib).

## How to run

### 1) Install dependencies

From the main repository directory:

```bash
python -m pip install numpy matplotlib
```

### 2) Run the program

Go to the implementation directory and run `main.py` with parameters.

Example for the one-dimensional function:

```bash
cd simulated_annealing
python main.py --function 1 --T0 500 --alpha 0.999 --k 0.1 --M 3000 --step 10.0 --runs 5
```

Example for the two-dimensional function:

```bash
cd simulated_annealing
python main.py --function 5 --T0 100 --alpha 0.999 --k 0.2 --M 7000 --step 1.0 --runs 5
```

### Parameters

- `--function` – `1` or `5` (test function selection)
- `--T0` – positive real number (initial temperature)
- `--alpha` – value in the range `(0, 1]` (cooling coefficient)
- `--k` – positive real number (temperature scaling in the Metropolis criterion)
- `--M` – positive integer (maximum number of iterations)
- `--step` – positive real number (range for generating neighboring solutions)
- `--runs` – positive integer (number of independent runs)

After completion, the program outputs statistics (including mean, best result, and standard deviation) and displays plots.