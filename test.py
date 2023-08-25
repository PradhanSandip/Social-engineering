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



def analyse_favorite(string):
    
    tweet = remove_emojis(string)
    org = tweet
    tweet = re.sub("(https|http)+(:|://)+(bit.ly+/\w{1,10}|(t.co+/\w{1,10}))", " ", tweet) #remove links
    # tweet = re.sub("@\w+", "",tweet) #remove mentions
    tweet = re.sub("RT|'|/|[\"]","",tweet) #remove RT. ',/,\,"
    print(pos_tag(word_tokenize(string)))
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
                print(pos_tag(info.split()[::-1][1:]))
                for word in pos_tag(info.split()[::-1])[1:]:
                    print(word[1])
                    if(current_pos != "" and word[1] == "JJS"):
                        prediction_result = word[0] + " " + prediction_result
                    
                    if(word[1] == "NN" or word[1] == "NNS" or word[1] == "NNP" or word[1] == "CD"):
                        print("pass", word)
                        new_string = word[0] + " " + prediction_result
                        prediction_result = new_string
                        current_pos = word[1]
                    else:
                        break
                        

            if(prediction_result != ""):
                print("favorite "+prediction+":"+ prediction_result+"    :"+tweet)
                    

    
    print("------------------------------------------------------------------------------------------------------------------------------------------------------")

def analyse_location(string):
    tweet = string
    reg = re.compile(" \\b(Avenue)\\b| \\b(Lane)\\b| \\b(Road)\\b| \\b(Boulevard)\\b| \\b(Street)\\b| \\b(Ave)\\b| \\b(Rd)\\b| \\b(Blvd+)\\b| \\b(Ln)\\b| \\b(St)\\b")
    tweet = remove_emojis(tweet)
    result = re.finditer(reg, tweet)
    context = ""
    locations = []
    if(result):
        # print(pos_tag(word_tokenize(tweet)))
        for group in result:
            location = ""
            current_focus_left = tweet[:group.span()[0]]
            current_focus_right = tweet[group.span()[1]:].replace(".", "")
            location += group.group()
            for word in pos_tag(current_focus_left.split())[::-1]:
                if(word[1] == "NNP" or word[1] == "NNS" or word[1] == "CD"):
                    # print(word[0], word[1])
                    location = word[0] + " " + location
                else:
                    break
            for word in pos_tag(current_focus_right.split()):
                
                if(word[1] == "NNP" or word[1] == "NNS" or word[1] == "CD"):
                    location = location + " " + word[0]
                else:
                    break
            locations.append(location.strip())
        for word in pos_tag(tweet.split()):
            if(word[1] == "NN" or word[1] == "NNP" and word[0] not in " ".join(locations).split()):
                context += word[0] + " "
        
            
    print(context,locations)


analyse_location("Last night I was out on patrol with NYPD First Deputy Commissioner Caban at Chambers Street and Canal Street subway lines. Pu")
analyse_location("Chicago! TOMORROW!!! Come hang out with me! @ReebokClassics Freestyle Hi at @villa_hydepark 5230 S. Lake Park Ave")
# analyse_location("RT @sheandhim: She &amp; Him are in Las Vegas tonight playing the Boulevard Pool at The Cosmopolitan! A few tickets are still available: http:/…")
analyse_location("An Australian band in Chambers Street and St. Louis tonight!!")

#An Australian band in Chambers
#and St. Louis tonight!!

#An Australian band in Chambers Street and 
#Louis tonight!!