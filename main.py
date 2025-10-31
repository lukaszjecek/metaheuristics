import numpy as np
import random
import math
import matplotlib.pyplot as plt
import argparse
import time

# ---------- ----------
# MATEMATYCZNE FUNKCJE TESTOWE
# ---------- ----------

# Rozdział 3. – przykład 1.
def f_chapter3(x):
    if -105 < x < -95:
        return -2 * abs(x + 100) + 10
    elif 95 < x < 105:
        return -2.2 * abs(x - 100) + 11
    else:
        return 0

# Rozdział 4 – przykład 5.
def f_chapter4(x, y):
    return 21.5 + x * math.sin(4 * math.pi * x) + y * math.sin(20 * math.pi * y)

# ---------- ----------
# FUNKCJE POMOCNICZE
# ---------- ----------

def format_point(x):
    x_disp = np.round(x, 6)
    x_text = ""
    if x_disp.size == 1:
        x_text = f"x = {x_disp.item()}"
    elif x_disp.size == 2:
        x_text = f"x = {x_disp[0]}, y = {x_disp[1]}"
    return x_text

# ---------- ---------- ----------
# ALGORYTM SYMULOWANEGO WYŻARZANIA
# ---------- ---------- ----------

def simulated_annealing(func, bounds, T0, alpha, k, M, step=10):
    x = np.array([random.uniform(low, high) for low, high in bounds])
    f_current = func(*x)
    x_best = np.copy(x)
    f_best = f_current
    T = T0

    values = [f_best]
    improvements = 0

    for i in range(M):
        x_new = x + np.random.uniform(-step, step, size=len(bounds))
        x_new = np.clip(x_new, [b[0] for b in bounds], [b[1] for b in bounds])
        f_new = func(*x_new)
        delta = f_new - f_current

        # kryterium Metropolisa
        if delta > 0 or random.random() < math.exp(delta / (k * T)):
            x = x_new
            f_current = f_new
            if f_new > f_best:
                f_best = f_new
                x_best = np.copy(x)
                improvements += 1

        T *= alpha
        values.append(f_best)

    return x_best, f_best, values, improvements

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Symulowane wyżarzanie")
    parser.add_argument("--funkcja", type=int, choices=[1, 5], default=1, help="Wybór funkcji testowej: przykład 1. lub 5.")
    parser.add_argument("--T0", type=float, default=500, help="Temperatura początkowa")
    parser.add_argument("--alpha", type=float, default=0.999, help="Współczynnik chłodzenia")
    parser.add_argument("--k", type=float, default=0.1, help="Współczynnik k (skalowania temperatury)")
    parser.add_argument("--M", type=int, default=3000, help="Liczba iteracji")
    parser.add_argument("--step", type=float, default=10, help="Zakres kroku wylosowania sąsiedztwa")
    parser.add_argument("--runs", type=int, default=5, help="Liczba powtórzeń algorytmu (dla analizy stochastyczności)")
    args = parser.parse_args()

    if args.funkcja == 1:
        bounds = [(-150, 150)]
        func = f_chapter3
    else:
        bounds = [(-3, 12), (4.1, 5.8)]
        func = f_chapter4

    results = []
    start_total = time.time()

    for run in range(args.runs):
        start_single = time.time()

        x_best, f_best, values, improvements = simulated_annealing(
            func, bounds, args.T0, args.alpha, args.k, args.M, args.step
        )

        end_single = time.time()

        results.append((f_best, x_best, improvements))

        print(f"Uruchomienie nr {run + 1}: f(x) = {f_best:.6f}, {format_point(x_best)}, liczba korekcji = {improvements}, "
              f"czas (dla {args.M} iteracji) = {round(end_single - start_single, 4)} s")

    end_total = time.time()

    # Statystyka z wielu uruchomień
    f_values = [r[0] for r in results]
    best_idx = np.argmax(f_values)

    print("\n=== PODSUMOWANIE ===")
    print(f"Funkcja z przykładu {args.funkcja}.")
    print("Średnia wartość maksimum: f(x) =", round(np.mean(f_values), 6))
    print("Najlepsze maksimum: f(x) =", round(f_values[best_idx], 6), "dla punktu: ", format_point(results[best_idx][1]))
    print("Odchylenie standardowe:", round(np.std(f_values), 6))
    print("Średnia liczba korekcji:", int(np.mean([r[2] for r in results])))
    print("Liczba iteracji:", args.M)
    print("Czas całkowity:", round(end_total - start_total, 4), "s")
    print(f"Parametry: T_0 = {args.T0}, α = {args.alpha}, k = {args.k}, step = {args.step}, runs = {args.runs}")

    # Wykres z ostatniego przebiegu
    plt.plot(values)
    plt.xlabel("Iteracja")
    plt.ylabel("Wartość funkcji")
    plt.title(f"Zbieżność algorytmu SA (funkcja z przykładu {args.funkcja}) – ostatni przebieg")
    plt.grid(True)
    plt.show()