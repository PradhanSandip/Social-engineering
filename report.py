import matplotlib.pyplot as plt
from pathlib import Path
from parse_json import read_json
import numpy as np

# wikipedia data
wiki_data = read_json("celeb-data.json")

#draw bar chart visualising dataset
def count_english_profiles():
    #total_dataset
    total_profile = list(Path("twitter-celebrity-tweets-data").rglob("*.csv"))
    #english_dataset
    english_profile = list(Path("english_only").rglob("*.csv"))
    #profile exist in wikipedia
    wiki_profile = 0
    #get total number of profiles that exist in wikipedia
    for profile in english_profile:
        if(profile.name[:-4] in wiki_data.keys()):
            wiki_profile += 1
    #draw bar chart
    x = np.array(["Total Profiles", "English Profiles", "Profile in wikipedia"])
    y = np.array([len(total_profile), len(english_profile), wiki_profile])
    fig, ax = plt.subplots()
    ax.set_title("Dataset information")
    bars = ax.bar(x,y, width=0.4, color="#33cccc")
    ax.bar_label(bars)
    plt.show()

#dataset report
count_english_profiles()

#draw bar char visiualising score based on keyword match in wikipedia
def average_score():
    #english_dataset
    english_profile = list(Path("english_only").rglob("*.csv"))
    total_score = 0
    profile_count = 0
    #get total number of profiles that exist in wikipedia
    for profile in english_profile:
        if(profile.name[:-4] in wiki_data.keys()):
            total_score += wiki_data[profile.name[:-4]]["score"]
            profile_count += 1
    average = int(total_score/profile_count)
    #draw bar char
    x = np.array(["Average score"])
    y = np.array([average])
    fig, ax = plt.subplots()
    ax.set_title("Wikipedia profile score based on keywords")
    bars = ax.bar(x,y, width=0.4, color="#33cccc")
    ax.set_xlim(-2,2)
    ax.bar_label(bars)
    plt.show()

average_score()


