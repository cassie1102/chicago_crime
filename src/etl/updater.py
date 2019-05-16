# -*- coding: utf-8 -*-
"""
Created on Thu May 16 12:38:30 2019

@author: andyj
"""

import requests
import os 
import sys
import pandas as pd
import json
from pandas.io.json import json_normalize 


# setwd
os.chdir('E:/projects/chi_crime/src/etl/')

URL = "https://data.cityofchicago.org/resource/ijzp-q8t2.json?"

API_TOKEN = os.environ.get("CHI_API_TOKEN")
if not API_TOKEN:
    print("You need to get an City of Chicago API token! Exiting..")
    sys.exit(1)

# pull in last update date
txt_file = open("last_update.txt", "r")
last_update_datetime = txt_file.read()

# set parameters
param = {'$$app_token' : API_TOKEN,
         '$limit' : '1000000',
         '$where' : "date > " + last_update_datetime}
  
# API call 
response = requests.get(URL, params = param)
data = json.loads(response.text)

# set to df
df = json_normalize(data)

# bring in old df
df_old = pd.read_csv('../../data/interim/aggregate_data.csv')

# update working df
df = pd.concat([df_old, df])     
df = df.reset_index(drop=True)   

# write out old file:
upload_dir = 'E:/projects/chi_crime/data/interim/'
upload_file = 'BACKUP-previous_version'
df_old.to_csv(upload_dir + upload_file + '.csv', index = False)

# write out new file
upload_file = 'aggregate_data'
df.to_csv(upload_dir + upload_file + '.csv', index = False)

# update last update txt file
with open('last_update.txt', 'w') as f:
    f.write(max(df.iloc[:, 5]))