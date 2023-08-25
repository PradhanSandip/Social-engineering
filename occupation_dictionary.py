from parse_json import update_json
from pathlib import Path
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords

save_location = "occupation_dictionary.json"
information_location = "professions_information"

files  = Path(information_location).rglob("*.txt")
dictionary = {}
for file in files:
    name = file.name[:-4]
    dictionary[name] = []
    with open(file,encoding='utf-8') as f:
        for line in f.readlines():
            line = word_tokenize(line.strip())
            line = [word for word in line if word.lower() not in stopwords.words("english") and len(word) > 2]
            for l in line:
                if l.lower() not in dictionary[name]:
                    dictionary[name].append(l.lower())
    print(dictionary)
    update_json(save_location,dictionary)
