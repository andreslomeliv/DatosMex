import pandas as pd
import requests
import json
import geopandas as gpd
from shapely.geometry import Point

class DENUE:
    def __init__(self, token):
        self.__token = token
        self.__liga_base = 'https://www.inegi.org.mx/app/api/denue/v1/consulta/'
    
    # realiza las transformaciones necesarias para hacer iun geodataframe
    def __obtener_geodataframe(self, df): 
        df[['Longitud','Latitud']] = df[['Longitud','Latitud']].astype(float)
        df['geometry'] = df[['Longitud','Latitud']].values.tolist()
        df.geometry = df.geometry.apply(Point)
        geo_df = gpd.GeoDataFrame(df)
        geo_df.crs = 'EPSG:4326'
        return geo_df
     
    #ahorita parece que no vale la pena esta funcion pero tal vez sirva más en el futuro
    #su punto es estandarizar los strings para de nombres o ramas economicas etc
    # al final parece que esta función sí es totalmente inútil
    def __estadarizar_string(self, s): 
        s = s.lower().strip()
        return s
    
    # metodo general para obtener el json y pasarlo a un df o geodf
    def __obtener_consulta(self, liga, as_geodf):
        req = requests.get(liga)
        assert req.status_code == 200, 'No se encontró información con las parámetros especificados. \n Liga: {}'.format(liga)
        data = json.loads(req.text)
        df = pd.DataFrame(data)
        if as_geodf: df = self.__obtener_geodataframe(df)
        if len(df.columns) == 3: df.loc[:,'Total'] = df.loc[:, "Total"].astype(int)
        return df
        
    def Buscar(self, 
               condiciones: 'str|lsit', 
               latitud: float, 
               longitud: float, 
               distancia: int, 
               as_geodf: bool = True):
        ''' 
        Realiza una consulta de todos los establecimientos que cumplan las condiciones definidas.
        Esta función permite obtener la información de los establecimientos registrados en el DENUE dentro de un área definida de acuerdo con una lista de condiciones.
        
        Parámetros:
        ------------
        condiciones: str/list. Palabra(s) a buscar en el nombre del establecimiento, razón social, calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad. Para buscar todos los establecimientos se deberá ingresar la palabra "todos".
        latitud: float. Latitud que define el punto en el mapa a partir del cual se hará la consulta alrededor.
        longitud: float. Longitud que define el punto en el mapa a partir del cual se hará la consulta alrededor.
        distancia: int. Distancia en metros a partir de las coordenadas que definen el radio de búsqueda. La distancia máxima es de 5 000 metros.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 
        ------------
        
        Regresa un DataFrame o GeoDataFrame con la información de la consulta.
        
        Para más información ir a: https://www.inegi.org.mx/servicios/api_denue.html
        
        '''
        if isinstance(condiciones, str): condiciones = [condiciones]
        condiciones = [self.__estadarizar_string(s) for s in condiciones] # checar si es necesario estas dos lineas
        condiciones = ','.join(condiciones)
        coordenadas = '{},{}'.format(str(latitud),str(longitud))
        liga = self.__liga_base + 'Buscar/{}/{}/{}/{}'.format(condiciones, coordenadas, str(distancia), self.__token)
        return self.__obtener_consulta(liga, as_geodf)
        
    
    def Ficha(self, 
              clave: str, 
              as_geodf: bool = True):
        ''' 
        Obtiene la información de un establecimiento en específico.
        
        Parámetros:
        ------------
        clave: str. ID única del establecimiento.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial.
        ------------
        
        Regresa un DataFrame o GeoDataFrame con la información de la consulta.

        Para más información ir a: https://www.inegi.org.mx/servicios/api_denue.html
        
        '''
        liga = self.__liga_base + 'Ficha/{}/{}'.format(clave, self.__token)
        return self.__obtener_consulta(liga, as_geodf)
    
    def Nombre(self, 
               nombre: str, 
               entidad: str = '00', 
               registro_inicial: int = 1, 
               registro_final: int = 10, 
               as_geodf: bool = True):
        ''' 
        Realiza una consulta de todos los establecimientos por nombre o razón social.
        
        Parámetros:
        ------------
        nombre: str. Nombre del establecimiento ó razón social.
        entidad: str. Clave de dos dígitos de la entidad federativa (01 a 32). Para incluir todas las entidades se especifica 00.
        registro_inicial: int. Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
        registro_final: int. Número de registro final que se mostrará en los resultados de la búsqueda.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial.
        ------------
        
        Regresa un DataFrame o GeoDataFrame con la información de la consulta.

        Para más información ir a: https://www.inegi.org.mx/servicios/api_denue.html
        
        '''
        nombre = self.__estadarizar_string(nombre)
        liga = self.__liga_base + 'Nombre/{}/{}/{}/{}/{}'.format(nombre, entidad, str(registro_inicial), str(registro_final), self.__token)
        return self.__obtener_consulta(liga, as_geodf)
    
    def BuscarEntidad(self, 
                      condiciones: 'str|list', 
                      entidad: str = '00', 
                      registro_inicial: int = 1, 
                      registro_final: int = 10, 
                      as_geodf: bool = True):
        ''' 
        Realiza una consulta de todos los establecimientos que cumplan las condiciones definidas y puede ser acotada por entidad federativa.
        
        Parámetros:
        ------------
        condiciones: str/list. Palabra(s) a buscar en el nombre del establecimiento, razón social, calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad. Para buscar todos los establecimientos se deberá ingresar la palabra "todos".
        entidad: str. Clave de dos dígitos de la entidad federativa (01 a 32). Para incluir todas las entidades se especifica 00.
        registro_inicial: int. Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
        registro_final: int. Número de registro final que se mostrará en los resultados de la búsqueda.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial.
        ------------
        
        Regresa un DataFrame o GeoDataFrame con la información de la consulta.

        Para más información ir a: https://www.inegi.org.mx/servicios/api_denue.html
        
        '''
        if isinstance(condiciones, str): condiciones = [condiciones]
        condiciones = [self.__estadarizar_string(s) for s in condiciones] # checar si es necesario estas dos lineas
        condiciones = ','.join(condiciones)
        liga = self.__liga_base + 'BuscarEntidad/{}/{}/{}/{}/{}'.format(condiciones, entidad, str(registro_inicial), str(registro_final), self.__token)
        return self.__obtener_consulta(liga, as_geodf)
    
    # sirve para pasar de claves concatenadas de area y actividad económica a su versión separada para la consulta
    # evita que se llenen un montón de parámteros y simplifica las siguientes funciones
    def __desconcatenador(self, clave_area, clave_actividad):
        # para clave de area
        entidad = clave_area[:2] if len(clave_area[:2]) != 0 else '00'
        municipio = clave_area[2:5] if len(clave_area[2:5]) != 0 else '0'
        localidad = clave_area[5:9] if len(clave_area[5:9]) != 0 else '0'
        ageb = clave_area[9:13] if len(clave_area[9:13]) != 0 else '0'
        manzana = clave_area[13:16] if len( clave_area[13:16]) != 0 else '0'
        
        # para sector
        sector = clave_actividad if len(clave_actividad) == 2 else '0'
        subsector = clave_actividad if len(clave_actividad) == 3 else '0'
        rama = clave_actividad if len(clave_actividad) == 4 else '0'
        clase = clave_actividad if len(clave_actividad) == 6 else '0'
        
        return (entidad, municipio, localidad, ageb, manzana), (sector, subsector, rama, clase)

    def BuscarAreaAct(self, 
                      nombre: str, 
                      clave_area: str = '', 
                      clave_actividad: str = '', 
                      registro_inicial: int = 1, 
                      registro_final: int = 10,  
                      clave_establecimiento: str = '0', 
                      estrato: str = '0', 
                      as_geodf: bool = True):
        ''' 
        Realiza una consulta de todos los establecimientos con la opción de acotar la búsqueda por área geográfica, actividad económica, nombre, clave del establecimiento y estrato económico.
        
        Parámetros:
        ------------
        nombre: str. Nombre del establecimiento a buscar.
        clave_area: str. Clave de dos a dieciseis caracteres que indentifica el área geográfica de acuerdo con el Marco Geoestadístico. En caso de no definir una clave se regresan todos los establecimientos del país.
                                    Dos caracteres para incluir nivel estatal (ej. 01 a 32).
                                    Cinco caracteres dígitos para incluir nivel municipal (ej. 01001).
                                    Nueve caracteres para incluir nivel localidad (ej. 010010001).
                                    Trece caracteres para incluir nivel Área Geoestadística Básica (AGEB) (ej. 010010001216A).
                                    Dieciseis caracteres para incluir nivel manzana (ej. 010010001465A004).
        clave_actividad: str. Clave de dos a seis dígitos que identifica el área de actividad económica del establecimiento de acuerdo con el Sistema de Clasificación Industrial de América del Norte 2018. En caso de no definir una clave se regresan todas las áreas.
                                    Dos dígitos para definir un sector (ej.46).
                                    Tres dígitos para definir un subsector (ej. 464).
                                    Cuatro dígitos para definir una rama (ej. 4641).
                                    Cinco dígitos para definir una subrama (ej. 46411).
                                    Seis dígitos para definir una clase (ej. 464111).
        registro_inicial: int. Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
        registro_final: int. Número de registro final que se mostrará en los resultados de la búsqueda.
        clave_establecimiento: str. Clave única del establecimiento. Para incluir todos los establecimientos se especifica 0.
        estrato: str. Clave de un dígito que identifica el estrato del establecimiento (cantidad de trabajadores). Para incluir todos los tamaños se especifica 0.
                                    1. Para incluir de 0 a 5 personas.
                                    2. Para incluir de 6 a 10 personas.
                                    3. Para incluir de 11 a 30 personas.
                                    4. Para incluir de 31 a 50 personas.
                                    5. Para incluir de 51 a 100 personas.
                                    6. Para incluir de 101 a 250 personas.
                                    7. Para incluir de 251 y más personas.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial.
        ------------
        
        Regresa un DataFrame o GeoDataFrame con la información de la consulta.

        Para más información ir a: https://www.inegi.org.mx/servicios/api_denue.html
        
        Para consultar las claves de actividad económica ir a: https://www.inegi.org.mx/app/scian/
        
        '''
        cves_area, cves_act = self.__desconcatenador(clave_area, clave_actividad)
            
        nombre = self.__estadarizar_string(nombre)
            
        liga = self.__liga_base + 'BuscarAreaActEstr/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}'.format(cves_area[0],cves_area[1], cves_area[2], cves_area[3], cves_area[4],
                                                                                                          cves_act[0], cves_act[1], cves_act[2], cves_act[3],
                                                                                                          nombre, str(registro_inicial), str(registro_final),
                                                                                                          clave_establecimiento, estrato, self.__token)
        return self.__obtener_consulta(liga, as_geodf)

    def Cuantificar(self, 
                    clave_area: 'str|list' = '0',
                    clave_actividad: 'str|list' = '0', 
                    estrato: str = '0'):
        ''' 
        Realiza un conteo de todos los establecimientos con la opción de acotar la búsqueda por área geográfica, actividad económica y estrato.
        
        A diferencia de las otras funciones permite múltiples claves en cada campo.
        
        Otra diferencia importante es que el resultado de esta consulta no regresa valores de las coordenadas para obtener un GeoDataFrame.
        
        Parámetros:
        ------------
        clave_area: str/list. Clave(s) de dos a nueve caracteres que indentifica el área geográfica de acuerdo con el Marco Geoestadístico. En caso de no definir una clave se regresan todos los establecimientos del país.
                                    Dos dígitos para incluir nivel estatal (ej.01 a 32).
                                    Cinco dígitos dígitos para incluir nivel municipal (ej. 01001).
                                    Nueve dígitos para incluir nivel localidad (ej. 010010001).
        clave_actividad: str/list. Clave(s) de dos a seis dígitos que identifican el área de actividad económica de los establecimientos de acuerdo con el Sistema de Clasificación Industrial de América del Norte 2018. Para incluir todas las actividades se especifica 0.
                                    Dos dígitos para definir un sector (ej.46).
                                    Tres dígitos para definir un subsector (ej. 464).
                                    Cuatro dígitos para definir una rama (ej. 4641).
                                    Cinco dígitos para definir una subrama (ej. 46411).
                                    Seis dígitos para definir una clase (ej. 464111).
        estrato: str. Clave de un dígito que identifica el estrato del establecimiento (cantidad de trabajadores). Para incluir todos los tamaños se especifica 0.
                                    1. Para incluir de 0 a 5 personas.
                                    2. Para incluir de 6 a 10 personas.
                                    3. Para incluir de 11 a 30 personas.
                                    4. Para incluir de 31 a 50 personas.
                                    5. Para incluir de 51 a 100 personas.
                                    6. Para incluir de 101 a 250 personas.
                                    7. Para incluir de 251 y más personas.
        ------------
        
        Regresa un DataFrame con la información de la consulta.

        Para más información ir a: https://www.inegi.org.mx/servicios/api_denue.html
        
        '''
        if isinstance(clave_actividad, list): clave_actividad = ','.join(clave_actividad)
        if isinstance(clave_area, list): clave_area = ','.join(clave_area)
        liga = self.__liga_base + 'Cuantificar/{}/{}/{}/{}'.format(clave_actividad, clave_area, estrato, self.__token)
        return self.__obtener_consulta(liga, False)
        