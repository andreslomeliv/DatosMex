import pandas as pd
import requests
import json
import geopandas as gpd
from shapely.geometry import Point

class DENUE:
    def __init__(self, token):
        self.__token = token
        self.__liga_base = 'https://www.inegi.org.mx/app/api/denue/v1/consulta/'
        self.__df = None
    
    
    def __obtener_geodataframe(self, df): 
        df['geometry'] = df[['Longitud','Latitud']].astype(float).values.tolist()
        df.geometry = df.geometry.apply(Point)
        geo_df = gpd.GeoDataFrame(df)
        geo_df.crs = 'EPSG:4326'
        return geo_df
     
    #ahorita parece que no vale la pena esta funcion pero tal vez sirva más en el futuro
    #su punto es estandarizar los strings para de nombres o ramas economicas etc
    def __estadarizar_string(self, s): 
        s = s.lower().strip()
        return s
    
    # metodo general para obtener el json y pasarlo a un df o geodf
    def __obtener_consulta(self, liga, as_geodf):
        req = requests.get(liga)
        assert req.status_code == 200, 'No se encontró información con las parámetros especificados.'
        data = json.loads(req.text)
        df = pd.DataFrame(data)
        if as_geodf: df = self.__obtener_geodataframe(df)
        return df
        
    def Buscar(self, condiciones, latitud, longitud, distancia, as_geodf = True):
        ''' 
        Realiza una consulta de todos los establecimientos que cumplan las condiciones definidas.
        Esta función permite obtener la información de los establecimientos registrados en el DENUE dentro de un área definida de acuerdo con una lista de condiciones.
        
        Parámetros:
        ------------
        condiciones: str o list. Palabra(s) a buscar en el nombre del establecimiento, razón social, calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad.
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
        
    
    def Ficha(self, clave, as_geodf = True):
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
    
    def Nombre(self, nombre, entidad = '00', registro_inicial = 1, registro_final = 10, as_geodf = True):
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
    
    def BuscarEntidad(self, condiciones, entidad = '00', registro_inicial = 1, registro_final = 10, as_geodf = True):
        ''' 
        Realiza una consulta de todos los establecimientos que cumplan las condiciones definidas y puede ser acotada por entidad federativa.
        
        Parámetros:
        ------------
        condiciones: str o list. Palabra(s) a buscar en el nombre del establecimiento, razón social, calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad.
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

    def BuscarAreaAct(self, nombre, clave_area = None, entidad = '00', municipio = '0', localidad = '0', ageb = '0', manzana = '0', sector = '0', 
                      subsector = '0', rama = '0', clase = '0', registro_inicial = 1, registro_final = 10, clave_establecimiento = '0', as_geodf = True):
        ''' 
        Realiza una consulta de todos los establecimientos con la opción de acotar la búsqueda por área geográfica, actividad económica, nombre y clave del establecimiento.
        
        Las claves de actividad económica (sector, subsector, rama, clase) son únicas e incluyentes del nivel previo por lo que no solo se tiene que definir la clave con mayor desagregación. Si se define un subsector no es necesario definir un sector, si se define una rama no es necesario definir un subsector ni un sector, etc.

        Las claves para las áres geográficas no son únicas ni incluyentes del nivel previo. Si se define un AGEB pero no se define los niveles previos los resultados incluirán a todas las AGEBS con esa clave aunque se encuentren en diferentes entidades federativas, municipios y/o localidades. 
        Por esto, si no importa el nivel previo se pude definir cada nivel de manera individual. Sin embargo, si los niveles previos sí importan también se puede definir la clave completa o concatenada hasta el nivel de agregaión deseado para evitar llenar cada valor individualmente. 

        Parámetros:
        ------------
        nombre: str. Nombre del establecimiento a buscar.
        clave_area: str. Clave concatenada del área geográfica a buscar. Se puede definir para cualquier nivel de agregación, desde estado hasta manzana.
        entidad: str. Clave de dos dígitos de la entidad federativa (01 a 32). Para incluir todas las entidades se especifica 00.
        municipio: str. Clave de tres dígitos del municipio (ej. 001). Para incluir todos los municipios se especifica 0.
        localidad: str. Clave de cuatro dígitos de la localidad (ej. 0001 ). Para incluir todas las localidades se especifica 0.
        ageb: str. Clave de cuatro dígitos AGEB(ej. 2000 ).Para incluir todas las AGEBS se especifica 0.
        manzana: str. Clave de tres dígitos de la manzana (ej. 043 ). Para incluir todas las manzanas se especifica 0.
        sector: str. Clave de dos dígitos del sector de la actividad económica (ej. 46 ). Para incluir todos los sectores se especifica 0.
        subsector: str. Clave de tres dígitos del subsector de la actividad económica ( ej. 464 ). Para incluir todos los subsectores se especifica 0.
        rama: str. Clave de cuatro dígitos de la rama de la actividad económica (ej. 4641 ). Para incluir todas las ramas se especifica 0.
        clase: str. Clave de seis dígitos de la clase (ej. 464112 ). Para incluir todas las actividades se especifica 0.
        registro_inicial: int. Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
        registro_final: int. Número de registro final que se mostrará en los resultados de la búsqueda.
        clave_establecimiento: str. Clave única del establecimiento. Para incluir todos los establecimientos se especifica 0.
        as_geodf: bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial.
        ------------
        
        Regresa un DataFrame o GeoDataFrame con la información de la consulta.

        Para más información ir a: https://www.inegi.org.mx/servicios/api_denue.html
        
        '''
        if clave_area: 
            try: entidad = clave_area[:2]
            except: pass
            
            try: municipio = clave_area[2:5]
            except ExplicitException: pass
            
            try: localidad = clave_area[5:9]
            except ExplicitException: pass
            
            try: ageb = clave_area[9:13]
            except ExplicitException: pass
            
            try: manzana = clave_area[13:16]
            except ExplicitException: pass
            
        nombre = self.__estadarizar_string(nombre)
            
        liga = self.__liga_base + 'BuscarAreaAct/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}'.format(entidad, municipio, localidad, ageb, manzana,
                                                                                                    sector, subsector, rama, clase, 
                                                                                                    nombre, str(registro_inicial), str(registro_final),
                                                                                                    clave_establecimiento, self.__token)
        return self.__obtener_consulta(liga, as_geodf)

    def BuscarAreaActEstr(self, nombre, clave_area = None, entidad = '00', municipio = '0', localidad = '0', ageb = '0', manzana = '0', sector = '0', 
                          subsector = '0', rama = '0', clase = '0', registro_inicial = 1, registro_final = 10, clave_establecimiento = '0', estrato = '0', 
                          as_geodf = True):
        ''' 
        Realiza una consulta de todos los establecimientos con la opción de acotar la búsqueda por área geográfica, actividad económica, nombre,clave del establecimiento y estrato.
        
        Las claves de actividad económica (sector, subsector, rama, clase) son únicas e incluyentes del nivel previo por lo que no solo se tiene que definir la clave con mayor desagregación. Si se define un subsector no es necesario definir un sector, si se define una rama no es necesario definir un subsector ni un sector, etc.

        Las claves para las áres geográficas no son únicas ni incluyentes del nivel previo. Si se define un AGEB pero no se define los niveles previos los resultados incluirán a todas las AGEBS con esa clave aunque se encuentren en diferentes entidades federativas, municipios y/o localidades. 
        Por esto, si no importa el nivel previo se pude definir cada nivel de manera individual. Sin embargo, si los niveles previos sí importan también se puede definir la clave completa o concatenada hasta el nivel de agregaión deseado para evitar llenar cada valor individualmente. 

        Parámetros:
        ------------
        nombre: str. Nombre del establecimiento a buscar.
        clave_area: str. Clave concatenada del área geográfica a buscar. Se puede definir para cualquier nivel de agregación, desde estado hasta manzana.
        entidad: str. Clave de dos dígitos de la entidad federativa (01 a 32). Para incluir todas las entidades se especifica 00.
        municipio: str. Clave de tres dígitos del municipio (ej. 001). Para incluir todos los municipios se especifica 0.
        localidad: str. Clave de cuatro dígitos de la localidad (ej. 0001 ). Para incluir todas las localidades se especifica 0.
        ageb: str. Clave de cuatro dígitos AGEB(ej. 2000 ).Para incluir todas las AGEBS se especifica 0.
        manzana: str. Clave de tres dígitos de la manzana (ej. 043 ). Para incluir todas las manzanas se especifica 0.
        sector: str. Clave de dos dígitos del sector de la actividad económica (ej. 46 ). Para incluir todos los sectores se especifica 0.
        subsector: str. Clave de tres dígitos del subsector de la actividad económica ( ej. 464 ). Para incluir todos los subsectores se especifica 0.
        rama: str. Clave de cuatro dígitos de la rama de la actividad económica (ej. 4641 ). Para incluir todas las ramas se especifica 0.
        clase: str. Clave de seis dígitos de la clase (ej. 464112 ). Para incluir todas las actividades se especifica 0.
        registro_inicial: int. Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
        registro_final: int. Número de registro final que se mostrará en los resultados de la búsqueda.
        clave_establecimiento: str. Clave única del establecimiento. Para incluir todos los establecimientos se especifica 0.
        estrato: str. Clave de un dígito del estrato. Para incluir todos los tamaños se especifica 0.
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
        
        '''
        if clave_area: 
            try: entidad = clave_area[:2]
            except: pass
            
            try: municipio = clave_area[2:5]
            except ExplicitException: pass
            
            try: localidad = clave_area[5:9]
            except ExplicitException: pass
            
            try: ageb = clave_area[9:13]
            except ExplicitException: pass
            
            try: manzana = clave_area[13:16]
            except ExplicitException: pass
            
        nombre = self.__estadarizar_string(nombre)
            
        liga = self.__liga_base + 'BuscarAreaActEstr/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}'.format(entidad, municipio, localidad, ageb, manzana,
                                                                                                            sector, subsector, rama, clase, 
                                                                                                            nombre, str(registro_inicial), str(registro_final),
                                                                                                            clave_establecimiento, estrato, self.__token)
        return self.__obtener_consulta(liga, as_geodf)

    def Cuantificar(self, clave_actividad = '0', clave_area = '0', estrato = '0'):
        ''' 
        Realiza un conteo de todos los establecimientos con la opción de acotar la búsqueda por área geográfica, actividad económica y estrato.
        
        A diferencia de las otras funciones, esta solo permite ingresar las claves de actividad económica y de área en su forma completa o concatenada además de que también permite múltiples claves en cada campo.
        
        Otra diferencia importante es que el resultado de esta consulta no regresa valores de las coordenadas para obtener un GeoDataFrame por lo que no se encuentra tal opción por el momento.
        
        Parámetros:
        ------------
        clave_actividad: str o list. Clave(s) de dos a cinco dígitos de la actividad económica. Para considerar más de una clave deberás separarlas con coma. Para incluir todas las actividades se especifica 0.
                                        Dos dígitos para incluir nivel sector (ej.46).
                                        Tres dígitos para incluir nivel subsector (ej. 464).
                                        Cuatro dígitos para incluir nivel rama (ej. 4641).
                                        Cinco dígitos para incluir nivel subrama (ej. 46411).
                                        Seis dígitos para incluir nivel clase (ej. 464111).
        clave_area: str o list. Clave(s) de dos a nueve dígitos del área geográfica. Para incluir todo el país se especifica 0.
                                    Dos dígitos para incluir nivel estatal (ej.01 a 32).
                                    Cinco dígitos dígitos para incluir nivel municipal (ej. 01001).
                                    Nueve dígitos para incluir nivel localidad (ej. 010010001).
        estrato: str. Clave de un dígito del estrato. Para incluir todos los tamaños se especifica 0.
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
        