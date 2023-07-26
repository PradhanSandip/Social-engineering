import pandas as pd
import re
from parse_json import read_json, update_json
import requests
import wikipediaapi
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import time
from generate_profile_wikipedia import remove_emojis

twitter_profile = pd.read_csv("extra-data.csv", sep=":::", engine="python",index_col=False)
wiki_data = read_json("celeb-data.json")
data = read_json("celeb-data.json")
stopwords = list(stopwords.words('english'))

#add additional stopwords source: https://www.kaggle.com/datasets/rowhitswami/stopwords
with open("stopwords.txt", "r") as file:
    for line in file.readlines():
        stopwords.append(line.replace("\n",""))



#serach keywords in html and return score based on match out of 100
def search_words(url, keywords):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    infobox = soup.find(class_="infobox").get_text(" ")
    print(infobox)
    found = []
    not_found = []
    for word in keywords:
        print("word: "+word)
        if((re.search(word, soup.get_text()) or re.search(word, infobox)) and word.lower() not in found):
            print("found: ", word)
            found.append(word.lower())
            # elif(word[0].islower() and word.title() in keywords):
            #     found.append(word.lower())
    print("############################################################## ",found)
    for word in keywords:
        if(word.lower() not in found and word.lower() not in not_found):
                not_found.append(word.lower())
            
    if(len(found) > 0):
        score = len(found)/(len(found)+len(not_found))*100
    else:
        score = 0
    return {"score":score, "found":found, "not_found":not_found}


#find score for each profile
for user in wiki_data.keys():
    print(user)
    if("score" not in data[user].keys() or data[user]["score"] == 0): 
        current_user = twitter_profile[twitter_profile["username"] == user]
        name = current_user["name"].iloc[0]
        description = current_user["description"].iloc[0]
        location = current_user["location"].iloc[0]
        # print(description)
        url = wiki_data[user]["full-url"]
        keywords = []
        keywords.append(name)
        if(type(description) != float):
            regex = re.compile('[https://t.co/]+\\w{10}')
            description = remove_emojis(re.sub(regex, "", description))
            # print("Description: ", description)
            for word in word_tokenize(description):
                word = word.replace("+", "")
                if(not word.isdigit() and word.lower() not in stopwords and len(word) > 2 and (word.title() not in keywords and word.lower() not in keywords)):
                    keywords.append(word.title())
                    keywords.append(word.lower())
        if(type(location) != float):
            for word in word_tokenize(location):
                if word.lower() not in stopwords and len(word) > 2:
                    if(word == "nyc" or word == "NYC"):
                        word = "New York City"
                    if(word == "LA"):
                        word = "Los Angeles"
                    keywords.append(word)
        print("keywords: ",keywords)
        result = search_words(url, keywords)
        print(result)
        temp = data[user]
        temp["score"] = result["score"]
        temp["found"] = result["found"]
        temp["not_found"] = result["not_found"]
        update_json("celeb-data.json", {user:temp})
        time.sleep(15)




# print(search_words("https://en.wikipedia.org/wiki/Eva_Longoria", ['Eva Longoria Baston', 'Risacookware', 'risacookware', 'Clubnecaxa', 'clubnecaxa', 'Weareangelcity', 'weareangelcity', 'Equila', 'equila', 'Weareunbelievable', 'weareunbelievable']))
    