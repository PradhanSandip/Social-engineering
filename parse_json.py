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




