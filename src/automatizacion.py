
# !pip install python-Levenshtein

import pandas as pd
import numpy as np

import os
import glob
import time
import requests
from sys import platform

from Levenshtein import distance

import gspread
import time
import pandas as pd
import os
import requests
import os
import requests
import glob
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
creds = ServiceAccountCredentials.from_json_keyfile_name('../gspread/service_account.json')
client = gspread.authorize(creds)
# open second shee
sheet = client.open('Users TUDUU').worksheet('reecomendaciones')
client = gspread.authorize(creds)

from probabilidades import *
from funciones import *

sa = gspread.service_account(filename = "./../gspread/service_account.json")
sh = sa.open('Users TUDUU')
wks = sh.worksheet('automatizacion')
wks2 = sh.worksheet('productos')
json = wks.get_all_records()
json2 = wks2.get_all_records()
df = pd.DataFrame(json)
df_prod = pd.DataFrame(json2)

load_dotenv()
AIRTABLE_BASE_ID=os.environ.get("appEX0yBBP1xhAkeL")
AIRTABLE_API_KEY=os.environ.get("keyedN52o4Usdo8DS")
AIRTABLE_TABLE_NAME=os.environ.get("Cabeceras")
AIRTABLE_TABLE_NAME2=os.environ.get("Users")

import warnings

warnings.filterwarnings("ignore")

while True:
    df2 = pd.DataFrame(wks.get_all_records())
    if df.equals(df2):
        print('No change')
        
    else:
        df = df2
        print('cambios efectuados')
        print('hola')
        load_dotenv()
        print('holaa')
        path = '../cluster_2_1/' # use your path
        #save into df all files
        all_files = glob.glob(path + "/*.xlsx")
        print('All files')

        li = dict()
        for filename in all_files:
            df = pd.read_excel(filename, index_col=None, header=0)
            print('ok')
            filename = filename.split('/')[1].split('.')[0]
            print('split hecho')
            # if platform =='darwin':
            #     filename = filename.split('/')[1].split('.')[0] # mac
            # elif platform == 'win32':
            #     filename = filename.split('\\')[1].split('.')[0] # windows
            df['prob'] = 1/len(df)
            li[filename] = df
            print(filename)
            print('filename')

        # Segmento de cliente
        tipo_comprador1 = '1' # poner el segmento real del cliente
        
        # print(tipo_comprador1)
        while True:
            cesta = modelo_recomendacion(tipo_comprador1, li)
            if cesta[1] > 50:
                # print(len(cesta[1]))
                break
        print('final')


        # Cesta recomendada
        df3 = pd.read_csv('../Menu_Items.csv')

        #### CELIACOS
        
        if len(df2['celiaco'].iloc[-1]) > 0:
            for i in range(len(df3)):
                # si exiten productos sin gluten, cambiarlos por los sin gluten
                try:
                    df3[' Name'].iloc[i] = df3[df3[' Name'].str.contains('gluten') & df3[' Name'].str.contains(df3[' Name'].iloc[i])][' Name'].iloc[0]
                except:
                    pass

        #### LACTOSA
        
        if len(df2['intolerante'].iloc[-1]) > 0:
            for i in range(len(df3)):
                try:
                    df3[' Name'].iloc[i] = df3[df3[' Name'].str.contains('lactosa') & df3[' Name'].str.contains(df3[' Name'].iloc[i])][' Name'].iloc[0]
                except:
                    pass

        ## Vegetarianismo
        print(df2['vegetariano'].iloc[-1])

        max_distance = 2
        if len(df2['vegetariano'].iloc[-1]) > 0:
            try:
                productos_list = cesta
                productos_vegetarianos = [producto for producto in productos_list 
                                        if all(
                                                distance(x.lower(), prod.lower())>max_distance
                                                for prod in lista_carne+lista_pescado
                                                for x in producto.split()
                                            )]
                df3[' Name'] = productos_vegetarianos

            except:
                pass


        ## Veganismo
        print(df2['vegano'].iloc[-1])

        max_distance=2
        if len(df2['vegano'].iloc[-1]) > 0:
            try:
                # productos_list = df3[' Name']
                productos_list = cesta
                productos_veganos = [producto for producto in productos_list 
                                        if all(
                                                distance(x.lower(), prod.lower())>max_distance
                                                for prod in lista_pescado+lista_carne+lista_veganos
                                                for x in producto.split()
                                            )]
                df3[' Name'] = productos_veganos
            except:
                pass

        df3 = df3[df3[' Name'].isin(cesta[0])]
        df3 = df3.groupby(' Name').apply(lambda x: x.sample(1))
        print(df3[' Name'].tolist())
        

        #print(cesta[0], cesta[1])
        df2 = pd.DataFrame(wks.get_all_records())
        df = pd.DataFrame(wks.get_all_records())
                    
    time.sleep(5) # Esti tiene que ser cada vez que detecte un cambio, no cada 5 segundos

    