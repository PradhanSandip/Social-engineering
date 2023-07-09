
from pathlib import Path
import pandas as pd

file = pd.read_csv("./extra-data.csv")
print(file.loc[13])



