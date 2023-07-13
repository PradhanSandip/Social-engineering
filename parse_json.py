from pathlib import Path
import json
import re


'''read and retun json file'''
def read_json(file_name):
    #if file does not exist
    if(not Path(file_name).exists()):
        #create file
        with open(file_name, "w") as file:
            #write data
            file.write("{}")
    #open file
    with open(file_name, "r+") as file:
        #return json data
        return json.load(file)

'''function to update and save json file'''
def update_json(file_name, content):
    #load json data of a file
    data = read_json(file_name)
    #update json
    data.update(content)
    #open json file
    with open(file_name, "w") as file:
        #save updated json 
        json.dump(data, file)


'''retrive json by key'''
def get_json_object_by_key(file_name, key):
    return read_json(file_name)[key]

'''print json in more readable form'''
def print_json(file_name, key):
    data = get_json_object_by_key(file_name, key)
    for key in data.keys():
        print(key+": "+data[key], end="\n")

    print("---------------------------------------------------------------------------------",end="\n\n")

'''get date of birth and age'''
def name_date_age_occupation(file_name, key):
    result = {}
    data = read_json(file_name)[key]
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
        
    print(result)

for key in read_json("celeb-data.json").keys():
    name_date_age_occupation("celeb-data.json", key)


