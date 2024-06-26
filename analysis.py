import nltk
import re
from nltk import word_tokenize, pos_tag, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import pandas as pd
from ast import literal_eval
from generate_profile_wikipedia import remove_emojis
from pathlib import Path
from query import name_date_age_occupation
from parse_json import update_json, read_json


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
                    if(calculated[2:] == n_d_a_o["dob"][2:]):
                        print("Predicted: "+calculated)
                        print("DOB: "+n_d_a_o["dob"])
                        result = {n_d_a_o["name"]:{"calculated_dob": calculated, "wiki_dob": n_d_a_o["dob"], "mentions":context_result, "tweet":tweet}}
                        update_json(save_result, result)
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
    contexts = []
    predictions = []
    save_location = "favorites.json"
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
            org = tweet
            tweet = re.sub("(https|http)+(:|://)+(bit.ly+/\w{1,10}|(t.co+/\w{1,10}))", " ", tweet) #remove links
            # tweet = re.sub("@\w+", "",tweet) #remove mentions
            tweet = re.sub("RT|'|/|[\"]","",tweet) #remove RT. ',/,\,"
            sentence = sent_tokenize(tweet)
            for tweet_sentence in sentence:
                regex = re.compile("favorite")
                result = re.search(regex, tweet_sentence)
                prediction = ""
                label_found = False
                prediction_result = ""
                if(result):
                    info = tweet_sentence.split("favorite")[1]
                    for word in word_tokenize(info):
                        if(pos_tag([word])[0][1] == "NN" or pos_tag([word])[0][1] == "NNS" or pos_tag([word])[0][1] == "NNP"):
                            prediction += word+" "
                            label_found = True
                        else:
                            if(label_found):
                                break
                    if(re.search(" is my ", tweet_sentence)):
                        if(re.search('"."', tweet_sentence)):
                            prediction_result += re.re.search('"."', tweet_sentence).group()
                        info = tweet_sentence.split(" is my ")[0]
                        prediction_result += info.split()[::-1][0]
                        current_pos = pos_tag(info.split()[::-1])[0][1]
                        for word in pos_tag(info.split()[::-1])[1:]:
                            if(current_pos != "" and word[1] == "JJS"):
                                prediction_result = word[0] + " " + prediction_result
                            if(word[1] == "NN" or word[1] == "NNS" or word[1] == "NNP" or word[1] == "CD"):
                                new_string = word[0] + " " + prediction_result
                                prediction_result = new_string
                                current_pos = word[1]
                            else:
                                break
                            
                    if(prediction_result != ""):
                        print("favorite "+prediction+":"+ prediction_result+"    :"+tweet)
                        contexts.append("favorite "+prediction)
                        predictions.append(prediction_result)
    if(len(contexts) > 0 and len(predictions) > 0):
        pass
            #update_json(save_location, {target.name[:-4]:{"context": contexts, "prediction":predictions}})
           
                    

    
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")

def analyse_location(target):
    print("###########################"+target.name+"#########################################")
    save_location = "location.json"
    dictionary = {}
    data = pd.read_csv(target)
    #tweets
    tweets = data["tweet"]
    contexts = []
    locations = []
    reg = re.compile(" \\b(Avenue)\\b| \\b(Lane)\\b| \\b(Road)\\b| \\b(Boulevard)\\b| \\b(Street)\\b| \\b(Ave)\\b| \\b(Rd)\\b| \\b(Blvd+)\\b| \\b(Ln)\\b| \\b(St)\\b")
    for index, tweet in enumerate(tweets):
        if(tweet.startswith('b')):
            tweet = remove_emojis(literal_eval(tweet).decode("UTF-8"))
        tweet = re.sub("(https|http)+(:|://)+(bit.ly+/\w{1,10}|(t.co+/\w{1,10}))", " ", tweet)
        result = re.finditer(reg, tweet)
        
        for group in result:
            location = ""
            context = ""
            current_focus_left = tweet[:group.span()[0]]
            current_focus_right = tweet[group.span()[1]:].replace(".", "")
            location += group.group()
            for word in pos_tag(current_focus_left.split())[::-1]:
                if(word[1] == "NNP" or word[1] == "CD"):
                    location = word[0] + " " + location
                else:
                    break
            for word in pos_tag(current_focus_right.split()):
                
                if(word[1] == "NNP"  or word[1] == "CD"):
                    location = location + " " + word[0]
                else:
                    break
            if(len(location.split()) > 1 and location not in locations):
                locations.append(location.strip())
                if(group):
                    for word in pos_tag(tweet.split()):
                        if(word[1] == "NN" or word[1] == "NNP" and word[0] not in " ".join(locations).split()):
                            context += word[0] + " "
                    contexts.append(context)


            

    if(len(locations) > 0):
        for contex, location in zip(contexts, locations):
            print("################################################################")
            print("# Context: ",context)
            print("# Location: ", location)
            print("################################################################")
        # update_json(save_location, {target.name[:-4]: {"location":locations, "context": contexts}})
    
    print("#########################END###################################")

