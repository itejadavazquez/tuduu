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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import difflib
platos = pd.read_excel('../data/Platos.xlsx')
mercadona = pd.read_csv('../data/Productos_final.csv')


scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict({
  "type": "service_account",
  "project_id": "acoustic-patrol-366917",
  "private_key_id": "5a98bcecb1486d7dcd72b234da2a522a30748f00",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+YgetLH7tA+2n\n+cakLn9QZG5xall61l+LW4PomyKf0ihJbWsB2ZnFlhdzMYyQy626cYeSygDJufi/\nURni32PArr9twhCU4wyDr5/hZGpKElca+14rkpXUfCZdz8MXnqYQbpwke74ug5e9\nrkQA8LVU2A4TPH5W2jCQHw/CS30rb3wZEuyigTWrTUSyoWwvU/JwwZgeRHPRqzeu\nVP/hB7Wn1e33kTFerG0GaXcDYaoc936t/waWyPYKCLfxcSyjUPHMAr6T1cO6CBEo\nT4KZnmovIl3kRNqsOSdfKt53NulcfcaGwmp0QW0/jx9Im8/gyqm2TIg3+dAQA30G\nN0F9XhBhAgMBAAECggEAESbJvds29oL9Fr37T4oOcQXedIJ6DzjGIMrpplU1MfEz\nLSWAMQl5v5twmP5X+I99vKdC6U5TjD9TeDQfp39fZqaxNK7GfNm7pEpFMBjlm0i6\ngJuWwnwq2jRZGU7nXfbH/s3IOWBm8M/TWTfpUa0qpbsiAXxySvObOAPkXcLpQulZ\nCn1eTTWiKB7GeztMcouF7P37bKnTVEAhzTUwY3htWKDtT5xzl3q5lXsT5TFCfoXw\nOKm2T+eNBMgcf/PXJdFtz+6FFikG7J2dZATp934NPozWqRhvj1EXajNHdQT1xLAu\nLrwJbyVSRcHzcREW/adf0CzejgnJYAarzswfrn7ZxQKBgQDqnT7pUiuSZjoFAL3i\nAN7MbLxUBTwdwrnliBhPQCavC9CBu8u7DkaocUSQp5ux0W9FF86wmkX4hOlhl5ez\ntJfiaoHRkT4atzoOCapaxFP98gACa3nJ/iKRUK8cSbKlq3JpfH0RcLCo/ngELzTA\nihMAfKlT6zcMTEZ2cK4YSi5R6wKBgQDPvKQIRDArHY+PE3/YbNgA/aaan3pV/FbJ\ni5N3/8GkUikMk96lGfNx5ZS9sYNmxkEBg8pHVI/1PcqRJtGPMvrGC5PoV1qxnsUC\nte2/buS0lmXmxQx9ztSoUL2TLltpgdZd9oh1x220rSGQZtysRk2gzGDF0QjBES8l\nIcL7JKoH4wKBgEsIv3YfsY/A4g13j0MYxCjdHd5BTli2Tn36aMvv2G9jd+wGA8Jv\nbmmw0BzzffgA43VVh+Uzce1plLqBoSL4PxtKtPoxWYtxzj9vF+yvna06GIatmOXh\nQWz4QQjrCRezHYRfLCDHybhCql+sOVLa1fjx5bXRJGnqex6mKwfZsbbBAoGBAKwf\nFBZZUUPYGWOl926+OHcRs6I38ygdjVcvE8AApFRfUu2982L+zowXehd2ZnaYW7JC\nnS5e7Wx4h0efT1EEH25Kl4GSJ242K+xkCxpraooKd2Iu8HupDOBtDbZOWaVg09pE\n86oK1GY4cS/xWnRPR/Cshp5A5az6bQKqJ6DpLwybAoGANRG57EiaDjnyIoZP9BdF\n6PKa7jxi9gNDVebNsI+sScAVgd3S1dFqKxFNQH5xp+jCKL9ubkdpS8vEvyJSH8Zi\noTcKBDvurNAFpYKUHHcaBy/3ItNZnRfELUPyIiuYY578qYhzQptOMrReFKV42ZIJ\nUsaBsgRm9wApAn4CNzEtulg=\n-----END PRIVATE KEY-----\n",
  "client_email": "tuduu-822@acoustic-patrol-366917.iam.gserviceaccount.com",
  "client_id": "112907750804970910816",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tuduu-822%40acoustic-patrol-366917.iam.gserviceaccount.com"
}, scope)

sa = gspread.authorize(creds)
sh = sa.open('Users TUDUU')
wks = sh.worksheet('clientes')
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



