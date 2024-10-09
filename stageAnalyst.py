from selenium import webdriver
import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
import time
from pandas import json_normalize

cat_frame = pd.read_csv('catStatList.csv')
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
        if enemy_data[type]:
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

enemy_frame = pd.DataFrame(enemy_list)
print(enemy_frame)