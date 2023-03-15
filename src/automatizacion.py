import gspread
import time
import pandas as pd
import os
import requests
import os
import requests
import glob
from Levenshtein import distance
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
creds = ServiceAccountCredentials.from_json_keyfile_name('gspread/service_account.json')
client = gspread.authorize(creds)
# open second shee
sheet = client.open('Users TUDUU').worksheet('reecomendaciones')
client = gspread.authorize(creds)

sa = gspread.service_account()
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
        path = r'cluster_2_1/' # use your path
        #save into df all files
        all_files = glob.glob(path + "/*.xlsx")

        li = dict()
        for filename in all_files:
            df = pd.read_excel(filename, index_col=None, header=0)
            filename = filename.split('\\')[1].split('.')[0]
            df['prob'] = 1/len(df)
            li[filename] = df



        def is_in_list(a, b):
            a = a.split(' ')
            a = [word.lower() for word in a]
            return any(i in a for i in b)


        def set_probabilities(tipo_cluster):
            for i in range(len(li['Desayuno'] )):
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


        print('holaa')
            
        probx3_2_1_desayuno = ['cereales', 'pan', 'tostada', 'palitos', 'baguette', 'hogaza', 'baguettes', 'panadería', 'cereales','aceite',  'tostadas','galletas','tortitas', 'leche', 'cerezas', 'manzana', 'plátano', 'fresa', 'higos', 'paraguayo', 'nectarina','manzana', 'aguacates', 'mango', 'aguacate',  'limón', 'melón', 'sandía', 'kiwis', 'bífidus', 'queso', 'yogur', 'mantequilla']
        probx3_2_1_comida_cena = ['huevo','huevos','tortiglioni','helice','tallarín','cannelloni','fusilli','pasta', 'macarrón', 'tallarines', 'garbanzos', 'lentejas', 'alubias','albóndigas','entrecot','burguer','solomillo','salchichas','bacalao','mejillones','almejas', 'bonito','langostino','atún', 'rodaballo', 'rape', 'merluza','gallo', 'dorada', 'lubina','lenguado', 'calamar','sepia','gambón','filete','cebolla', 'ajo','zanahoria', 'albahaca', 'calabaza','salmorejo','sopa', 'gazpacho', 'patatas', 'patata', 'arroz', 'tomate', 'pollo,','proteínas', 'pollo', 'salmón','arroz','tiramisú','mousse','flan', 'helado','ensalada','champiñones','pimientos', 'espinacas','cebolla','lechuga', 'iceberg','zanahoria', 'brócoli', 'berenjena','berenjenas', 'coliflor', 'pepino','alcachofa','tomate', 'puerro', 'calabaza', 'calabacín','pimiento','patata', 'remolacha', 'zanahoria', 'cebolla', 'ajo','ajos','puerro','espárrago','canónigos', 'coliflor','champiñón', 'seta','zanahorias', 'tomates']
        probx3_2_1_entre_horas = [ 'chocolate', 'galletas','cheesecake', 'copa','brownie','cacao', 'choco', 'berlina', 'gofres', 'sobaos', 'croissant','snack','chocolate', 'pizza', 'tarta', 'hamburguesa','mayonesa', 'nata', 'paté','nachos','york','quesos','morcilla', 'ibéricos', 'ibérico','jamón', 'chorizo','paletilla', 'ibérica', 'salchichón', 'longaniza','paleta','lonchas', 'pavo', 'fiambre','lonchas']
        cluster1 = [probx3_2_1_desayuno, probx3_2_1_comida_cena, probx3_2_1_entre_horas]

        prob_3_2_2_desayuno = ['cereales','pan', 'tostada', 'palitos', 'baguette','hogaza','baguettes', 'panadería','cereales','aceite',  'tostadas','galletas','leche','cerezas','albaricoque', 'manzana', 'plátano', 'fresa','uvas','ciruela', 'higos', 'paraguayo','naranja', 'mandarina', 'uva', 'peras', 'pera', 'piña','manzanas', 'manzana', 'banana', 'ciruelas', 'paraguayos', 'frambuesas', 'aguacates', 'mango', 'aguacate','limón', 'melón', 'sandía', 'kiwis','bífidus','yogur','cereales', 'pan', 'tostada', 'palitos', 'baguette', 'hogaza', 'baguettes', 'panadería', 'cereales','aceite',  'tostadas','galletas','tortitas', 'leche', 'cerezas', 'manzana', 'plátano', 'fresa', 'higos', 'paraguayo', 'nectarina','manzana', 'aguacates', 'mango', 'aguacate',  'limón', 'melón', 'sandía', 'kiwis', 'bífidus', 'queso', 'yogur', 'mantequilla','zumo','leche']
        prob_3_2_2_comida_cena = ['huevo','huevos','tortiglioni','helice','tallarín','cannelloni','fusilli','pasta', 'spaghetti','macarrón', 'tallarines','garbanzo','legumbre', 'garbanzos', 'lentejas', 'alubias', 'lenteja', 'alubia', 'lomo', 'cerdo', 'pollo', 'pechuga','solomillo', 'bonito', 'atún', 'rodaballo', 'rape', 'merluza','gallo', 'dorada', 'lubina','lenguado', 'calamar','filete','cebolla', 'ajo', 'espinaca', 'alcachofa', 'zanahoria', 'albahaca', 'calabaza', 'remolacha', 'salmorejo','sopa', 'gazpacho','patatas', 'patata', 'arroz', 'tomate','pollo,','proteínas', 'pollo', 'salmón','arroz','tiramisú','mousse', 'flan', 'helado','ensalada','alcachofas','champiñones','alcachofa','verduras','verdura', 'pimientos', 'espinacas', 'cebolla','haba', 'rollitos', 'rodajas', 'lechuga', 'iceberg', 'zanahoria', 'brócoli', 'berenjena','judía','berenjenas', 'coliflor', 'pepino', 'escarola', 'alcachofa', 'tomate', 'puerro', 'calabaza', 'calabacín', 'pimiento', 'patata', 'remolacha', 'zanahoria', 'cebolla', 'ajo','ajos','puerro', 'maíz','remolacha', 'espárrago', 'puerro', 'espinaca','rúcula', 'lechuga', 'canónigos', 'coliflor', 'brócoli', 'alcachofa','acelgas','champiñón', 'seta', 'zanahorias', 'tomates', 'cebollas', 'batata', 'lechugas']
        prob_3_2_2_entre_horas =  ['chocolate', 'galletas','cheesecake', 'copa','brownie','cacao', 'choco', 'berlina', 'trenza', 'napolitana', 'palmeritas', 'mantecadas','gofres', 'sobaos','croissant','snack','chocolate', 'pizza', 'tarta', 'hamburguesa','mayonesa', 'nata','paté','nachos','york','quesos','morcilla', 'ibéricos', 'ibérico','jamón', 'chorizo','chistorra', 'paletilla', 'ibérica', 'salchichón', 'longaniza','paleta','lonchas', 'pavo', 'fiambre','lonchas']
        cluster2 = [prob_3_2_2_desayuno, prob_3_2_2_comida_cena, prob_3_2_2_entre_horas]

        prob_3_2_3_desayuno = ['cereales','pan', 'tostada', 'palitos','baguette','hogaza', 'baguettes', 'panadería','cereales','aceite',  'tostadas','leche','cerezas','albaricoque','manzana', 'plátano', 'fresa','uvas','ciruela', 'higos', 'paraguayo', 'arándanos', 'nectarina', 'melocotón', 'naranja', 'mandarina', 'uva', 'peras', 'pera', 'piña','manzanas', 'manzana', 'banana', 'ciruelas', 'paraguayos', 'frambuesas', 'aguacates', 'mango', 'aguacate', 'limón', 'melón', 'sandía', 'kiwis','bífidus','yogur','cereales', 'pan', 'tostada', 'palitos', 'baguette', 'hogaza', 'baguettes', 'panadería', 'cereales','aceite',  'tostadas','galletas','tortitas', 'leche', 'cerezas', 'manzana', 'plátano', 'fresa', 'higos', 'paraguayo', 'nectarina','manzana', 'aguacates', 'mango', 'aguacate',  'limón', 'melón', 'sandía', 'kiwis', 'bífidus', 'queso', 'yogur', 'zumo','leche']
        prob_3_2_3_comida_cena = ['huevo','huevos','tortiglioni','helice','tallarín','cannelloni','fusilli','pasta', 'spaghetti', 'macarrón', 'tallarines', 'garbanzo','legumbre', 'garbanzos', 'lentejas', 'alubias', 'lenteja', 'alubia','pollo','pechuga','bonito', 'atún', 'rodaballo', 'rape', 'merluza','gallo', 'dorada', 'lubina', 'lenguado', 'calamar','filete','cebolla', 'ajo', 'espinaca', 'alcachofa', 'zanahoria', 'albahaca', 'calabaza', 'remolacha','salmorejo','sopa', 'gazpacho', 'patatas', 'patata', 'arroz', 'tomate','pollo,','proteínas', 'pollo', 'integrales','tiramisú','mousse', 'flan', 'helado','ensalada','alcachofas','champiñones','alcachofa','verduras','verdura', 'pimientos', 'espinacas', 'cebolla','haba', 'rollitos', 'rodajas', 'lechuga', 'iceberg','zanahoria', 'brócoli', 'berenjena','judía','berenjenas', 'coliflor', 'pepino', 'escarola', 'alcachofa', 'tomate', 'puerro', 'calabaza', 'calabacín','pimiento','patata', 'remolacha', 'zanahoria', 'cebolla', 'ajo','ajos','puerro','maíz','remolacha','espárrago', 'puerro','espinaca','rúcula', 'lechuga', 'canónigos', 'coliflor', 'brócoli', 'alcachofa','acelgas','champiñón', 'seta','zanahorias', 'tomates', 'cebollas', 'batata', 'lechugas']
        prob_3_2_3_entre_horas = ['york','quesos','ibéricos', 'ibérico','jamón','paletilla', 'ibérica','paleta', 'lonchas', 'pavo','lonchas']
        cluster3 = [prob_3_2_3_desayuno, prob_3_2_3_comida_cena, prob_3_2_3_entre_horas]

        prob_3_2_4_desayuno = ['cereales','pan', 'tostada', 'palitos','baguette','hogaza','baguettes', 'panadería','cereales','aceite',  'tostadas', 'leche','muesli','cerezas','albaricoque','manzana', 'plátano', 'fresa','uvas','ciruela', 'higos', 'paraguayo', 'arándanos', 'nectarina', 'melocotón', 'naranja', 'mandarina', 'uva', 'peras', 'pera', 'piña', 'manzanas', 'manzana', 'banana', 'ciruelas', 'paraguayos', 'frambuesas','aguacates', 'mango', 'aguacate', 'limón', 'melón', 'sandía', 'kiwis','bífidus','yogur','kéfir','cereales', 'pan', 'tostada', 'palitos', 'baguette', 'hogaza', 'baguettes', 'panadería', 'cereales','aceite',  'tostadas','galletas','tortitas', 'leche', 'cerezas', 'manzana', 'plátano', 'fresa', 'higos', 'paraguayo', 'nectarina','manzana', 'aguacates', 'mango', 'aguacate',  'limón', 'melón', 'sandía', 'kiwis', 'bífidus', 'queso', 'yogur','zumo','leche']
        prob_3_2_4_comida_cena = ['huevo','huevos','tortiglioni','helice','tallarín','cannelloni','fusilli','pasta', 'spaghetti', 'macarrón', 'tallarines','garbanzo','legumbre', 'garbanzos', 'lentejas', 'alubias', 'lenteja', 'alubia','pollo','pechuga','bonito', 'atún', 'rodaballo', 'rape', 'merluza','gallo', 'dorada', 'lubina', 'lenguado', 'calamar','filete','cebolla', 'ajo', 'espinaca', 'alcachofa', 'zanahoria', 'albahaca', 'calabaza', 'remolacha','salmorejo','sopa', 'gazpacho','patatas', 'patata', 'arroz', 'tomate', 'mozzarella','pollo','proteínas', 'pollo', 'salmón', 'desnatada',  'desnatada', 'desnatada','avena','arroz','0%','integrales','avena','ensalada','alcachofas','champiñones','alcachofa','verduras','verdura', 'pimientos', 'espinacas', 'cebolla','haba', 'rollitos', 'rodajas', 'lechuga', 'iceberg','zanahoria', 'brócoli', 'berenjena','judía','berenjenas', 'coliflor', 'pepino', 'escarola', 'alcachofa','tomate', 'puerro', 'calabaza', 'calabacín','pimiento','patata', 'remolacha', 'zanahoria', 'cebolla', 'ajo','ajos','puerro','maíz','espárrago','puerro','espinaca','rúcula', 'lechuga', 'canónigos', 'coliflor', 'brócoli', 'alcachofa','acelgas','champiñón', 'seta', 'zanahorias', 'tomates', 'cebollas', 'batata', 'lechugas']
        prob_3_2_4_entre_horas = ['york','lonchas', 'lonchas''lonchas','pavo', 'pavo','pavo','lonchas']
        cluster4 = [prob_3_2_4_desayuno, prob_3_2_4_comida_cena, prob_3_2_4_entre_horas]

        lista_carne = ["Albóndigas", "Entrecot", "Burguer", "Solomillo", "Salchichas", "Filete", "Pollo", "Ibéricos", "Ibérico", "Jamón", "Chorizo", "Paletilla", "Ibérica", "Salchichón", "Longaniza", "Paleta", "Pavo", "Fiambre", "Lonchas"]
        lista_pescado = ["Bacalao", "Mejillones", "Almejas", "Bonito", "Langostino", "Atún", "Rodaballo", "Rape", "Merluza", "Gallo", "Dorada", "Lubina", "Lenguado", "Calamar", "Sepia", "Gambón", "Salmón"]
        lista_veganos = ["Queso", "Leche", "Nata", "Mantequilla", "Yogur", "Huevos", "Miel"]

        def modelo_recomendacion(tipo_comprador):
            
            if tipo_comprador == '1':
                productos = [9,9,3,5,6]
                Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(cluster1)
                df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
                lista_productos = df_cesta[' Name'].tolist()
                precio_total = df_cesta['Price'].sum()
            elif tipo_comprador == '2':
                productos = [9,9,7,5,6]
                Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(cluster2)
                df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
                lista_productos = df_cesta[' Name'].tolist()
                precio_total = df_cesta['Price'].sum()
            elif tipo_comprador == '3':
                productos = [9,9,7,5,6]
                Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(cluster3)
                df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
                lista_productos = df_cesta[' Name'].tolist()
                precio_total = df_cesta['Price'].sum()
            elif tipo_comprador == '4':
                productos = [9,9,7,5,6]
                Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(cluster4)
                df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
                lista_productos = df_cesta[' Name'].tolist()
                precio_total = df_cesta['Price'].sum()
            return lista_productos, precio_total


        print('holaaaaa')
        tipo_comprador1 = '1'
        while True:
            cesta = modelo_recomendacion(tipo_comprador1)
            if cesta[1] > 50:
                break
        print('final')

        df3 = pd.read_csv('Menu_Items.csv')


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


        ## Vegetarianismo
        print(df2['vegetariano'].iloc[-1])

        max_distance = 2
        if len(df2['vegetariano'].iloc[-1]) > 0:
            try:
                productos_list = df3[' Name']
                productos_vegetarianos = [producto for producto in productos_list 
                                        if all(
                                                distance(x.lower(), prod.lower())>max_distance
                                                for prod in lista_carne+lista_pescado
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
                                                for prod in lista_pescado+lista_carne+lista_veganos
                                                for x in producto.split()
                                            )]
            except:
                pass
        

        #print(cesta[0], cesta[1])
        df2 = pd.DataFrame(wks.get_all_records())
        df = pd.DataFrame(wks.get_all_records())
        
        sheet.append_row(df3[' Name'].tolist())
        print('final')
    time.sleep(5)

    