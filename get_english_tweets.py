import langid #language detection library
import pandas as pd #pandas to read csv
import random #to generate random number
import shutil # to copy files
from pathlib import Path # to manipulate directories
csv_path = "./twitter-celebrity-tweets-data" # tweet dataset folder
save_path = "./english_only" #english tweet save location

if(not Path(save_path).exists()): #if save folder does not exist
    os.makedirs(save_path) # create save folder


files = Path(csv_path).rglob("*.csv") # get all the csv files in the dataset

for f in files: # for each csv file
    content = pd.read_csv(f)["tweet"] # retrieve tweets
    is_english = 0 # score out of 4
    for i in range(4): # for 4 tweets
        if(langid.classify(content[random.randint(0,len(content)-1)][2:-1]))[0] == "en": # if tweet is in english
            is_english += 1 # add score
    if(is_english > 2): #if the score is 3 or more
        shutil.copy2(f, save_path) # save the csv to save location
        is_english = 0 # reset score
        print(f) # print file name
    
    
    


