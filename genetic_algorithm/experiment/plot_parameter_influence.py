import argparse
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

PARAM_PATTERN = re.compile(
    r"pc(?P<Pc>[\d\.]+)_pm(?P<Pm>[\d\.]+)_n(?P<N>[\d\.]+)_t(?P<T>[\d\.]+)_"
    r"(?P<selection>roulette|ranking|tournament)_"
    r"(?P<crossover>one_point|two_point|uniform)_"
    r"(?P<mutation>.+)\.csv"
)

def parse_filename(filename):
    m = PARAM_PATTERN.match(filename)
    return m.groupdict() if m else None

def load_all_results(src_dir):
    results = []

    for file in os.listdir(src_dir):
        if not file.endswith(".csv"):
            continue

        parsed = parse_filename(file)
        if parsed is None:
            continue

        df = pd.read_csv(os.path.join(src_dir, file))

        for _, row in df.iterrows():
            results.append({
                "Pc": float(parsed["Pc"]),
                "Pm": float(parsed["Pm"]),
                "N": int(float(parsed["N"])),
                "T": int(float(parsed["T"])),
                "selection_method": parsed["selection"],
                "crossover_method": parsed["crossover"],
                "mutation_method": parsed["mutation"],
                "best_value": row["best_value"],
            })

    return pd.DataFrame(results)

def plot_parameter_influence(df, param, outdir):
    if param not in df.columns:
        print(f"Parametr {param} nie istnieje w danych.")
        return

    grouped = df.groupby(param)["best_value"]

    means = grouped.mean()
    medians = grouped.median()
    mins = grouped.min()
    maxs = grouped.max()
    stds = grouped.std()

    stat_df = pd.DataFrame({
        "mean": means,
        "median": medians,
        "min": mins,
        "max": maxs,
        "std": stds
    })

    stats_path = os.path.join(outdir, f"influence_{param}_stats.txt")
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write(f"Statystyki dla parametru: {param}\n")
        f.write("=" * 60 + "\n\n")

        def fmt(x):
            if pd.isna(x):
                return ""
            return f"{x:,.1f}".replace(",", " ")

        f.write(f"{param:<15} {'mean':>15} {'median':>15} {'min':>15} {'max':>15} {'std':>15}\n")
        f.write("-" * 90 + "\n")

        for value in stat_df.index:
            f.write(
                f"{str(value):<15} "
                f"{fmt(stat_df.loc[value, 'mean']):>15} "
                f"{fmt(stat_df.loc[value, 'median']):>15} "
                f"{fmt(stat_df.loc[value, 'min']):>15} "
                f"{fmt(stat_df.loc[value, 'max']):>15} "
                f"{fmt(stat_df.loc[value, 'std']):>15}\n"
            )

    print(f"\nZapisano statystyki do: {stats_path}")

    plt.figure(figsize=(10, 6))
    means.plot(marker="o")
    plt.xlabel(param)
    plt.ylabel("Średnia best_value")
    plt.title(f"Wpływ parametru {param} na jakość rozwiązania")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"influence_{param}_mean.png"))
    plt.close()

    print(f"Zapisano wykres: influence_{param}_mean.png")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--param", required=True,
                        help="Parametr do analizy: Pc, Pm, N, T, selection_method, crossover_method, mutation_method")
    parser.add_argument("--src_dir", required=True,
                        help="Folder z plikami CSV (np. influ_Pc)")
    args = parser.parse_args()

    print(f"Wczytywanie plików CSV z folderu: {args.src_dir}")
    df = load_all_results(args.src_dir)

    if df.empty:
        print("Brak plików CSV pasujących do wzorca w podanym folderze.")
        return

    plot_parameter_influence(df, args.param, args.src_dir)

if __name__ == "__main__":
    main()