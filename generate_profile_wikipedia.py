import wikipediaapi
import wikipedia
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

wiki = wikipediaapi.Wikipedia(f'CelebInfo/0 {os.environ.get("contact")}', "en")


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

#parse url to extract data
def parse_url(url, username):
    #open csv file to retrieve data
    dataFrame = pd.read_csv("extra-data.csv", sep=":::",engine='python')
    data = dataFrame[dataFrame["username"] == username]
    keywords = [i for i in data.values]
    #search keywords
    req = requests.get(url, auth=('user', 'pass'))

#simple search check if the wikipedia page exist with the name, if exist do keyword search otherwise search all the result
def simple_search(name,username):
    score = 0
    result = wiki.page(name)
    if(result.exists):
        score += 1
        url = result.fullurl
        req = requests.get(url)
        if(req.status_code == 200):
            #open csv file to retrieve data
            dataFrame = pd.read_csv("extra-data.csv", sep=":::",engine='python')
            data = dataFrame[dataFrame["username"] == username]
            soup = BeautifulSoup(req.content, 'html.parser')
            for keys in data.values.tolist():
                for key in keys:
                    for keyword in remove_emojis(str(key).replace(",","")).split(" "):
                        if(keyword != ""):
                            print(keyword)
                            if(len(soup.body.findAll(string=re.compile(str(keyword)+"|"+str(keyword.lower())))) > 0):
                                score += 1
    if(score > 5):
        data = []
        birth_date = soup.find(class_="bday").text
        if(len(birth_date)>0):
            data.append(birth_date)
        occupation = soup.find(class_="hlist").text
        if(len(occupation)>0):
            data.append(occupation)
        print(data)

    else:
        #do query url search    
        pass    

simple_search("Kevin Durant","KDTrey5")
