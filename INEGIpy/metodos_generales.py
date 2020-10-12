# -*- coding: utf-8 -*-
#### funciones generales
import pandas as pd
import requests 
import json

liga_base = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'

with open('localidades_INEGI.txt','r') as file:
       localidades_dict = json.loads(file.read())

## FUNCIONES

def obtener_json(token,indicador,banco,localidad):
    """ 

    Construye la liga de consulta y obtiene la información resultante del API del
    INEGI. Esta función es principalmente para uso interno como en indicador_a_df().
    
    Parámetros:
    ------------
    token: str. Token para acceder al API. 
    
    indicadores: str.  Número del indicador a buscar.
    
    banco: str. Banco de información donde se encuentra el indocador. Puede ser 
                'BIE' o 'BISE'.
    
    localidades: str o lista. Nombre, número o lísta de la entidad geográfica de 
                            la búsqueda, donde el 'Total Nacional' es el '0700' 
                            y los estados están ordenados alfabeticamente:
                                * 'Aguascalienes':'07000001'
                                * 'Baja California':'0700002'
                                * Resto de los estados
                            Un diccionario con los nombres y números de las 
                            entidades geográficas se encuentra en INEGI.localidades_dict
   -------------

    Regresa un diccionario con la información del indicador proporcionada por el API
    del INEGI en formato JSON. 

    Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

    """
    global liga_base, localidades_dict
    if localidad.isdigit() is False: localidad = localidades_dict[localidad]
    print(localidad)
    indicador = indicador + '/'
    idioma = 'es/'
    banco = banco + '/2.0/'
    final_liga = str(token) + '?type=json'
    liga_api = liga_base + indicador + idioma + localidad + '/false/' + banco + final_liga
    print(liga_api)
    req = requests.get(liga_api)
    data = json.loads(req.text)
    return data

def indicador_a_df(token,indicador,banco,localidad):
    """ 
    
    Construye un DataFrame con la información resultante del API del INEGI de 
    un solo indicador a la vez.

    Parámetros:
    -----------
    token: str. Token para acceder al API.
    
    indicadores: str o  lista. Número o lista con los números de los indicadores
                                a buscar.
    
    banco: str. Banco de información donde se encuentra el indocador. Puede ser 
                'BIE' o 'BISE'.
    
    localidades: str o lista. Nombre, número o lísta de la entidad geográfica de 
                            la búsqueda, donde el 'Total Nacional' es el '0700' 
                            y los estados están ordenados alfabeticamente:
                                * 'Aguascalienes':'07000001'
                                * 'Baja California':'0700002'
                                * Resto de los estados
                            Un diccionario con los nombres y números de las 
                            entidades geográficas se encuentra en INEGI.localidades_dict
    ------------
    
    Regresa un diccionario con la información del indicador proporcionada por el API
    del INEGI en formato JSON. 

    Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

    """
    data = obtener_json(token,indicador,banco,localidad)
    obs_totales = len(data['Series'][0]['OBSERVATIONS'])
    dic = {'fechas':[data['Series'][0]['OBSERVATIONS'][i]['TIME_PERIOD'] for i in range(obs_totales)],
            indicador:[float(data['Series'][0]['OBSERVATIONS'][i]['OBS_VALUE']) for i in range(obs_totales)]}
    df = pd.DataFrame.from_dict(dic)
    df.set_index(pd.to_datetime(df.fechas),inplace=True, drop=True)
    df = df.drop(['fechas'],axis=1)
    return df

def indicadores_a_df(token,indicadores,bancos,localidades):
    """ 
    
    Construye un DataFrame con la información resultante del API del INEGI de 
    varios indicadores a la vez. 

    Parámetros:
    -----------
    token: str. Token para acceder al API.
    
    indicadores: list. Lista con los números de los indicadores a buscar.
    
    banco: list. Lista con el banco de información en donde se encuentra los
                 indocadores. Puede ser 'BIE' o 'BISE'.
    
    localidades: str o lista. Nombre, número o lísta de la entidad geográfica de 
                            la búsqueda, donde el 'Total Nacional' es el '0700' 
                            y los estados están ordenados alfabeticamente:
                                * 'Aguascalienes':'07000001'
                                * 'Baja California':'0700002'
                                * Resto de los estados
                       Un diccionario con los nombres y números de las 
                       entidades geográficas se encuentra en INEGI.localidades_dict
    ------------

    Regresa un diccionario con la información del indicador proporcionada por el API
    del INEGI en formato JSON. 

    Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

    """
    lista_df = []
    
    for i in range(len(indicadores)):
        indicador = indicadores[i]
        banco = bancos[i]
        for localidad in localidades:
            df = indicador_a_df(token, indicador, banco, localidad)
            df.columns = [indicador + ' ' + localidad]
            lista_df.append(df)
   
    df = pd.concat(lista_df,axis=1)
    return df    