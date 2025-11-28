import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--Pc', type=float, default=0.6, help="Prawdopodobieństwo krzyżowania")
    parser.add_argument('--Pm', type=float, default=0.05, help="Prawdopodobieństwo mutacji")
    parser.add_argument('--N', type=int, default=30, help="Wielkość populacji")
    parser.add_argument('--T', type=int, default=300, help="Liczba iteracji")
    parser.add_argument('--selection_method', type=str, choices=["roulette", "ranking", "tournament"],
                        help="Metoda selekcji nowego rodzica")
    parser.add_argument('--crossover_method', type=str, choices=["one_point", "two_point", "uniform"],
                        help="Metoda krzyżowania w procesie tworzenia potomstwa")
    parser.add_argument('--mutation_method', type=str, choices=["single_bit_flip", "all_bit_inversion"],
                        default="single_bit_flip", help="Metoda mutacji genów w chromosomie")
    parser.add_argument('--data_file', type=str, default="problem plecakowy dane CSV tabulatory.csv",
                        help="Plik csv z dostępnymi do włożenia do plecaka przedmiotami")

    args = parser.parse_args()

    if args.Pc < 0 or args.Pc > 1.0:
        parser.error("Prawdopodobieństwo krzyżowaniu musi być w zakresie [0, 1].")

    if args.Pm < 0 or args.Pm > 1.0:
        parser.error("Prawdopodobieństwo mutacji musi być w zakresie [0, 1].")

    if args.N <= 0:
        parser.error("Wielkość populacji musi być większa od 0.")

    if args.T <= 0:
        parser.error("Liczba iteracji musi być większa od 0.")

    return args