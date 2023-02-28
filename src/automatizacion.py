!pip install python-Levenshtein

import pandas as pd
import numpy as np

import os
import glob
import time
import requests
from sys import platform

from Levenshtein import distance

import gspread
from dotenv import load_dotenv

from probabilidades import *
from funciones import *

sa = gspread.service_account(filename = "./gspread/service_account.json")
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

while True: # Esto tiene que ser que se ejecute cuando detecte un cambio, no que esté siempre ejecutándose
    df2 = pd.DataFrame(wks.get_all_records())
    if df.equals(df2):
        print('No change')
        
    else:
        df = df2
        print('cambios efectuados')
        load_dotenv()
        path = r'cluster_2_1/' # use your path
        #save into df all files
        all_files = glob.glob(path + "/*.xlsx")

        li = dict()
        for filename in all_files:
            df = pd.read_excel(filename, index_col=None, header=0)
            if platform =='darwin':
                filename = filename.split('/')[1].split('.')[0] # mac
            elif platform == 'win32':
                filename = filename.split('\\')[1].split('.')[0] # windows
            df['prob'] = 1/len(df)
            li[filename] = df

        # Segmento de cliente
        tipo_comprador1 = '1'
        while True:
            cesta = modelo_recomendacion(tipo_comprador1)
            if cesta[1] > 50:
                break

        # Cesta recomendada
        df3 = pd.read_csv('Menu_Items.csv')

        # Restricciones sobre la cesta recomendada
        ## Celiaquía
        print(df2['celiaco'].iloc[-1])
        if len(df2['celiaco'].iloc[-1]) > 0:
            for i in range(len(df3)):
                # si exiten productos sin gluten, cambiarlos por los sin gluten
                try:
                    df3[' Name'].iloc[i] = df3[df3[' Name'].str.contains('gluten') & df3[' Name'].str.contains(df3[' Name'].iloc[i])][' Name'].iloc[0]
                except:
                    pass
        ## Lactosa
        print(df2['intolerante'].iloc[-1])
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
                productos_list = df3[' Name']
                productos_vegetarianos = [producto for producto in productos_list 
                                          if all(
                                                distance(x.lower(), prod.lower())>max_distance
                                                for prod in productos_carne+productos_pescado
                                                for x in producto.split()
                                            )]
            except:
                pass


        ## Veganismo
        print(df2['vegano'].iloc[-1])

        max_distance=2
        if len(df2['vegano'].iloc[-1]) > 0:
            try:
                productos_list = df3[' Name']
                productos_veganos = [producto for producto in productos_list 
                                          if all(
                                                distance(x.lower(), prod.lower())>max_distance
                                                for prod in productos_carne+productos_pescado+productos_huevos
                                                for x in producto.split()
                                            )]
            except:
                pass

        df3 = df3[df3[' Name'].isin(cesta[0])]
        df3 = df3.groupby(' Name').apply(lambda x: x.sample(1))
        print(df3[' Name'].tolist())
        

        #print(cesta[0], cesta[1])
        df2 = pd.DataFrame(wks.get_all_records())
        df = pd.DataFrame(wks.get_all_records())
                
    time.sleep(5) # Esti tiene que ser cada vez que detecte un cambio, no cada 5 segundos

    