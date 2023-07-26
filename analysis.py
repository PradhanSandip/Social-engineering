import nltk
import re
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import pandas as pd
from ast import literal_eval
from generate_profile_wikipedia import remove_emojis
from pathlib import Path
from query import name_date_age_occupation

target = "english_only\Alyssa_Milano.csv"
stopwords = list(stopwords.words('english'))
#add additional stopwords source: https://www.kaggle.com/datasets/rowhitswami/stopwords
with open("stopwords.txt", "r") as file:
    for line in file.readlines():
        stopwords.append(line.replace("\n",""))

#age = dd-mm-yyyy
def calculate_age(age):
    pass




def analyse(target):
    data = pd.read_csv(target)
    tweets = data["tweet"]
    id = data["twitter_id"]
    result = {}
    for index, tweet in enumerate(tweets):
        if(tweet.startswith('b')):
            tweet = remove_emojis(literal_eval(tweet).decode("UTF-8"))
            tweet = re.sub("https://t.co/+\w{10}", " ", tweet)
            # print(tweet)
            tweet_token = word_tokenize(tweet)
            
            tweet_token = [word for word in tweet_token if word not in stopwords]
            #regular expressions
            reg_birthday = re.compile("\d{1,3}\w{2}+ +birthday|birthday+ +\d{1,3}\w{2}")
            reg_context = re.compile("@\w+")
            # reg_fav = re.compile("\w+ favorite +\w+")
            birthday_result = re.search(reg_birthday, tweet)
            context_result = ""
            if(birthday_result):
                context_result = re.findall(reg_context, tweet)
            if( birthday_result != None):
                print(tweet)
                print(birthday_result)
                #get file name
                file = str(target).split("\\")[1][:-4]
                if(name_date_age_occupation(file) != None and "dob" in name_date_age_occupation(file).keys()):
                    print(name_date_age_occupation(file)["age"])
                print(context_result)
                print("------------------------------------------------------------------------------------------------")
                # print(pos_tag(tweet))
    



if __name__ == "__main__":
    csvs = Path("english_only").rglob("*.csv")
    for csv in csvs:
        analyse(csv)