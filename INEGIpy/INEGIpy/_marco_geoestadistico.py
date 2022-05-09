import pandas as pd
import requests
import json
import geopandas as gpd
from typing import Optional

class MarcoGeoestadistico:
    def __init__(self):
        self.__liga_base = 'https://gaia.inegi.org.mx/wscatgeo/'
        
    # uiliza la liga/url para obtener el geojson y pasarlo a un geodataframe
    def __obtener_df(self, liga, as_gdf):
        req = requests.get(liga)
        assert req.status_code == 200, 'No se encontró información con las parámetros especificados. \n Liga: {}'.format(liga)
        data =  json.loads(req.text)
        if as_gdf: 
            try: 
                gdf = gpd.GeoDataFrame.from_features(data["features"])
                gdf.crs = 'EPSG:4326'
                return gdf
            except: raise Exception('No se encontró información con las parámetros especificados. \n Liga: {}'.format(liga))
        else: 
            try: return pd.DataFrame.from_dict(data['datos'])
            except: raise Exception('No se encontró información con las parámetros especificados. \n Liga: {}'.format(liga))
    
    # construye la liga y la lista de entidades
    # se tiene que ver la mejor fórma de usar esta función para entidades más desagregadas:
    # a cada nivel de agregación se añade una variable extra y complejiza más la consulta
    def __liga_y_areas(self, nombres, claves, tipo_area, as_gdf):
        if as_gdf: liga = '{}geo/'.format(self.__liga_base)
        else: liga =  self.__liga_base
        
        if nombres: 
            liga = '{}{}/buscar/'.format(liga, tipo_area)
            areas_geoestadisticas = nombres
        else: 
            liga = '{}{}/'.format(liga, tipo_area)
            areas_geoestadisticas = claves
        
        if isinstance(areas_geoestadisticas, str): areas_geoestadisticas = [areas_geoestadisticas]
        
        return liga, areas_geoestadisticas
    
    def __desconcatenador_de_claves(self, claves_concatenadas):
        entidades = list()
        municipios = list()
        localidades = list()
        if isinstance(claves_concatenadas, str): claves_concatenadas = [claves_concatenadas]
        for clave in claves_concatenadas:
            if len(clave[:2]) > 0: entidades.append(clave[:2])
            else: entidades.append(None)# aquí sería agregar un raise exception

            if len(clave[2:5]) > 0: municipios.append(clave[2:5])
            else: municipios.append(None)

            if len(clave[5:9]) > 0: localidades.append(clave[5:9])
            else: localidades.append(None)
            
        return entidades, municipios, localidades
    
    # para el caso de localidades lo mejor es concatenar en una sola clave en vez de separar con diagonales,
    # para eso se agrego la variable separadas.
    def __obtener_claves(self, entidades, municipios, localidades, agebs, claves_concatenadas, separadas = True):
        if claves_concatenadas: entidades, municipios, localidades = self.__desconcatenador_de_claves(claves_concatenadas)
        niveles = [entidades, municipios, localidades, agebs]
        if separadas: s = '{}/'
        else: s = '{}'
        clave = ''
        for nivel in niveles:
            if nivel is None: return clave
            elif isinstance(nivel, str): clave = clave + s.format(nivel)
            elif isinstance(nivel, list) and isinstance(clave, str): clave = [clave + s.format(n) for n in nivel] # más bien sería claves pero tiene iun punto seguir nombrándola clave
            elif isinstance(nivel, list) and isinstance(clave, list): clave = [clave[i]  + s.format(nivel[i]) if nivel[i] else clave[i] for i in range(len(nivel))]
            
        return clave
                
    def __obtener_consulta(self, liga, areas_geoestadisticas, as_gdf, ambito = None):
        if ambito not in ['rural','urbano', 'r','u',None]: raise Exception('El ámbito proporcionado no es correcto.') 
        dfs = list()
        if areas_geoestadisticas: 
            for area in areas_geoestadisticas: 
                liga_final = liga + area
                if ambito: liga_final = liga_final + ambito.capitalize()[0]
                df = self.__obtener_df(liga_final, as_gdf)
                dfs.append(df)
            c_df = pd.concat(dfs, axis = 0)
            return c_df.reset_index(drop = True)
        else:
            return self.__obtener_df(liga, as_gdf)
    
    def Entidades(self, 
                  entidades: 'str|list' = None, 
                  nombres: 'str|list' = None, 
                  as_geodf: bool = True):
        '''
        Obtiene el DataFrame con las áreas geoestadísticas estatales.
        
        Si no se especifíca un estado o lista de estados la función regresa un GeoDataFrame con todas las Entidades Federativas.
        
        Parámetros:
        -----------
        entidades: str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
        nombres: str/list. Nombre(s) de los estados a buscar.Si se define este parámetro obtiene las áreas geoestadísticas estatales cuyo nombre contenga el texto proporcionado sin necesidad de proporcionar las claves de las entidades. No distingue entre mayúsculas y minúsculas pero sí considera acentos.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 
        -----------
        
        Regresa un Dataframe o GeoDataFrame con las áreas seleccionadas.
        
        Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html
        
        '''
        liga, areas_geoestadisticas = self.__liga_y_areas(nombres, entidades, 'mgee', as_geodf)
        return self.__obtener_consulta(liga, areas_geoestadisticas, as_geodf)
    
    # esta requiere llamar la función concatenadora
    def Municipios(self, 
                   entidades: 'str|list' = None, 
                   municipios: 'str|list' = None, 
                   nombres: 'str|list' = None, 
                   claves_concatenadas: 'str|list' = None, 
                   as_geodf: bool = True):
        '''
        Obtiene el DataFrame con las áreas geoestadísticas municipales.
        
        Si no se especifícan los parámetros regresa un DataFrame con todos los municipios de México.
        
        Nota: si se pasa una lista de entidades no se puede definir un municipio en específico a buscar. En este caso se regresan todos los municipios de la lista de entidades.
        
        Parámetros:
        -----------
        entidades: str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
        municipios: str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001).
        nombres: str/list. Nombre(s) de los municipios a buscar. Si se define este parámetro obtiene las áreas geoestadísticas municipales cuyo nombre contenga el texto proporcionado sin necesidad de proporcionar las claves de los municipios. No distingue entre mayúsculas y minúsculas pero sí considera acentos.
        claves_concatendas: str/list. Clave(s) concatenada con los niveles de agregación espacial.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 
        -----------
        
        Regresa un DataFrame o GeoDataFrame con las áreas seleccionadas.
        
        Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html
        
        '''
        claves = self.__obtener_claves(entidades, municipios, None, None, claves_concatenadas)
        liga, areas_geoestadisticas = self.__liga_y_areas(nombres, claves, 'mgem', as_geodf)
        return self.__obtener_consulta(liga, areas_geoestadisticas, as_geodf)
    
    def LocalidadesAmanzanadas(self, 
                               entidades: 'str|list' = None, 
                               municipios: 'str|list' = None, 
                               localidades: 'str|list' = None, 
                               nombres: 'str|list' = None, 
                               claves_concatenadas: 'str|list' = None, 
                               ambito: str = None, 
                               as_geodf: bool = True):
        '''
        Obtiene el DataFrame con las áreas geoestadísticas a nivel localidad amanzanada.
        
        Si no se especifícan los parámetros regresa un DataFrame con todas las localidades de México. 
        
        Nota: si se pasa una lista de áreas con nivel de agregación menor a la localidad no se puede definir una localidad en específico a buscar. En este caso se regresan todos las localidades de los niveles previos. 
        
        Parámetros:
        -----------
        entidades: str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
        municipios: str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001)
        localidades: str/list. Clave(s) de cuatro dígitos de las localidad a buscar (ej. 0001 )
        nombres: str/list. Nombre(s) de las localidades a buscar. Si se define este parámetro obtiene las localidades amanzanadas cuyo nombre contenga el texto proporcionado sin necesidad de proporcionar las claves de las localidades. No distingue entre mayúsculas y minúsculas pero sí considera acentos.
        claves_concatendas: str/list. Clave(s) concatenada con los niveles de agregación espacial.
        ambito: str. ['urbano'|'rural'] Define el ambito de las localidades. Si se define un ámbito no se puede definir una localidad en específico y se debe definir tanto entidad como municipio.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 
        -----------
        
        Regresa un DataFrame o GeoDataFrame con las áreas seleccionadas.
        
        Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html
        
        '''
        if ambito: claves = self.__obtener_claves(entidades, municipios, localidades, None, claves_concatenadas)
        else: claves = self.__obtener_claves(entidades, municipios, localidades, None, claves_concatenadas, False)
        liga, areas_geoestadisticas = self.__liga_y_areas(nombres, claves, 'localidades/pol', True)
        df = self.__obtener_consulta(liga, areas_geoestadisticas, True, ambito)
        if as_geodf is False: df = pd.DataFrame(df.drop('geometry',axis=1))
        return df
    
    def LocalidadesRuralesPuntuales(self, 
                                    entidades: 'str|list' = None, 
                                    municipios: 'str|list' = None, 
                                    localidades: 'str|list' = None, 
                                    nombres: 'str|list' = None, 
                                    claves_concatenadas: 'str|list' = None, 
                                    as_geodf: bool = True):
        '''
        Obtiene el DataFrame con las áreas geoestadísticas a nivel localidad rural puntual.
        
        Si no se especifícan los parámetros regresa un DataFrame con todas las localidades rurales puntuales de México. 
        
        Nota: si se pasa una lista de áreas con nivel de agregación menor a la localidad no se puede definir una localidad en específico a buscar. En este caso se regresan todos las localidades de los niveles previos. 
        
        Parámetros:
        -----------
        entidades: str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
        municipios: str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001)
        loacalidades: str/list. Clave(s) de cuatro dígitos de las localidad a buscar (ej. 0001 )
        nombres: str/list. Nombre(s) de las localidades a buscar. Si se define este parámetro obtiene las localidades amanzanadas cuyo nombre contenga el texto proporcionado sin necesidad de proporcionar las claves de las localidades. No distingue entre mayúsculas y minúsculas pero sí considera acentos.
        claves_concatendas: str/list. Clave(s) concatenada con los niveles de agregación espacial.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 
        -----------
        
        Regresa un DataFrame o GeoDataFrame con las áreas seleccionadas.
        
        Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html
        
        '''
        claves = self.__obtener_claves(entidades, municipios, localidades, None, claves_concatenadas, False)
        liga, areas_geoestadisticas = self.__liga_y_areas(nombres, claves, 'localidades/ruralespto', True)
        df = self.__obtener_consulta(liga, areas_geoestadisticas, True, ambito)
        if as_geodf is False: df = pd.DataFrame(df.drop('geometry',axis=1))
        return df
    
    def AGEBs(self, 
              entidades: 'str|list' = None, 
              municipios: 'str|list' = None, 
              localidades: 'str|list' = None, 
              agebs: 'str|list' = None, 
              claves_concatenadas: 'str|list' = None, 
              ambito: str = 'urbano', 
              as_geodf: bool = True):
        '''
        Obtiene el DataFrame con las áreas geoestadísticas a nivel Área Geoestadística Básica. 
        
        Nota: si se pasa una lista de áreas con nivel de agregación menor al AGEB no se puede definir una localidad en específico a buscar. En este caso se regresan todos los AGEBs de los niveles previos. 
        
        Parámetros:
        -----------
        entidades: str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
        municipios: str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001).
        loacalidades: str/list. Clave(s) de cuatro dígitos de las localidad a buscar (ej. 0001).
        agebs: str/list. Clave(s) de cuatro dígitos con las AGEBs a buscar (ej. 2000).
        claves_concatendas: str/list. Clave(s) concatenada con los niveles de agregación espacial.
        ambito: str. ['urbano'|'rural'] Define el ambito de las AGEBs. A diferencia de las localidades amanzanadas siempre se debe especificar el ambitos de las AGEBsa buscar. Por default son urbanas.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 
        -----------
        
        Regresa un DataFrame o GeoDataFrame con las áreas seleccionadas.
        
        Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html
        
        '''
        tipo_area = 'ageb{}'.format(ambito[0].lower())
        if agebs: claves = self.__obtener_claves(entidades, municipios, localidades, agebs, claves_concatenadas, False)
        else: claves = self.__obtener_claves(entidades, municipios, localidades, agebs, claves_concatenadas)
        if claves_concatenadas: claves = [self.__obtener_claves(claves_concatenadas=clave)[0] if len(clave) <= 5 else clave for clave in claves]
        liga, areas_geoestadisticas = self.__liga_y_areas(None, claves, tipo_area, as_geodf)
        return self.__obtener_consulta(liga, areas_geoestadisticas, as_geodf)
        
        
    
    def Manzanas(self, 
                 entidades: 'str|list' = None,
                 municipios: 'str|list' = None, 
                 localidades: 'str|list' = None, 
                 claves_concatenadas: 'str|list' = None, 
                 ambito: str = None, 
                 as_geodf: bool = True):
        '''
        Obtiene el DataFrame con las áreas geoestadísticas a nivel manzana. 
        
        Nota: si se pasa una lista de áreas con nivel de agregación menor a la localidad no se puede definir una localidad en específico a buscar. En este caso se regresan todos las localidades de los niveles previos. 
        
        Tampoco se puede difinir un nivel de agregación sin definir el nivel previo. No se puede definir un municipio sin definir una entidad, etc.
        
        Parámetros:
        -----------
        entidades: str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
        municipios: str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001)
        localidades: str/list. Clave(s) de cuatro dígitos de las localidad a buscar (ej. 0001)
        claves_concatendas: str/list. Clave(s) concatenada con los niveles de agregación espacial.
        ambito: str. ['urbano'|'rural'] Define el ambito de las manzanas. Si se define un ámbito no se puede definir una localidad en específico y se debe definir tanto entidad como municipio.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 
        -----------
        
        Regresa un DataFrame o GeoDataFrame con las áreas seleccionadas.
        
        Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html
        
        '''
        claves = self.__obtener_claves(entidades, municipios, localidades, None, claves_concatenadas)
        liga, areas_geoestadisticas = self.__liga_y_areas(None, claves, 'mza', as_geodf)
        return self.__obtener_consulta(liga, areas_geoestadisticas, as_geodf, ambito)
    
    def Vialidades(self, 
                   entidades: 'str|list' = None, 
                   municipios: 'str|list' = None, 
                   localidades: 'str|list' = None, 
                   claves_concatenadas: 'str|list' = None, 
                   as_geodf: bool = True):
        '''
        Obtiene el DataFrame con las áreas geoestadísticas a nivel vialidad.
        
        Nota: si se pasa una lista de áreas con nivel de agregación menor a la localidad no se puede definir una localidad en específico a buscar. En este caso se regresan todos las localidades de los niveles previos. 
        
        Tampoco se puede difinir un nivel de agregación sin definir el nivel previo. No se puede definir un municipio sin definir una entidad, etc.
        
        Parámetros:
        -----------
        entidades: str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
        municipios: str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001)
        localidades: str/list. Clave(s) de cuatro dígitos de las localidad a buscar (ej. 0001)
        claves_concatendas: str/list. Clave(s) concatenada con los niveles de agregación espacial.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 
        -----------
        
        Regresa un DataFrame o GeoDataFrame con las áreas seleccionadas.
        
        Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html
        
        '''
        if localidades or claves_concatenadas: 
            claves = self.__obtener_claves(entidades, municipios, localidades, None, claves_concatenadas, False)
            claves = [self.__obtener_claves(None, None, None, None, clave)[0] if len(clave) <= 5 else clave for clave in claves]
        else: claves = self.__obtener_claves(entidades, municipios, localidades, None, claves_concatenadas)
        liga, areas_geoestadisticas = self.__liga_y_areas(None, claves, 'vialidades', as_geodf)
        return self.__obtener_consulta(liga, areas_geoestadisticas, as_geodf)
