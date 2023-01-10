import gspread
import time
import pandas as pd
import os
import requests
from dotenv import load_dotenv

sa = gspread.service_account(filename = "./gspread/service_acount.json")
sh = sa.open('Users TUDUU')
wks = sh.worksheet('automatizacion')
json = wks.get_all_records()
df = pd.DataFrame(json)

load_dotenv()
AIRTABLE_BASE_ID=os.environ.get("appEX0yBBP1xhAkeL")
AIRTABLE_API_KEY=os.environ.get("keyedN52o4Usdo8DS")
AIRTABLE_TABLE_NAME=os.environ.get("Cabeceras")

while True:
    df2 = pd.DataFrame(wks.get_all_records())
    if df.equals(df2):
        print('No change')
        
    else:
        print('Change')
        # print changes
        #print(df2[~df2.isin(df)].dropna())
        #get values
        changes = df2[~df2.isin(df)].dropna()
        print(changes)
        df = df2

        # get change

        # run local script

        endpoint=f'https://api.airtable.com/v0/appEX0yBBP1xhAkeL/Cabeceras'


        headers = {
            "Authorization": f"Bearer keyedN52o4Usdo8DS ",
            "Content-Type": "application/json"
        }

        data = {
        "records": [
            {
            "fields": {
                "Cesta": changes['cesta'].values[0],
                "User": changes['user'].values[0]
            }
            }
        ]
        }
        r = requests.post(endpoint, json=data, headers=headers)
        print('llega')
        
        record_id = r.json()['records'][0]['id']
        #save record id to use in the next script
        print(record_id)
        print(r.status_code)
        os.system('python final_model.py')
        

        
    time.sleep(5)
