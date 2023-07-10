import os
import pandas as pd
import tweepy 
from pathlib import Path
import numpy as np 
#authentication
client = tweepy.Client(bearer_token=os.environ.get("bearer_token"), 
access_token=os.environ.get("access_token"), access_token_secret=os.environ.get("access_token_secret"),consumer_key=os.environ.get("api_key"), 
consumer_secret=os.environ.get("api_key_secret"),return_type=dict, wait_on_rate_limit=True)
#csv se[erator
csv_sep = ':::'

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
    np.savetxt(save_file, frame, delimiter=csv_sep, header=csv_sep.join(frame.columns.values), fmt='%s', comments='', encoding=None)


#twitter rate limit
max=500
#count request number
counter = 0

#for each csv file
for file_ in list(files)[400:500]:
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
                s =  data["id"]+csv_sep+data["username"]+csv_sep+ data["name"]+csv_sep+ data["description"].replace("\n"," ")+csv_sep+ data["location"]+"\n"
            else:
                #store relevant data (no location)
                s = data["id"]+csv_sep+data["username"]+csv_sep+data["name"]+csv_sep+data["description"].replace("\n"," ")+csv_sep+ ""+"\n"
           
           #open the csv file
            with open(save_file,"a",encoding="utf-8") as data_file:
                #write to csv file
                data_file.write(s)
            #increment the counter
            counter += 1
            #print request counter and username
            print(counter,username)
        else:
            print(username+" does not exist")
        
 




