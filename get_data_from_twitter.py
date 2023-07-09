import os
import pandas as pd
import tweepy 
from pathlib import Path

#authentication
client = tweepy.Client(bearer_token=os.environ.get("bearer_token"), 
access_token=os.environ.get("access_token"), access_token_secret=os.environ.get("access_token_secret"),consumer_key=os.environ.get("api_key"), 
consumer_secret=os.environ.get("api_key_secret"),return_type=dict, wait_on_rate_limit=True)


csv_path = "./twitter-celebrity-tweets-data" # tweet dataset folder
#get csv files
files = Path(csv_path).rglob("*.csv")
#save location for retrieved data
save_file = "extra-data.csv"
#check if save file exist
if(not Path(save_file).exists()):
    #data frame with relevant column
    frame = pd.DataFrame(columns=["id", "username","name","description","location"])
    #save the data frame in csv file
    frame.to_csv(save_file,index=False)

#twitter rate limit
max=500
#count request number
counter = 0

#for each csv file
for file_ in list(files):
    #open the csv file
    write_file = pd.read_csv(save_file)
    #if rate limit not reached
    if(counter < max):
        #get username
        username = file_.name[:len(file_.name)-4]
        #request user data by username
        res = client.get_user(username=username,user_fields=["id,username,name,description,location"])
        #print result
        print(res)
        #if request contains profile data
        if("data" in res.keys()):
            #profile data
            data = res["data"]
            #if the profile data contains location
            if("location" in data.keys()):
                #store the relevant data + location
                s =  [data["id"],data["username"], data["name"], data["description"].replace("\n"," "), data["location"]]
            else:
                #store relevant data (no location)
                s = [data["id"],data["username"], data["name"], data["description"], None]
            #write to csv file
            write_file.loc[-1] = s
            #save the csv file
            write_file.to_csv(save_file, index=False)
            #increment the counter
            counter += 1
            #print request counter and username
            print(counter,username)
        
 




