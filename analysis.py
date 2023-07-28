import nltk
import re
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import pandas as pd
from ast import literal_eval
from generate_profile_wikipedia import remove_emojis
from pathlib import Path
from query import name_date_age_occupation
from parse_json import update_json

target = "english_only\Alyssa_Milano.csv"
stopwords = list(stopwords.words('english'))
save_result = "results.json"
incorrect_result = "incorrect-result.csv"
csv_data = []
#add additional stopwords source: https://www.kaggle.com/datasets/rowhitswami/stopwords
with open("stopwords.txt", "r") as file:
    for line in file.readlines():
        stopwords.append(line.replace("\n",""))

#age = dd-mm-yyyy
def calculate_age(age, date):
    day = date.split("-")[0]
    month = date.split("-")[1]
    year = date.split("-")[2]
    year = int(year) - int(age)
    predicted = "-".join([str(day),str(month),str(year)])
    return predicted



#function that analysis each tweet for information
def analyse_birthday(target):
    #csv data
    data = pd.read_csv(target)
    #tweets
    tweets = data["tweet"]
    #ids
    id = data["twitter_id"]
    for index, tweet in enumerate(tweets):
        if(tweet.startswith('b')):
            tweet = remove_emojis(literal_eval(tweet).decode("UTF-8"))
            tweet = re.sub("https://t.co/+\w{10}", " ", tweet)
            # print(tweet)
            tweet_token = word_tokenize(tweet)
            tweet_token = [word for word in tweet_token if word not in stopwords]
            #regular expressions
            reg_birthday = re.compile("\d{1,3}\w{2} birthday|birthday+ +\d{1,3}\w{2}")
            reg_context = re.compile("@\w+")
            # reg_fav = re.compile("\w+ favorite +\w+")
            birthday_result = re.search(reg_birthday, tweet)
            context_result = ""               
            if( birthday_result != None):
                context_result = re.findall(reg_context, tweet)
                # print(tweet)
                tweet_age_found = re.search("\d+",birthday_result.group()).group()
                #get file name
                file = str(target).split("\\")[1][:-4]
                n_d_a_o = name_date_age_occupation(file)
                if( n_d_a_o != None and "dob" in n_d_a_o.keys()):
                    # print(context_result)
                    tweet_date = re.search("\d{4}-\d{2}-\d{2}", data["date"].loc[index])
                    tweet_date = "-".join(tweet_date.group().split("-")[::-1])
                    calculated = calculate_age(tweet_age_found, tweet_date)
                    if(calculated == n_d_a_o["dob"]):
                        pass
                        # print("Predicted: "+calculated)
                        # print("DOB: "+n_d_a_o["dob"])
                        # result = {n_d_a_o["name"]:{"calculated_dob": calculated, "wiki_dob": n_d_a_o["dob"], "mentions":context_result, "tweet":tweet}}
                        # update_json(save_result, result)
                    else:
                        csv_data.append([file,n_d_a_o["name"], calculated, n_d_a_o["dob"], context_result, tweet.encode()])    
                        
                    print("------------------------------------------------------------------------------------------------")
                        

def analyse_occupation(target):
    nouns = []
    #csv data
    data = pd.read_csv(target)
    #tweets
    tweets = data["tweet"]
    #ids
    id = data["twitter_id"]
    for index, tweet in enumerate(tweets):
        if(tweet.startswith('b')):
            tweet = remove_emojis(literal_eval(tweet).decode("UTF-8"))
            tweet = re.sub("https://t.co/+\w{0,10}", " ", tweet)
            tweet = re.sub("@\w+|@\s\w+", "",tweet)
            tweet = re.sub("RT","",tweet)
            tweet = tweet.replace("…","").replace("...","")
            # print(tweet)
            tweet_token = word_tokenize(tweet)
            tweet_token = [word.lower() for word in tweet_token if word.lower() not in stopwords and len(word) > 2]
            for token in tweet_token:
                tagger = pos_tag([token])
                if(tagger[0][1] == "NN"):
                    nouns.append(token)
    FreqDist(nouns).pprint(maxlen=100, stream=None)
    # i = FreqDist(nouns)
    # for x in i.keys():
    #     if(i[x] > 10 and len(x) > 2):
    #         print(x, i[x])

def analyse_favorite(target):
    word_list = []
    #csv data
    data = pd.read_csv(target)
    #tweets
    tweets = data["tweet"]
    #ids
    id = data["twitter_id"]
    for index, tweet in enumerate(tweets):
        if(tweet.startswith('b')):
            tweet = remove_emojis(literal_eval(tweet).decode("UTF-8"))
            tweet = re.sub("https://t.co+\w{10}", " ", tweet)
            tweet = re.sub("@\w+", "",tweet)
            tweet = re.sub("RT|'|/|[\"]","",tweet)
            regex = re.compile("favorite")
            result = re.search(regex, tweet)
            if(result):
                tweet_token = word_tokenize(tweet)
                tweet_token = [word.lower() for word in tweet_token if word.lower() not in stopwords and len(word) > 2]
                for token in tweet_token:
                    tagger = pos_tag([token])
                    if(tagger[0][1] == "NN"):
                        word_list.append(token)
    FreqDist(word_list).pprint(maxlen=100, stream=None)
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")





if __name__ == "__main__":
    csvs = Path("english_only").rglob("*.csv")
    for csv in csvs:
        # analyse_birthday(csv)
        # analyse_occupation(csv)
        analyse_favorite(csv)
    csvs  = Path("new_tweets").rglob("*.csv")
    for csv in csvs:
        # analyse_birthday(csv)
        # analyse_occupation(csv)
        analyse_favorite(csv)
    # pd.DataFrame(csv_data).to_csv(incorrect_result, index=False, header=["id","name","calculated_dob","wiki_dob","mentions","tweet"])