def buscar_producto(ingrediente, df, sin_gluten=False):
    # Itera sobre los nombres de los productos en el archivo Excel
    nombres_productos = df[' Name'].tolist()
    mejores_coincidencias = process.extractOne(ingrediente, nombres_productos)

    # Establece un umbral de similitud mínima para considerar una coincidencia
    umbral_similitud = 80
    if mejores_coincidencias[1] >= umbral_similitud:
        producto_encontrado = mejores_coincidencias[0]
        return producto_encontrado
    else:
        return None

def obtener_productos_por_categoria(categoria, numero_recetas):
    # Filtra las recetas por la categoría especificada
    recetas_filtradas = platos[platos['Categoría  '] == categoria]

    # Obtiene una lista de todos los ingredientes de las recetas de la categoría
    ingredientes = []
    if numero_recetas <= 0:
        return []

    # Verifica si hay suficientes recetas disponibles
    if len(recetas_filtradas) <= numero_recetas:
        return recetas_filtradas
    # Obtiene una muestra aleatoria del número de recetas deseado
    recetas_muestra = recetas_filtradas.sample(n=numero_recetas)
    for i, receta in recetas_muestra.iterrows():
        ingredientes.extend([ingrediente.strip() for ingrediente in receta['Ingredientes '].split(',')])
    receta_completa = recetas_muestra['Platos'].tolist()
    

    # Elimina duplicados y obtiene una muestra aleatoria del número de productos deseado
    ingredientes_unicos = list(set(ingredientes))
    
    # Busca los productos correspondientes a cada ingrediente
    productos_encontrados = []
    for ingrediente in ingredientes_unicos:
        producto = buscar_producto(ingrediente, mercadona)
        if producto:
            productos_encontrados.append(producto)

    return productos_encontrados, receta_completa

def precio_cesta(cesta, df):
    precio_total = 0
    for producto in cesta:
        precio = df.loc[df[' Name'] == producto, 'Price'].iloc[0]
        precio_total += precio
    return precio_total



wks_final = sh.worksheet('clientes')
json_final = wks_final.get_all_records()
df_final = pd.DataFrame(json_final)


