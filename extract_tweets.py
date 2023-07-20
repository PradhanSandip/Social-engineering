import tweepy
import pandas as pd
from pathlib import Path
from parse_json import read_json, update_json
import os

#authentication
client = tweepy.Client(bearer_token=os.environ.get("bearer_token"), 
access_token=os.environ.get("access_token"), access_token_secret=os.environ.get("access_token_secret"),consumer_key=os.environ.get("api_key"), 
consumer_secret=os.environ.get("api_key_secret"),return_type=dict, wait_on_rate_limit=True)
#track tweet extration
save_file = "track_tweet_extraction.json"
#get users with wiki data 
wiki_data_users = read_json("celeb-data.json").keys()
#get users with english tweets
files = Path("english_only").rglob("*.csv")
english_tweet_users = []
for file in files:
    english_tweet_users.append(file.name[:-4])

def get_lateset_twitter_id(user):
    if(Path(f"new_tweets\{user}.csv").exists() and pd.read_csv(f"new_tweets\{user}.csv").shape[0] > 0):
        return pd.read_csv(f"new_tweets\{user}.csv").loc[0]["twitter_id"]
    else:
        return pd.read_csv(f"english_only\{user}.csv").loc[0]["twitter_id"]

# t = read_json("tweet-count.json")["10Ronaldinho"]
# # print(t)
# # update_json("tweet-count.json", {"10Ronaldinho":t})


#get users who has wiki data and tweets in english
# wiki_english_user = []
# for user in english_tweet_users:
#     if(user in wiki_data_users):
#         wiki_english_user.append(user)

'''
# #creating json file to track tweet conunts 
save_file = "tweet-count.json"
#create json file
read_json(save_file)
for english_user in english_tweet_users:
    tweet_count = pd.read_csv(f"english_only\\{english_user}.csv").shape[0]
    json_object = {}
    json_object[english_user] = {"tweet_count": tweet_count, "additional_download": 0, "more_available": True, "twitter_id": ""}
    update_json(save_file, json_object)
'''

#go thorugh each user if user has less than 3000 tweets download more
save_folder = "new_tweets/"
config_data = read_json("tweet-count.json")
config_data_keys = config_data.keys()

for user in config_data_keys:
    if(config_data[user]["more_available"] == True):
        print(user,end="\n##################################################################################################################################")
        save = save_folder+user+".csv"
        user_id = config_data[user]["twitter_id"] 
        if(user_id == ""):
            user_id = client.get_user(username=user)
            if("data" in user_id.keys()):
                user_id = user_id["data"]["id"]
                json_data = read_json("tweet-count.json")[user]
                json_data["twitter_id"] = user_id
                update_json("tweet-count.json", {user:json_data})
            else:
                print("no profile")
                json_data = read_json("tweet-count.json")[user]
                json_data["more_available"] = False
                update_json("tweet-count.json", {user:json_data})
        #retrive more tweets encoding = UTF-8
        most_recent_tweet_in_dataset = pd.read_csv(f"english_only/{user}.csv")["date"]
        tweets = client.get_users_tweets(id=user_id,max_results=100,since_id=get_lateset_twitter_id(user),tweet_fields=["id","text","created_at","lang"], user_auth =False)
        returned_tweets = []
        print(tweets)
        #if request is successful
        if("errors" not in tweets.keys() and "data" in tweets.keys()):
            returned_tweets = list(reversed(list(tweets["data"])))
            json_data = read_json("tweet-count.json")[user]
            json_data["additional_download"] += tweets["meta"]["result_count"]
            update_json("tweet-count.json", {user:json_data})
            print("no errors")
        elif("errors" in tweets.keys() or tweets["meta"]["result_count"] == 0 or "data" not in tweets.keys()):
            print("no more new tweets")
            json_data = read_json("tweet-count.json")[user]
            json_data["more_available"] = False
            update_json("tweet-count.json", {user:json_data})
        else:
            print(tweets)
            print(user+" account disabled/not active/follower only")
        #create csv if not exist
        if(not Path(save).exists()):
            with open(save, "w") as file:
                header = pd.DataFrame(columns=["twitter_id","data","tweet","lang"])
                header.to_csv(save, sep=",",index=False)
        data = []
        print(returned_tweets)
        for tweet in returned_tweets:
            data.insert(0, {"twitter_id":tweet["id"], "date": tweet["created_at"], "tweet": tweet["text"].encode(), "lang": tweet["lang"]})
        
            print(tweet["created_at"], tweet["text"])
        new = pd.concat([pd.DataFrame(data), pd.read_csv(save)], ignore_index=True)
        new.to_csv(save, index=False)

            


        

