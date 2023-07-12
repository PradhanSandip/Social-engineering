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
    search = wikipedia.search(name)
    if(len(search) > 0):
        urls = []
        for r in search:
            urls.append(wiki.page(r).fullurl)
    return urls

# #parse url to extract data
# def parse_url(url, username):
#     #open csv file to retrieve data
#     dataFrame = pd.read_csv("extra-data.csv", sep=":::",engine='python')
#     data = dataFrame[dataFrame["username"] == username]
#     keywords = [i for i in data.values]
#     #search keywords
#     req = requests.get(url)

#simple search check if the wikipedia page exist with the name, if exist do keyword search otherwise search all the result
def simple_search(name,username):
    #print current name and username
    print(name,username)
    #score based on keyword matches
    score = 0
    #get wiki page with name
    result = wiki.page(name)
    #if page exist
    if(result.exists() and result.summary != ""):
        #add score 
        score += 1
        #get page full url
        url = result.fullurl
        #get html
        req = requests.get(url)
        #if status ok
        if(req.status_code == 200):
            #open csv file containing tweets
            dataFrame = pd.read_csv("extra-data.csv", sep=":::",engine='python')
            #get the row matching username
            data = dataFrame[dataFrame["username"] == username]
            #BS4 object
            soup = BeautifulSoup(req.content, 'html.parser')
            #for each column in csv
            for keys in data.values.tolist():
                #for each word
                for key in keys:
                    #remove specia characters and emojis and create list of words
                    for keyword in re.sub(r"[+(),*?-]", " ", remove_emojis(str(key))).split(" "):
                        #if the word is not empty
                        if(keyword != ""):
                            #print key word
                            print("Keyword: "+keyword)
                            #if keyword in wiki page 
                            if(len(soup.body.findAll(string=re.compile(str(keyword)+"|"+str(keyword.lower())))) > 0):
                                #add score
                                score += 1
    #if score more than 1
    if(score > 1):
        
        table_row = soup.find(class_="infobox")
        if(table_row == None):
            return
        table_row = soup.find(class_="infobox").find_all("tr")
        json_object = {username:{"name":name,"full-url":url}}
        for row in table_row:
            content = ""
            table_head = row.find("th")
            if(table_head != None):
                key = table_head.text
                parent = row.find("td")
                if(parent != None):
                    for child in parent.children:
                        if(child.name != "style"):
                            if(child.name == "div" and child.find("ul") != None):
                                for index,li in enumerate(child.find_all("li")):
                                    if(index != len(child.find_all("li"))-1):
                                        content += li.text + "/"
                                    else:
                                        content += li.text
                            else:
                                content += child.text
                    json_object[username][" ".join(table_head.text.splitlines()).replace(u"\u2013",u"-").replace(u'\xa0', u' ')] = " ".join(content.replace(u'\xa0', u' ').replace(u"\u2013",u"-").replace("\n"," ").replace(u'\\u',u' ').encode('ascii',errors='ignore').decode().splitlines())
                    # print(table_head.text+"->")
                    # print(content.strip())  
        if(not Path(save_file).exists()):
            with open(save_file, "w") as jf:
                json.dump(json_object, jf)  
        else:
            with open(save_file, "r") as jf:
                data = json.load(jf)
            data.update(json_object)
            with open(save_file, "w") as jf:
                json.dump(data, jf) 
        print(json_object)
        time.sleep(5)       
            

    else:
        #do query url search    
        pass    

#
celeb_list = pd.read_csv("extra-data.csv", sep=":::",engine="python")
ignore = []
with open("ignore_missing.json", "r") as file:
    ignore = json.load(file)["data"]["ignore"]
for celeb in celeb_list.to_records():
   if(celeb["username"] not in ignore):
        if(Path(save_file).exists()):
            with open(save_file, "r") as jf:
                data = json.load(jf)
            if(celeb["username"] not in data.keys()):
                simple_search(celeb["name"],celeb["username"])
                
            else:
                continue
        else:
            simple_search(celeb["name"],celeb["username"])
        



