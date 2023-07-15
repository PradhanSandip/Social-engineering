from parse_json import read_json
import pandas as pd
from pathlib import Path

data = read_json("ignore_missing.json")

celeb_data = read_json("celeb-data.json")
missing = data["missing"]

path = "english_only"
eng_files = []
for file_ in Path(path).rglob("*.csv"):
    eng_files.append(file_.name[:-4])


c = 0
l = []
for key in celeb_data.keys():
    if(key in eng_files):
        c += 1
        l.append(key)

print(l)
print(c)
print(len(list(Path(path).rglob("*.csv"))))
    