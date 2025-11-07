import pandas as pd

data_bad = pd.read_csv('problem plecakowy dane CSV tabulatory.csv', sep='\t')

print(data_bad.shape)
print(data_bad.head())
print(data_bad.tail())