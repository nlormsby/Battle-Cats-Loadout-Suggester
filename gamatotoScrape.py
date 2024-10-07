from selenium import webdriver
import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
import time
from pandas import json_normalize

# Get a list to scrape
cat_url = 'https://mygamatoto.com/comparecats/'
listCheck = input("Do you have a My Gamatoto Cat List? (yes/no)")

while not (listCheck == "yes" or listCheck == "no"):
    listCheck = input("Do you have a My Gamatoto Compare Cats cat list? Answer with yes or no")
    print(listCheck)

if listCheck == "yes":
   cat_url = input("Paste your My Gamatoto cat list url here:")

   while cat_url[:35] != 'https://mygamatoto.com/comparecats/':
       print("Not a valid url, make sure it directs to a My Gamatoto Compare Cats cat list")
       cat_url = input("Either enter a valid url or type no to continue with no list")
       if cat_url == "no":
           url = 'https://mygamatoto.com/comparecats/'
           break


# url = 'https://mygamatoto.com/comparecats/?cat=001-1-Lvl30&cat=002-1-Lvl30&cat=003-1-Lvl30&cat=005-1-Lvl30&cat=006-1-Lvl30&cat=009-1-Lvl30&cat=007-1-Lvl30&cat=004-1-Lvl30&cat=008-1-Lvl30&cat=644-1-Lvl30'
driver = webdriver.Chrome()
driver.get(cat_url)

# allows for user to change list if needed and input when ready
input("Confirm your cats and press Enter to continue...")

cats = driver.find_elements("css selector", '.ant-table-body > .ant-table-fixed > tbody > tr')

cat_list = []

for cat in cats:
    Name = cat.find_element("xpath", './/td[2]/a').text
    Form = cat.find_element("xpath", './/td[3]/button/span').text
    Rarity = cat.find_element("xpath", './/td[4]').text
    Level = cat.find_element("xpath", './/td[5]/div/div/span').text
    Health = cat.find_element("xpath", './/td[6]/div').text
    Damage = cat.find_element("xpath", './/td[7]/div').text
    Range = cat.find_element("xpath", './/td[8]').text
    KB = cat.find_element("xpath", './/td[9]').text
    Speed = cat.find_element("xpath", './/td[10]').text
    DPS = cat.find_element("xpath", './/td[11]/div').text
    Target = cat.find_element("xpath", './/td[12]').text
    TBA = cat.find_element("xpath", './/td[13]').text
    Animation = cat.find_element("xpath", './/td[14]').text
    Respawn = cat.find_element("xpath", './/td[15]').text
    Cost = cat.find_element("xpath", './/td[16]').text

    type_list = cat.find_element("xpath", './/td[17]').text
    types = list(type_list.split(", "))
    for type in types:
        if type == ""


    # underline = cat.find_elements("xpath", './/td[18]/div*')
    # bold_check = False
    # for word in underline:
    #     print(word.text)
    #     if word.text.startswith("Against"):
    #         Against = list(word.text[8:].split(", "))
    #         bold_check = True


    Abilities = cat.find_element("xpath", './/td[18]').text

    cat_item = {
        'Name': Name,
        'Form': Form,
        'Rarity': Rarity,
        'Level': Level,
        'Health': Health,
        'Damage': Damage,
        'Range': Range,
        'KB': KB,
        'Speed': Speed,
        'DPS': DPS,
        'Target': Target,
        'TBA': TBA,
        'Animation': Animation,
        'Respawn': Respawn,
        'Cost': Cost,
        'Type': Type,
        'Abilities': Abilities
    }
    cat_list.append(cat_item)

cat_frame = pd.DataFrame(cat_list)
print(cat_frame)

url = 'https://mygamatoto.com/allstages/search-by-stage-name'
driver = webdriver.Chrome()
driver.get(url)

input("Open a stage and press Enter to continue...")

enemy_tables = driver.find_elements("css selector", '.ant-table-body > .ant-table-fixed > tbody')
enemies = enemy_tables[1].find_elements("xpath", './/tr')

enemy_list = []
enemy_api = 'https://onestoppress.com/api/singleenemy'
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
type_list = {"red", "floating", "black", "metal", "white", "angel", "alien", "zombie", "aku", "relic"}

for enemy in enemies:
    Name = enemy.find_element("xpath", './/td[1]/a/img').get_attribute('alt')
    Amplifier = enemy.find_element("xpath", './/td[2]/div').text
    Number = enemy.find_element("xpath", './/td[3]').text
    Base = enemy.find_element("xpath", './/td[4]').text
    Time = enemy.find_element("xpath", './/td[5]').text
    Interval = enemy.find_element("xpath", './/td[6]').text
    Boss = enemy.find_element("xpath", './/td[7]').text

    api_name = '{"compare":"' + Name + '"}'
    print(api_name)
    r = requests.post(url=enemy_api, headers=headers, data=api_name)
    data = r.json()
    print(data)
    enemy_data = data['sampledata']


    Speed = enemy_data["speed"]
    Range = enemy_data["range"]
    Target = enemy_data["att_type"]
    Ability = enemy_data["special_att_desc"]
    Type = []

    for type in type_list:
        if enemy_data[type] == True:
            Type.append(type)


    enemy_item = {
        'Name': Name,
        'Amplifier': Amplifier,
        'Number': Number,
        'Base': Base,
        'Time': Time,
        'Interval': Interval,
        'Boss': Boss,
        'Speed': Speed,
        'Range': Range,
        'Target': Target,
        'Ability': Ability,
        'Type': Type
    }
    enemy_list.append(enemy_item)

typed_cats = df[cat_frame['Type'] == 'Red']
enemy_frame = pd.DataFrame(enemy_list)
print(enemy_frame)

#cat row class:  ant-table-row editable-row ant-table-row-level-0
#name path:  //*[@id="root"]/div/div[2]/section/section/main/div[2]/div/div/div/div/div[1]/div[1]/div[2]/table/tbody/tr[2]/td[2]/a
#form path:  //*[@id="root"]/div/div[2]/section/section/main/div[2]/div/div/div/div/div[1]/div[1]/div[2]/table/tbody/tr[2]/td[3]/button/span


# url = "https://onestoppress.com/api/allenemies"
#
# resp = requests.get(url)

#print(resp.json())
# df = pd.DataFrame(resp.json())
#df = json_normalize(resp.json(), "sampledata")
# print(df)