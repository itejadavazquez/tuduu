from probabilidades import cluster1, cluster2, cluster3, cluster4

def is_in_list(a, b):
    a = a.split(' ')
    a = [word.lower() for word in a]
    return any(i in a for i in b)

def set_probabilities(li, tipo_cluster):
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

def clusters(tipo_comprador):
    if tipo_comprador== '1':
        return cluster1
    elif tipo_comprador=='2':
        return cluster2
    elif tipo_comprador=='3':
        return cluster3
    else:
        return cluster4

def modelo_recomendacion(tipo_comprador, li):
    lista_productos = []
    precio_total = 0
    if tipo_comprador == '1':
        # print('modelo de recomendacion')
        productos = [9,9,3,5,6]
        Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(li, clusters(tipo_comprador))
        # print('probabilidades asignadas')
        df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
        # print('cesta lista')
        lista_productos = df_cesta[' Name'].tolist()
        precio_total = df_cesta['Price'].sum()
    elif tipo_comprador == '2':
        productos = [9,9,7,5,6]
        Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(li, clusters(tipo_comprador))
        df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
        lista_productos = df_cesta[' Name'].tolist()
        precio_total = df_cesta['Price'].sum()
    elif tipo_comprador == '3':
        productos = [9,9,7,5,6]
        Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(li, clusters(tipo_comprador))
        df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
        lista_productos = df_cesta[' Name'].tolist()
        precio_total = df_cesta['Price'].sum()
    elif tipo_comprador == '4':
        productos = [9,9,7,5,6]
        Desayuno, comida_cena, entre_horas, Cuidado_personal, Hogar = set_probabilities(li, clusters(tipo_comprador))
        df_cesta = Desayuno.sample(n=productos[0], weights = Desayuno.prob).append(comida_cena.sample(n=productos[1], weights = comida_cena.prob)).append(entre_horas.sample(n=productos[2], weights = entre_horas.prob))#.append(Hogar.sample(n=productos[3])).append(Cuidado_personal.sample(n=productos[4]))
        lista_productos = df_cesta[' Name'].tolist()
        precio_total = df_cesta['Price'].sum()
    return lista_productos, precio_total