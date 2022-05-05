import requests
import json
import numpy as np
import pandas as pd
from pandas import DataFrame
import geopandas as gpd
from shapely.geometry import shape

# Módulo dedicado al api de Ruteo del INEGI: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token

# falta usar typing para definir los tipos que reciben los parámteros en las funciones de ruteo. 

class Ruteo:
    def __init__(self, token):
        self.__token = token
        self.__liga_base = 'https://gaia.inegi.org.mx/sakbe_v3.1/'
        
    def __obtener_consulta(self, funcion, params, as_geodf = True): # función base para realizar consulta y generar el geodataframe
        req = requests.post('https://gaia.inegi.org.mx/sakbe_v3.1/{}'.format(funcion), params=params)
        try: data = json.loads(req.text)['data']
        except: raise Exception("No se encontraro resultados para la búsqueda")
        if isinstance(data, dict): data = [data]
        df = pd.DataFrame.from_dict(data)
        if as_geodf:
            df['geometry'] = df['geojson'].apply(lambda x: shape(json.loads(x)))
            df = df.drop('geojson', axis=1)
            df = gpd.GeoDataFrame(df)
            df.crs = 'EPSG:4326'
            return df
        return df
        
    def BuscarDestino(self, busqueda: str, cantidad: int, proyeccion: str = 'GRS80'): 
        '''
        Permite buscar destinos como localidades urbanas y rurales, así como los sitios de interés que pueden ser instalaciones de servicios como aeropuertos, puertos, servicios médicos, centros educativos de nivel superior, así como sitios atractivos para el turismo como playas, cascadas, zonas arqueológicas, museos, pueblos mágicos, y más.
        
        Parámetros:
        -----------
        busqueda: str. Define el nombre o parte del destino que se desea encontrar. Se puede utilizar una coma para especificar la entidad federativa, p. e. “San Juan, Jalisco”.
        cantidad: int. Número de destinos que se desea obtener. 
        proyeccion: str. Define la proyección de los puntos resultantes. GRS80 para coordenadas geográficas y MERC para coordenadas Spherical Mercator. Por default será GRS80. 
        -----------
        
        Obtiene un GeoDataFrame con la información de los destinos registrados en la Red Nacional de Caminos. 

        Para más información consultar: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token

        '''
        params = {'buscar':busqueda, 
                  'type':'json', 
                  'num':cantidad, 
                  'key':self.__token, 
                  'proj':proyeccion}
        return self.__obtener_consulta('buscadestino', params)
    
    def BuscarLinea(self, lat: float, lng: float, escala: int = 1_000_000, proyeccion: str = 'GRS80'):
        '''
        Obtiene un GeoDataFrame con la información de la línea registrada en la Red Nacional de Caminos más cercana a una coordenada. 
        
        Parámetros:
        -----------
        lat: float. Latitud de la coordenada.
        lng: float. Longitud de la coordenada.
        escala: int. Valor de la escala de visualización. Por default es 1,000,000.
        proyeccion: str. Define la proyección de los puntos resultantes. GRS80 para coordenadas geográficas y MERC para coordenadas Spherical Mercator. Por default será GRS80. 
        -----------

        Para más información consultar: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token

        '''
        params = {'escala': escala, 
                  'type': 'json', 
                  'x': lng, 
                  'y': lat,
                  'key': self.__token, 
                  'proj': proyeccion}
        return self.__obtener_consulta('buscalinea', params)
    
    def __obtener_ruta(self, linea_inicial, linea_final, destino_inicial, destino_final, tipo_vehiculo, ruta, ejes_excedentes, saltar_lineas, proyeccion, funcion):
        rutas_validas = ['optima', 'libre', 'cuota']
        if ruta not in rutas_validas: raise ValueError("El tipo de ruta deber ser alguno de los siguientes {}".format(rutas_validas))
        if funcion == 'detalle_': funcion = '{}{}'.format(funcion, ruta[0])
        else: funcion = ruta
        params = {'type': 'json',
                  'key': self.__token, 
                  'proj': proyeccion,
                  'v': tipo_vehiculo,
                  'e': ejes_excedentes}
        
        if linea_inicial is not None:
            try: 
                n_params  = {'id_i': linea_inicial['id_routing_net'], 'source_i': linea_inicial['source'], 'target_i': linea_inicial['target']}
                params.update(n_params)
            except: raise Exception("Se deben proporcionar los parámterios id_routing_net, source y target de la línea inicial")
                                  
        if linea_final is not None:
            try: 
                n_params  = {'id_f': linea_final['id_routing_net'], 'source_f': linea_final['source'], 'target_f': linea_final['target']}
                params.update(n_params)
            except: raise Exception("Se deben proporcionar los parámterios id_routing_net, source y target de la línea final")
            
        if destino_inicial is not None: 
            if isinstance(destino_inicial, DataFrame): params['dest_i'] = destino_inicial['id_dest']
            else: params['dest_i'] = destino_inicial
        if destino_final is not None:
            if isinstance(destino_final, DataFrame): params['dest_f'] = destino_inicial['id_dest']
            else: params['dest_f'] = destino_final
        if saltar_lineas is not None: params['b'] = ','.join(saltar_lineas)
        
        return self.__obtener_consulta(funcion, params)
    
    def CalcularRuta(self, linea_inicial = None, linea_final = None, destino_inicial = None, destino_final = None, tipo_vehiculo: int = 0, 
                     ruta: str = 'optima', ejes_excedentes: int = 0, saltar_lineas = None, proyeccion: str = 'GRS80'):
        '''
        Obtiene un GeoDataFrame con la ruta calculada por Sistema de Ruteo de México y la Red Nacional de Caminos. Se puede obtener rutas de línea-línea, destino-destino, línea-destino y destino-linea. 
        
        Parámetros:
        -----------
        linea_inicial: DataFrame con las columnas id_routing_net, source y target de la línea inicial obtenido por la función BuscarLinea. También acepta un diccionario con la misma información.
        linea_final: DataFrame con las columnas id_routing_net, source y target de la línea final obtenido por la función BuscarLinea. También acepta un diccionario con la misma información.
        destino_inicial: DataFrame con la columna id_dest del destino inicial obtenido por la función BuscarDestino. También acepta el valor de id_dest en string o integer. 
        destino_final: DataFrame con la columna id_dest del destino final obtenido por la función BuscarDestino. También acepta el valor de id_dest en string o integer. 
        tipo_vehiculo: int. Clave con el tipo de vehículo. Por default es 0 que equivale a motocicleta mientras que 1 equivale a automóvil. Para consultar los demás valores se debe revisar la guía de desarrolladores en: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token
        ruta: str. ['optima' | 'libre' | 'cuota']. Tipo de ruta que se desea obtener. 
        ejes_excedentes: int. Número de ejes excedentes del vehículo. Por default es 0 que equivale a ningíun eje excedente. Para consultar los demás valores se debe revisar la guía de desarrolladores en: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token
        saltar_lineas: list. Lista con los id_routing_net de las líneas por las cuales la ruta no pasará por algún motivo. Por default es None.
        proyeccion: str. Define la proyección de los puntos resultantes. GRS80 para coordenadas geográficas y MERC para coordenadas Spherical Mercator. Por default será GRS80. 
        -----------

        Para más información consultar: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token

        '''

        ruta = self.__obtener_ruta(linea_inicial, linea_final, destino_inicial, destino_final, tipo_vehiculo, ruta, ejes_excedentes, saltar_lineas, proyeccion, '')
        ruta['peaje'] = np.select([ruta.peaje == 'f'],[False], True)
        
        return ruta
    
    def DetalleRuta(self, linea_inicial = None, linea_final = None, destino_inicial = None, destino_final = None, tipo_vehiculo: int = 0, 
                     ruta: str = 'optima', ejes_excedentes: int = 0, saltar_lineas = None, proyeccion: str = 'GRS80'):
        '''
        Obtiene un GeoDataFrame con los detalles de la ruta calculada por Sistema de Ruteo de México y la Red Nacional de Caminos. Se puede obtener rutas de línea-línea, destino-destino, línea-destino y destino-linea. 
        
        Parámetros:
        -----------
        linea_inicial: DataFrame con las columnas id_routing_net, source y target de la línea inicial obtenido por la función BuscarLinea. También acepta un diccionario con la misma información.
        linea_final: DataFrame con las columnas id_routing_net, source y target de la línea final obtenido por la función BuscarLinea. También acepta un diccionario con la misma información.
        destino_inicial: DataFrame con la columna id_dest del destino inicial obtenido por la función BuscarDestino. También acepta el valor de id_dest en string o integer. 
        destino_final: DataFrame con la columna id_dest del destino final obtenido por la función BuscarDestino. También acepta el valor de id_dest en string o integer. 
        tipo_vehiculo: int. Clave con el tipo de vehículo. Por default es 0 que equivale a motocicleta mientras que 1 equivale a automóvil. Para consultar los demás valores se debe revisar la guía de desarrolladores en: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token
        ruta: str. ['optima' | 'libre' | 'cuota']. Tipo de ruta que se desea obtener. 
        ejes_excedentes: int. Número de ejes excedentes del vehículo. Por default es 0 que equivale a ningíun eje excedente. Para consultar los demás valores se debe revisar la guía de desarrolladores en: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token
        saltar_lineas: list. Lista con los id_routing_net de las líneas por las cuales la ruta no pasará por algún motivo. Por default es None.
        proyeccion: str. Define la proyección de los puntos resultantes. GRS80 para coordenadas geográficas y MERC para coordenadas Spherical Mercator. Por default será GRS80. 
        -----------

        Para más información consultar: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token

        '''
        return self.__obtener_ruta(linea_inicial, linea_final, destino_inicial, destino_final, tipo_vehiculo, ruta, ejes_excedentes, saltar_lineas, proyeccion, 'detalle_')


    def Combustibles(self): 
        '''
        Regresa un DataFrame con los 4 tipos de combustibles más comunes y su costo promedio que se consultan el primer día hábil de cada semana en la página web de la Comisión Reguladora de Energía del Gobierno Federal: https://www.gob.mx/cre

        Nota: el dato que provee esta API solo es una referencia en función del precio promedio nacional excluyendo las 7 regiones sobre la frontera. También lo que refiere al gas LP el precio es un promedio ponderado que publica la Comisión Reguladora de Energía.

        Para más información consultar: https://www.inegi.org.mx/servicios/Ruteo/Default.html#token

        '''
        params = {'key':self.__token, 
                    'type': 'json'}
        return self.__obtener_consulta('combustible', params, as_geodf = False)