import nltk
import re
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import pandas as pd
from ast import literal_eval
from generate_profile_wikipedia import remove_emojis

target = "english_only\Alyssa_Milano.csv"
stopwords = list(stopwords.words('english'))
#add additional stopwords source: https://www.kaggle.com/datasets/rowhitswami/stopwords
with open("stopwords.txt", "r") as file:
    for line in file.readlines():
        stopwords.append(line.replace("\n",""))

def analyse():
    data = pd.read_csv(target)
    tweets = data["tweet"]
    id = data["twitter_id"]
    result = {}
    for tweet in tweets:
        if(tweet.startswith('b')):
            tweet = remove_emojis(literal_eval(tweet).decode("UTF-8"))
            tweet = re.sub("https://t.co/+\w{10}", " ", tweet)
            # print(tweet)
            tweet = word_tokenize(tweet)
            
            tweet = [word for word in tweet if word not in stopwords]
            tweet_sentence = " ".join(tweet)
            #regular expressions
            reg_number = re.compile("birthday")
            result = re.search(reg_number, tweet_sentence)
            if( result != None):
                print(tweet_sentence)
                print(pos_tag(tweet))
                print(result)
    

    

analyse()