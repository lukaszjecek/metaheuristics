# Genetic Algorithm (GA)

[Back to the main README](../README.md)

## What is included

An implementation of the **Genetic Algorithm** (GA) for the **knapsack problem**.

Key assumptions:

- A solution is encoded as a **binary chromosome** (0/1) of length `n = 26`.
- *1* means that an item is selected for the knapsack, *0* means it is omitted.
- **Fitness** = sum of the values of selected items.
- If the total weight exceeds the maximum capacity (**6,404,180 kg**), fitness = `0`.

Supported operators:

- Selection: `roulette`, `ranking`, `tournament`
- Crossover: `one_point`, `two_point`, `uniform`
- Mutation: `single_bit_flip`, `all_bit_inversion`

Input problem data is provided in a CSV file (tab-separated) located in `data/`.

## How to run

### 1) Install dependencies

From the main repository directory:

```bash
python -m pip install pandas
```

If you want to run the experiment module (plots), also install Matplotlib:

```bash
python -m pip install matplotlib
```

### 2) Run a single GA execution

```bash
cd genetic_algorithm
python main.py \
  --Pc 0.6 --Pm 0.01 --N 50 --T 700 \
  --selection_method roulette \
  --crossover_method two_point \
  --mutation_method single_bit_flip \
  --data_file "data/problem plecakowy dane CSV tabulatory.csv"
```

Parameters:

- `--Pc`, `--Pm` – `float` in the range `[0, 1]`
- `--N`, `--T` – `int` > 0
- `--selection_method` – `{roulette, ranking, tournament}`
- `--crossover_method` – `{one_point, two_point, uniform}`
- `--mutation_method` – `{single_bit_flip, all_bit_inversion}`
- `--data_file` – path to the data file (note: the filename contains spaces, so use quotes)

The program prints the best knapsack value and the corresponding chromosome to the console.

## Experiments (optional)

The `experiment/` directory contains scripts for running series of experiments and analyzing parameter influence.

### Running an experiment (saving results + plots)

The following command runs **5 GA executions** for the given parameters and saves:

- progress plots (PNG)
- a summary CSV file with results

Results are saved to: `genetic_algorithm/results/<parameter_based_name>/`.

```bash
cd genetic_algorithm
python -m experiment.experiment \
  --Pc 0.6 --Pm 0.01 --N 50 --T 700 \
  --selection_method roulette \
  --crossover_method two_point \
  --mutation_method single_bit_flip \
  --data_file "data/problem plecakowy dane CSV tabulatory.csv"
```

### Reproducing experiment series (parameter grid)

An example Git Bash variant:

```bash
cd genetic_algorithm

BASE="--T 700 --selection_method roulette --crossover_method two_point --mutation_method single_bit_flip"
DATA="data/problem plecakowy dane CSV tabulatory.csv"

for Pc in 0.6 0.8 1.0; do
  for Pm in 0.01 0.05 0.10; do
    for N in 50 150 300; do
      python -m experiment.experiment --Pc "$Pc" --Pm "$Pm" --N "$N" $BASE --data_file "$DATA"
    done
  done
done
```

### Parameter influence analysis (plots / statistics)

The `experiment.plot_parameter_influence` script reads CSV files from a single directory and generates:

- `influence_<param>_mean.png` (mean value plot)
- `influence_<param>_stats.txt` (statistics)

Typical workflow:

1. Run a series of experiments to generate CSV files in `results/`.
2. Copy/Move selected CSV files to:
   - `experiment/influ_Pc/` (Pc comparison)
   - `experiment/influ_Pm/` (Pm comparison)
   - `experiment/influ_N/` (N comparison)
   - (analogously) `experiment/influ_selection/`, `experiment/influ_cross/`
3. Run the analysis:

```bash
cd genetic_algorithm
python -m experiment.plot_parameter_influence --param Pc --src_dir experiment/influ_Pc
python -m experiment.plot_parameter_influence --param Pm --src_dir experiment/influ_Pm
python -m experiment.plot_parameter_influence --param N  --src_dir experiment/influ_N
```

### Influence of the selection method

1. Based on results from `influ_Pc/`, `influ_Pm/`, `influ_N/`, choose the best `Pc`, `Pm`, and `N`.
2. Run experiments for the three selection methods, setting `T=699` (to avoid overwriting results from `T=700`).
3. Copy generated CSV files (from `results/...`) to `experiment/influ_selection/`.
4. Generate plots/statistics:

```bash
cd genetic_algorithm

BASE_SEL="--Pc 1.0 --Pm 0.10 --N 300 --T 699 --crossover_method two_point --mutation_method single_bit_flip"
DATA="data/problem plecakowy dane CSV tabulatory.csv"

python -m experiment.experiment $BASE_SEL --selection_method roulette  --data_file "$DATA"
python -m experiment.experiment $BASE_SEL --selection_method ranking   --data_file "$DATA"
python -m experiment.experiment $BASE_SEL --selection_method tournament --data_file "$DATA"

python -m experiment.plot_parameter_influence --param selection_method --src_dir experiment/influ_selection
```

### Influence of the crossover method

1. Determine the best `Pc`, `Pm`, and `N`.
2. Run experiments for the three crossover methods, setting `T=701` (to avoid overwriting results).
3. Copy CSV files to `experiment/influ_cross/`.
4. Generate plots/statistics:

```bash
cd genetic_algorithm

BASE_CROSS="--Pc 1.0 --Pm 0.10 --N 300 --T 701 --selection_method roulette --mutation_method single_bit_flip"
DATA="data/problem plecakowy dane CSV tabulatory.csv"

python -m experiment.experiment $BASE_CROSS --crossover_method one_point --data_file "$DATA"
python -m experiment.experiment $BASE_CROSS --crossover_method two_point --data_file "$DATA"
python -m experiment.experiment $BASE_CROSS --crossover_method uniform  --data_file "$DATA"

python -m experiment.plot_parameter_influence --param crossover_method --src_dir experiment/influ_cross
```