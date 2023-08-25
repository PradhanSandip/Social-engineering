import wikipediaapi
import os
from nltk import pos_tag, word_tokenize
from parse_json import update_json

save = "occupation_dictionary.json"
#wikipedia api
# wiki = wikipediaapi.Wikipedia(f'CelebInfo/0 {os.environ.get("contact")}', "en")

# with open("Professions.txt") as profession:
#     lines = profession.readlines()
#     for line in lines:
#         dictionary = []
        
#         if(not line.startswith("#") and not line.startswith("\n")):
#             result = wiki.page(line.strip())
#             summary = result.summary
            
#             words = word_tokenize(summary)
            
#             for word in words:
#                 print(pos_tag([word]))
#                 if(pos_tag([word])[0][1] == "NN" or pos_tag([word])[0][1] == "NNS"):
#                     if(word.encode().decode() not in dictionary):
#                         dictionary.append(word.encode().decode().lower())
        
#             update_json(save, {line.strip():dictionary})

