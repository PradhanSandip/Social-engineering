import wikipediaapi
import wikipedia
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
import json
from pathlib import Path
import time
from parse_json import read_json, update_json
#wikipedia api
wiki = wikipediaapi.Wikipedia(f'CelebInfo/0 {os.environ.get("contact")}', "en")

#json file to save celeb info
save_file = "celeb-data.json"


#remove emojis from the string
def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)





#return url of page matches name
def get_urls(name):
    #search wiki with name
    search = wikipedia.search(name)
    #if search returns result
    if(len(search) > 0):
        #list to store urls
        urls = []
        #for each result
        for r in search:
            #save the full url
            urls.append(wiki.page(r).fullurl)
    #return urls
    return urls

#parse url to extract data
def parse_url(url, username):
    #open csv file to retrieve tweeet data 
    dataFrame = pd.read_csv("extra-data.csv", sep=":::",engine='python')
    #get row that matches username
    data = dataFrame[dataFrame["username"] == username]
    #list of keywords from twitter profile
    keywords = [i for i in data.values]
    #search keywords
    req = requests.get(url)
    #TODO: parse html

#simple search check if the wikipedia page exist with the name, if exist do keyword search otherwise search all the result
def simple_search(name,username):
    #print current username and name
    print(name,username)
    #score based on keyword match in wiki
    score = 0
    #get wiki page with name
    result = wiki.page(name)
    #if result exists
    if(result.exists() and result.summary != ""):
        #add score
        score += 1
        #get full page url
        url = result.fullurl
        #get html 
        req = requests.get(url)
        #if request is ok
        if(req.status_code == 200):
            #open csv file to retrieve user profile data
            dataFrame = pd.read_csv("extra-data.csv", sep=":::",engine='python')
            #get userprofile that matches username
            data = dataFrame[dataFrame["username"] == username]
            #BS4 object
            soup = BeautifulSoup(req.content, 'html.parser')
            #for each column in profile
            for keys in data.values.tolist():
                #for each word in column
                for key in keys:
                    #remove special characters and emojis
                    for keyword in re.sub(r"[+(),*]", " ", remove_emojis(str(key))).split(" "):
                        #if word not empty
                        if(keyword != ""):
                            #print keyword
                            print("Keyword: "+keyword)
                            #if keyword is found
                            if(len(soup.body.findAll(string=re.compile(str(keyword)+"|"+str(keyword.lower())))) > 0):
                                #add score
                                score += 1
    #if score 1 or more
    if(score > 1):
        #find the infobox in wiki page
        table_row = soup.find(class_="infobox")
        #if infobox does not exist
        if(table_row == None):
            #exit
            return
        #get all the row in infobox
        table_row = soup.find(class_="infobox").find_all("tr")
        #initial json object
        json_object = {username:{"name":name,"full-url":url}}
        #for each row in infobox
        for row in table_row:
            #empty result
            content = ""
            #find the infobox head (key/title/column name)
            table_head = row.find("th")
            #if table head exist
            if(table_head != None):
                #get the text
                key = table_head.text
                #find table data
                parent = row.find("td")
                #if table data exist 
                if(parent != None):
                    #for all the table data in a row
                    for child in parent.children:
                        #if the child is not style tag
                        if(child.name != "style"):
                            #if child is div and contain ul element
                            if(child.name == "div" and child.find("ul") != None):
                                #get all the li elements
                                for index,li in enumerate(child.find_all("li")):
                                    #as long as the li element no the end li
                                    if(index != len(child.find_all("li"))-1):
                                        #add the text to the content + a seperator "/"
                                        content += li.text + "/"
                                    #else just add the text
                                    else:
                                        content += li.text
                            #if the child is not div or contains ul element
                            else:
                                #just get the text
                                content += child.text
                    #create a json object with username as key and content as value            
                    json_object[username][" ".join(table_head.text.splitlines()).replace(u"\u2013",u"-").replace(u'\xa0', u' ')] = " ".join(content.replace(u'\xa0', u' ').replace(u"\u2013",u"-").replace("\n"," ").replace(u'\\u',u' ').encode('ascii',errors='ignore').decode().splitlines())
        #update the json file with new key value
        update_json(save_file, json_object)
        #print the new json object
        print(json_object)
        #sleep for 5 sec to avoid server timeout
        time.sleep(5)       
            

    else:
        #do query url search    
        pass    

#get all the tweeter profile
celeb_list = pd.read_csv("extra-data.csv", sep=":::",engine="python")
#for each profile
for celeb in celeb_list.to_records():
    #load the json file containing celeb data
    data = read_json(save_file)
    #if the json file does not contain celebrity with username
    if(celeb["username"] not in data.keys()):
        #retrieve data from wiki with name
        simple_search(celeb["name"],celeb["username"])
        #sleep for 1 sec
        time.sleep(1)
    



