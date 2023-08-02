from parse_json import read_json
import pandas as pd
from pathlib import Path
import re



#display number of tweets downloaded additionally 
def total_tweets_downloaded():
    celeb_data = read_json("tweet-count.json")
    total = 0
    for user in celeb_data.keys():
        total += celeb_data[user]["additional_download"]
    print(total)






'''get date of birth and age'''
def name_date_age_occupation(key):
    file_name = "celeb-data.json"
    result = {}
    
    data = read_json(file_name)
    if(key in data.keys()):
        data = data[key]
        result["name"] = data["name"]
        if("Born" in data.keys()):
            born = data["Born"]
            date_regex = re.compile("\d{4}-\d{2}-\d{2}")
            age_regex = re.compile("age \d{2}")
            search = (re.search(date_regex, born))
            if(search is not None):
                result["dob"] = "-".join(search.group().split("-")[::-1])
            search = re.search(age_regex, born)
            if(search is not None):
                result["age"] = search.group().split(" ")[1]
        elif("Date of birth" in data.keys()):
            born = data["Date of birth"]
            date_regex = re.compile("\d{4}-\d{2}-\d{2}")
            age_regex = re.compile("age \d{2}")
            search = (re.search(date_regex, born))
            if(search is not None):
                result["dob"] = "-".join(search.group().split("-")[::-1])
            search = re.search(age_regex, born)
            if(search is not None):
                result["age"] = search.group().split(" ")[1]

        if("Occupations" in data.keys()):
            result["occupations"] = data["Occupations"]
        elif("Occupation" in data.keys()):
            result["occupations"] = data["Occupation"]
        elif("Occupation(s)" in data.keys()):
            result["occupations"] = data["Occupation(s)"]
        elif("Role" in data.keys()):
            result["role"] = data["Role"]
        elif("Position" in data.keys()):
            result["position"] = data["Position"]
        elif("Position(s)" in data.keys()):
            result["position"] = data["Position(s)"]
        return result 

if __name__ == "__main__":
    celeb_data = read_json("celeb-data.json")
    users = []
    csv = list(Path("english_only").rglob("*.csv"))
    for user in csv:
        users.append(user.name[:-4])

    total = 0
    missing = 0
    for key in celeb_data.keys():
        if("occupations" in name_date_age_occupation(key).keys()):
            print(name_date_age_occupation(key)["occupations"])
    #     if(key in users):
    #         total += 1    
    #         if("dob" not in name_date_age_occupation(key).keys()):
    #             print(key)
    #             missing += 1

    # print(total, missing)