i = 2
for _, _ in df_final.iterrows():
    tipo_consumidor = _['tipo cliente']
    print(tipo_consumidor)
    if tipo_consumidor == 'sin restricciones':
        cesta_pasta = obtener_productos_por_categoria('Pasta ', 2)
        cesta_verdura = obtener_productos_por_categoria('Verduras ', 1)
        cesta_carne = obtener_productos_por_categoria('Carne ', 3)
        cesta_pescado = obtener_productos_por_categoria('Pescado', 1)
        cesta_legumbres = obtener_productos_por_categoria('Legumbres ', 1)
        cesta_ensaladas = obtener_productos_por_categoria('Ensaladas', 1)
        cesta_pure = obtener_productos_por_categoria('Purés', 1)
        cesta_desayuno = obtener_productos_por_categoria('Desayunos ', 4)
        cesta_bebidas = obtener_productos_por_categoria('Bebidas ', 1)
        cesta_alcohol = obtener_productos_por_categoria('Alcohol ', 1)
        cesta1 = cesta_pasta[0] + cesta_verdura[0] + cesta_carne[0] + cesta_pescado[0] + cesta_legumbres[0] + cesta_ensaladas[0] + cesta_pure[0] + cesta_desayuno[0] + cesta_bebidas[0] + cesta_alcohol[0]
        cesta2 = cesta_pasta[1] + cesta_verdura[1] + cesta_carne[1] + cesta_pescado[1] + cesta_legumbres[1] + cesta_ensaladas[1] + cesta_pure[1] + cesta_desayuno[1] + cesta_bebidas[1] + cesta_alcohol[1]
    elif tipo_consumidor == 'Como sano pero me gusta caer en la tentación…':
        cesta_pasta = obtener_productos_por_categoria('Pasta ', 2)
        cesta_verdura = obtener_productos_por_categoria('Verduras ', 2) 
        cesta_carne = obtener_productos_por_categoria('Carne ', 1) 
        cesta_pescado = obtener_productos_por_categoria('Pescado', 1)
        cesta_legumbres = obtener_productos_por_categoria('Legumbres ', 1)
        cesta_ensaladas = obtener_productos_por_categoria('Ensaladas', 1)
        cesta_pure = obtener_productos_por_categoria('Purés', 1)
        cesta_desayuno = obtener_productos_por_categoria('Desayunos ', 4)
        cesta1 = cesta_pasta[0] + cesta_verdura[0] + cesta_carne[0] + cesta_pescado[0] + cesta_legumbres[0] + cesta_ensaladas[0] + cesta_pure[0] + cesta_desayuno[0]
        cesta2 = cesta_pasta[1] + cesta_verdura[1] + cesta_carne[1] + cesta_pescado[1] + cesta_legumbres[1] + cesta_ensaladas[1] + cesta_pure[1] + cesta_desayuno[1]
    elif tipo_consumidor == 'Dieta equilibrada, sin excesos':
        cesta_pasta = obtener_productos_por_categoria('Pasta ', 1)
        cesta_verdura = obtener_productos_por_categoria('Verduras ', 3) 
        cesta_carne = obtener_productos_por_categoria('Carne ', 1) 
        cesta_pescado = obtener_productos_por_categoria('Pescado', 1)
        cesta_legumbres = obtener_productos_por_categoria('Legumbres ', 1)
        cesta_ensaladas = obtener_productos_por_categoria('Ensaladas', 2)
        cesta_pure = obtener_productos_por_categoria('Purés', 2)
        cesta_desayuno = obtener_productos_por_categoria('Desayunos ', 4)
        cesta1 = cesta_pasta[0] + cesta_verdura[0] + cesta_carne[0] + cesta_pescado[0] + cesta_legumbres[0] + cesta_ensaladas[0] + cesta_pure[0] + cesta_desayuno[0]
        cesta2 = cesta_pasta[1] + cesta_verdura[1] + cesta_carne[1] + cesta_pescado[1] + cesta_legumbres[1] + cesta_ensaladas[1] + cesta_pure[1] + cesta_desayuno[1]
    elif tipo_consumidor == 'Como sano y deporte':
        cesta_pasta = obtener_productos_por_categoria('Pasta ', 3)
        cesta_verdura = obtener_productos_por_categoria('Verduras ', 2) 
        cesta_carne = obtener_productos_por_categoria('Carne ', 2) 
        cesta_pescado = obtener_productos_por_categoria('Pescado', 3)
        cesta_legumbres = obtener_productos_por_categoria('Legumbres ', 1)
        cesta_ensaladas = obtener_productos_por_categoria('Ensaladas', 1)
        cesta_desayuno = obtener_productos_por_categoria('Desayunos ', 4)
        cesta1 = cesta_pasta[0] + cesta_verdura[0] + cesta_carne[0] + cesta_pescado[0] + cesta_legumbres[0] + cesta_ensaladas[0] + cesta_desayuno[0]
        cesta2 = cesta_pasta[1] + cesta_verdura[1] + cesta_carne[1] + cesta_pescado[1] + cesta_legumbres[1] + cesta_ensaladas[1] + cesta_desayuno[1]
      
lista_productos_cambiados = []

for producto in cesta1:
    productos_similares = difflib.get_close_matches(producto, mercadona[' Name'])
    
    if len(productos_similares) > 0:
        producto_similar_mas_caro = None
        precio_original = mercadona[mercadona[' Name'] == producto]['Price'].iloc[0]
        
        for prod_similar in productos_similares:
            precio_similar = mercadona[mercadona[' Name'] == prod_similar]['Price'].iloc[0]
            if precio_similar > precio_original:
                if producto_similar_mas_caro is None or precio_similar > mercadona[mercadona[' Name'] == producto_similar_mas_caro]['Price'].iloc[0]:
                    producto_similar_mas_caro = prod_similar
        
        if producto_similar_mas_caro is not None:
            lista_productos_cambiados.append(producto_similar_mas_caro)
        else:
            lista_productos_cambiados.append(producto)
    else:
        lista_productos_cambiados.append(producto)

    valor = ", ".join(cesta1)
    valor_premium = ", ".join(lista_productos_cambiados)
    precio = precio_cesta(cesta1, mercadona)
    #print(cesta1)
    valor2 = ", ".join(cesta2)
    #print(valor)
    print(mercadona.head())
    wks_final.update_cell(i,4 , valor) # Actualiza la celda correspondiente con el resultado
    
    wks_final.update_cell(i,6 , precio)
    wks_final.update_cell(i,7 , valor_premium)
    wks_final.update_cell(i,5 ,valor2)
    # cesta_premium = recomendar_cesta_mas_cara(df3, cesta, len(cesta))
    # cesta_premium = cesta_premium[' Name'].tolist()
    # valor2 = ", ".join(cesta_premium)
    # wks_final.update_cell(i,5 , valor2) # Actualiza la celda correspondiente con el resultado
    i += 1
