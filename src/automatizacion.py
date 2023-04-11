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
# path = os.listdir('../gspread/')
# creds = ServiceAccountCredentials.from_json_keyfile_name(filename = '../gspread/service_account.json')
# client = gspread.authorize(creds)

from Levenshtein import distance

# importamos clusters
from probabilidades import cluster1, cluster2, cluster3, cluster4
from probabilidades_vegetarianos import cluster1_vegetariano, cluster2_vegetariano, cluster3_vegetariano, cluster4_vegetariano
from probabilidades_veganos import cluster1_vegano, cluster2_vegano, cluster3_vegano, cluster4_vegano

clusters_normal = [cluster1, cluster2, cluster3, cluster4]
clusters_vegetariano = [cluster1_vegetariano, cluster2_vegetariano, cluster3_vegetariano, cluster4_vegetariano]
clusters_vegano = [cluster1_vegano, cluster2_vegano, cluster3_vegano, cluster4_vegano]

# open second shee
# sheet = client.open('Users TUDUU').worksheet('reecomendaciones')
# client = gspread.authorize(creds)

sa = gspread.service_account(filename = '../gspread/service_account.json')
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
        load_dotenv()
        path = r'../data/cluster_2_1/' # use your path
        #save into df all files
        all_files = glob.glob(path + "/*.xlsx")

        li = dict()
        for filename in all_files:
            df = pd.read_excel(filename, index_col=None, header=0)
            print(filename)
            filename = filename.split('/')[2].split('.')[0]
            df['prob'] = 1/len(df)
            li[filename] = df

        def is_in_list(a, b):
            a = a.split(' ')
            a = [word.lower() for word in a]
            return any(i in a for i in b)

        def set_probabilities(tipo_cluster):
            for i in range(len(li['Desayuno'])):
                if is_in_list(li['Desayuno'][' Name'][i], tipo_cluster[0]):
                    li['Desayuno']['prob'][i] *= 100
            for i in range(len(li['comida_cena'] )):
                if is_in_list(li['comida_cena'][' Name'][i], tipo_cluster[1]):
                    li['comida_cena']['prob'][i] *= 100
            for i in range(len(li['entre_horas'] )):
                if is_in_list(li['entre_horas'][' Name'][i], tipo_cluster[2]):
                    li['entre_horas']['prob'][i] *= 100
            Desayuno = li['Desayuno']
            comida_cena = li['comida_cena']
            entre_horas = li['entre_horas']
            Cuidado_personal = li['Cuidado_personal']
            Hogar = li['Hogar']
            return Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar

        tipo_comprador1 = 'Como muy sano y hago deporte'

        if tipo_comprador1 == 'Como muy sano y hago deporte':
            tipo_comprador1 = '1'
        elif tipo_comprador1 == 'Dieta equilibrada, sin excesos':
            tipo_comprador1 = '2'
        elif tipo_comprador1 == 'No me quito nada, como de todo':
            tipo_comprador1 = '3'
        elif tipo_comprador1 == 'Como sano pero me gusta caer en la tentación...':
            tipo_comprador1 = '4'
        else:
            tipo_comprador1 == '4'

        # print(tipo_comprador1)

        def modelo_recomendacion(tipo_comprador, clusters):
            if tipo_comprador == '1':
                productos = [9,9,3,5,6]
                Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(clusters[0])
                df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
                lista_productos = df_cesta[' Name'].tolist()
                precio_total = df_cesta['Price'].sum()
            elif tipo_comprador == '2':
                productos = [9,9,7,5,6]
                Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(clusters[1])
                df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
                lista_productos = df_cesta[' Name'].tolist()
                precio_total = df_cesta['Price'].sum()
            elif tipo_comprador == '3':
                productos = [9,9,7,5,6]
                Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(clusters[2])
                df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
                lista_productos = df_cesta[' Name'].tolist()
                precio_total = df_cesta['Price'].sum()
            elif tipo_comprador == '4':
                productos = [9,9,7,5,6]
                Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(clusters[3])
                df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
                lista_productos = df_cesta[' Name'].tolist()
                precio_total = df_cesta['Price'].sum()
            
            return lista_productos, precio_total

        while True:
            if len(df2['vegetariano'].iloc[-1]) > 0:
                cesta = modelo_recomendacion(tipo_comprador1, clusters_vegetariano)
            else:
                cesta = modelo_recomendacion(tipo_comprador1, clusters_normal)
            print('Cesta: ', cesta[0])
            if cesta[1] > 50:
                break

        df3 = pd.read_csv('../data/Menu_Items.csv')

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

        df3 = df3[df3[' Name'].isin(cesta[0])]
        df3 = df3.groupby(' Name').apply(lambda x: x.sample(1))
        print(df3[' Name'].tolist())

        #print(cesta[0], cesta[1])
        df2 = pd.DataFrame(wks.get_all_records())
        df = pd.DataFrame(wks.get_all_records())
        
        # sheet.append_row(df3[' Name'].tolist())
        print('final')
    time.sleep(5)
