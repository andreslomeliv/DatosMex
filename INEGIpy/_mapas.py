import pandas as pd
import requests
import json
import geopandas as gpd

class Mapas:
    def __init__(self):
        self.__liga_base = 'https://gaia.inegi.org.mx/wscatgeo/geo/'
        
    # uiliza la liga/url para obtener el geojson y pasarlo a un geodataframe
    def __obtener_geodf(self, liga):
        req = requests.get(liga)
        geojson =  json.loads(req.text)
        return gpd.GeoDataFrame.from_features(geojson["features"])
    
    # construye la liga y la lista de entidades
    # se tiene que ver la mejor fórma de usar esta función para entidades más desagregadas:
    # a cada nivel de agregación se añade una variable extra y complejiza más la consulta
    def __liga_y_entidades(self, nombres, claves, tipo_area):
        if nombres: 
            liga = '{}{}/buscar/'.format(self.__liga_base, tipo_area)
            entidades = nombres
        else: 
            liga = '{}{}/'.format(self.__liga_base, tipo_area)
            entidades = claves
        
        if isinstance(entidades, str): entidades = [entidades]
        
        return liga, entidades
    
    def __obtener_consulta(self, liga, entidades):
        dfs = list()
        if entidades: 
            for ent in entidades: 
                liga_final = liga + ent
                df = self.__obtener_geodf(liga_final)
                dfs.append(df)
            return pd.concat(dfs, axis = 0)
        else:
            return self.__obtener_geodf(liga)
    
    def Estados(self, claves = None, nombres = None):
        '''
        Obtiene el GeoDataFrame con las áreas geoestadísticas estatales.
        
        Si no se especifíca un estado o lista de estados la función regresa un GeoDataFrame con todas las Entidades Federativas.
        
        Parámetros:
        -----------
        claves: str/list. Clave(s) AGEE de los estados a buscar.
        nombres: str/list. Nombre(s) de los estados a buscar.
        -----------
        
        Regresa un GeoDataFrame con las áreas seleccionadas.
        
        Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html
        
        '''
        liga, entidades = self.__liga_y_entidades(nombres, claves, 'mgee')
        return self.__obtener_consulta(liga, entidades)
    
    def Municipios(self, nombres = None, claves = None):
        pass
    
    def Localidades(self):
        pass
    
    def AGEB(self):
        pass
    
    def Manzanas(self): 
        pass
    
    def Asentamientos(self):
        pass
    
    def Vialidades(self):
        pass