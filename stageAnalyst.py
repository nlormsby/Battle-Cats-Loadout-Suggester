from selenium import webdriver
import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
import re

import ratingCalculation


# import cat data from csv from catStatList
cat_frame = pd.read_csv('catStatList.csv')
print(cat_frame)

# set up Selenium start
url = 'https://mygamatoto.com/allstages/search-by-stage-name'
driver = webdriver.Chrome()
driver.get(url)

# wait for stage selection
input("Open a stage and press Enter to continue...")

# find table rows
enemy_tables = driver.find_elements("css selector", '.ant-table-body > .ant-table-fixed > tbody')
enemies = enemy_tables[1].find_elements("xpath", './/tr')

# define some variables
enemy_list = []
enemy_api = 'https://onestoppress.com/api/singleenemy'
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
type_list = {"red", "floating", "black", "metal", "white", "angel", "alien", "zombie", "aku", "relic"}

# scrape each enemy row
for enemy in enemies:
    Name = enemy.find_element("xpath", './/td[1]/a/img').get_attribute('alt')
    Amplifier = enemy.find_element("xpath", './/td[2]/div').text
    Number = enemy.find_element("xpath", './/td[3]').text
    Base = enemy.find_element("xpath", './/td[4]').text
    Time = enemy.find_element("xpath", './/td[5]').text
    Interval = enemy.find_element("xpath", './/td[6]').text
    Boss = enemy.find_element("xpath", './/td[7]').text

    # call api for data not on the website
    api_name = '{"compare":"' + Name + '"}'
    r = requests.post(url=enemy_api, headers=headers, data=api_name)
    data = r.json()
    enemy_data = data['sampledata']

    #transfer api data to pandas and add modifiers for stage
    HP = enemy_data["hp"] * (int(Amplifier.rstrip("%"))/100)
    Attack = enemy_data["atk"] * (int(Amplifier.rstrip("%"))/100)
    DPS = enemy_data["dps"] * (int(Amplifier.rstrip("%"))/100)
    Speed = enemy_data["speed"]
    Range = enemy_data["range"]
    Target = enemy_data["att_type"]
    ability_desc = enemy_data["special_att_desc"]
    traits = re.findall(r'b1(.*?)b2', ability_desc)
    Abilities = []
    Immunities = []
    for trait in traits:
        if "immune" in trait:
            Immunities.append(trait[:-7])
        else:
            Abilities.append(trait)



    # condense types into one column
    Types = []
    for type in type_list:
        if enemy_data[type]:
            Types.append(type)

    # define a pandas row and add
    enemy_item = {
        'Name': Name,
        'Amplifier': Amplifier,
        'HP': HP,
        'Attack': Attack,
        'DPS': DPS,
        'Number': Number,
        'Base': Base,
        'Time': Time,
        'Interval': Interval,
        'Boss': Boss,
        'Speed': Speed,
        'Range': Range,
        'Target': Target,
        'Abilities': Abilities,
        'Immunities': Immunities,
        'Types': Types
    }
    enemy_list.append(enemy_item)

enemy_frame = pd.DataFrame(enemy_list)
# print(enemy_frame.to_string())

# Apply the overall rating calculation to each row in cat_frame
cat_frame['rating'] = cat_frame.apply(lambda row: ratingCalculation.calculate_overall_rating(row, enemy_frame), axis=1)


#sort cats by rating
cat_frame = cat_frame.sort_values(by='rating', ascending=False)

print(cat_frame.to_string())