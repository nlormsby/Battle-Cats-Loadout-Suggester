from selenium import webdriver
import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
import time
from pandas import json_normalize

pd.set_option('display.max_colwidth', None)

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
    Types = list(type_list.split(", "))


    ability_list = cat.find_element("xpath", './/td[18]/div').text
    Immunities = ""

    loc = ability_list.find("Not affected by: ")
    # account for length of the above sub-string
    if loc > -1:
        loc += 17
        Immunities = list(ability_list[loc:].split(", "))

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
        'Types': Types,
        'Abilities': ability_list,
        'Immunities': Immunities
    }
    cat_list.append(cat_item)

cat_frame = pd.DataFrame(cat_list)
print(cat_frame)
cat_frame.to_csv('catStatList.csv')