def predict_occupation(target):
    print(target.name[:-4],"\n","--------------------------------------------------------------------------------------------------------------------------------------")
    tracker = {}
    data = pd.read_csv(target)
    dictionary = read_json("occupation_dictionary.json")
    #tweets
    tweets = data["tweet"]
    for index, tweet in enumerate(tweets):
        if(tweet.startswith('b')):
            tweet = remove_emojis(literal_eval(tweet).decode("UTF-8"))
            words = word_tokenize(tweet)
            for word in words:
                tag = pos_tag([word])[0]
                if((tag[1] == "NN" or tag[1] == "NNS") and len(tag[0]) > 2):
                    word = tag[0]
                    if(len(word) < 3):
                        print(tag)
                    for key in dictionary.keys():
                        if(key in tracker.keys()):
                            if(word not in tracker[key]["checked"] and word.lower() in dictionary[key]):
                                
                                tracker[key]["score"] += 1
                                tracker[key]["checked"].append(word)
                        else:
                            if(word.lower() in dictionary[key]):
                                tracker[key] = {"score":1,"checked":[word]}
    score_dict = {key:tracker[key]["score"] for key in tracker.keys()}
    print(list(sorted(score_dict.items(), key=lambda item: item[1],reverse=True))[0][0],end="\n")
    # for key in score_dict:                                            ####### total percentage base approach #####
    #     if(score_dict[key]/len(dictionary[key]) > 0.5):
    #         print(key, score_dict[key]/len(dictionary[key]))          #############################################
    print("############# Actual occupation (from Wiki) #####################")
    data = name_date_age_occupation(target.name[:-4])
    if("occupation" in data.keys()):
        print(data["occupation"])
        print("---------------------------------------------------------------------------------------------------------------------------\n\n")
    else:
        print("NO INFO")
        print("---------------------------------------------------------------------------------------------------------------------------\n\n")
    
if __name__ == "__main__":
    csvs = Path("english_only").rglob("*.csv")
    # analyse_favorite(Path("english_only\ActuallyNPH.csv"))
    # predict_occupation(Path("english_only\ActuallyNPH.csv"))
    # predict_occupation(Path("english_only\\10Ronaldinho.csv"))
    celeb_data = read_json("celeb-data.json")
    for csv in csvs:
        if(csv.name[:-4] in celeb_data.keys()):
            # pass
            # analyse_birthday(csv)
            # analyse_occupation(csv)
            # analyse_favorite(csv)
            analyse_location(csv)
            # predict_occupation(csv)
    csvs  = Path("new_tweets").rglob("*.csv")
    for csv in csvs:
        if(csv.name[:-4] in celeb_data.keys()):
            pass
            # analyse_birthday(csv)
            # predict_occupation(csv)
            # analyse_favorite(csv)
            # analyse_location(csv)
            # predict_occupation(csv)
    # pd.DataFrame(csv_data).to_csv(incorrect_result, index=False, header=["id","name","calculated_dob","wiki_dob","mentions","tweet"])