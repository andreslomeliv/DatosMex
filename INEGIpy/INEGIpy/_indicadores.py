import pandas as pd
import requests
import json
import warnings
from numpy import nan

class Indicadores:
    
    def __init__(self, token):
        self.__token = token # token proporcionado por el INEGI único para cada usuario
        self.__liga = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/' 
        self.__liga_base = self.__liga + 'INDICATOR/' #base de los indicadores
        # vriables para la consulta
        self._indicadores = list() # lista con los indicadores a consultar. cada módulo la llena con sus especificaciones
        self._bancos = list() # lista con los bancos de los indicadores
        self._columnas = list() # nombres de las columnas. En los módulos de series se llena automáticamente.
        # diccionario con la clave de frecuencia del INEGI y el factor por el cual se debe multiplicar
        # el último valor para pasarlo a su mes correspondiente
        # Ejemplo: una serie semestral tiene como clave de frecuencia '4', esto indica que para cada año van
        # a haber dos periodos indicando los dos semestres: "2020/01, 2020/02"
        # El factor del diccionario indicaría que al último dígito lo multiplicamos por 6 para pasarlo a meses
        # las claves que no se encuentran en el diccionario son irregulares y no se van a operar
        self.__frecuancias_dict = {'BIE': {'1':(1,'Y'), '2':(1,'Y'), '3':(1,'Y'), '4':(6,'M'), '5':(4,'M'), '6':(3,'Q'), 
                                           '7':(2,'M'), '8':(1,'M'), '9':(14,'SM')},
                                    'BISE': {'1':(1,'Y'), '3':(1,'Y'), '4':(3,'Q'), '7':(1,'Y'), '8':(1,'M'), '9':(1,'Y'), '16':(1,'Y')}}
        self.__clave_entidad = None
        
############## Obtener Data Frame ########################

# Se definen  los métodos internos y públicos necesarios para obtener la serie y pasarla a un DataFrame
# Las dos variables esenciales para esto son self._indicadores y self._bancos. Cada módulo debe contar con métodos
# o atributos que permitan definir estas variables. También todas las variables de consulta deben ser accesibles tanto 
# dentro de las funciones obtener_df() y grafica() como parámetros así como atributos de la clase. 

    # aquí falta un control de errores cuando no se pudo obtener la info y advirtiendo que se cheque bien el token
    def __request(self, liga_api):
        req = requests.get(liga_api)
        assert req.status_code == 200, 'No se encontró información con las parámetros especificados.'
        data = json.loads(req.text)
        return data

    def __obtener_banco(self, indicador):
        if int(indicador) <= 698680: 
            return 'BIE'
        else: 
            return 'BISE'


    def __obtener_json(self, indicador, banco):
        """ 
    
        Construye la liga de consulta y obtiene la información resultante del API del
        INEGI. 
        
        Parámetros:
        ------------
        
        indicador: str.  Número del indicador a buscar.
       -------------
    
        Regresa un diccionario con la información del indicador proporcionada por el API
        del INEGI en formato JSON. 
    
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
    
        """
        if banco is None: 
            if indicador in ['539260', '539261', '539262']: 
                raise Exception("Para los indicadores '539260', '539261' y '539262' es necesario definir el banco ya que existen tanto para el BIE como para el BISE")
            else: banco = self.__obtener_banco(indicador)
        liga_api = '{}{}/es/{}/false/{}/2.0/{}?type=json'.format(self.__liga_base, indicador,  self.__clave_entidad, banco, str(self.__token))
        data = self.__request(liga_api)

        return data['Series'][0], banco
    
    def __json_a_df(self, data, banco):
        """ 
        
        Construye un DataFrame con la información resultante del API del INEGI de 
        un solo indicador a la vez.
    
        Parámetros:
        -----------
        data: Dict. JSON obtendio del API del INEGI.
        banco: str. Banco de información donde se encuentra el indocador. Puede ser 
                    'BIE' o 'BISE'.
        -----------
        
        Regresa un objeto tipo DataFrame con la información del indicador proporcionada por el API
        del INEGI en formato JSON. 
    
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
    
        """
        serie = data.pop('OBSERVATIONS') #con esto se separa la serie real de los metadatos

        # construcción de la serie
        obs_totales = len(serie)
        dic = {'fechas':[serie[i]['TIME_PERIOD'] for i in range(obs_totales)],
                'valor':[float(serie[i]['OBS_VALUE']) if serie[i]['OBS_VALUE'] is not None else nan for i in range(obs_totales)]}
        df = pd.DataFrame.from_dict(dic)
        frecuencia = data['FREQ']
        factor, period = self.__frecuancias_dict[banco].get(frecuencia) # factor que multiplica el periodo para pasar a fecha y periodo de pd
        if factor: 
            try: 
                cambio_fechas = lambda x: '/'.join(x.split('/')[:-1] + [str(int(x.split('/')[-1])*factor)])
                df.fechas = df.fechas.apply(cambio_fechas)
                df.set_index(pd.to_datetime(df.fechas),inplace=True, drop=True)
                df = df.drop(['fechas'],axis=1)
                if period == 'SM': df.index = df.index + pd.offsets.SemiMonthBegin()
            except: 
                df.fechas = dic['fechas']
                df.set_index(df.fechas,inplace=True, drop=True)
                df = df.drop(['fechas'],axis=1)
                warnings.warn('No se pudo interpretar la fecha correctamente por lo que el índice no es tipo DateTime')
        else:
            df.set_index(df.fechas,inplace=True, drop=True)
            df = df.drop(['fechas'],axis=1)
            warnings.warn('No se pudo interpretar la fecha correctamente por lo que el índice no es tipo DateTime')

        # construcción de metadatos
        data['BANCO'] = banco
        meta = pd.DataFrame.from_dict(data, orient='index', columns=['valor'])
            
        return df, meta

    def __definir_cve_ent(self, entidad):
        cve_base = '0700'
        if entidad == '00': 
            self.__clave_entidad = cve_base
            return
        if len(entidad[2:5]) == 0: self.__clave_entidad = '{}00{}'.format(cve_base, entidad[:2])
        else: self.__clave_entidad = '{}00{}0{}'.format(cve_base, entidad[:2], entidad[2:5])

    def _consulta(self, inicio, fin, banco, metadatos):
        
        if isinstance(self._indicadores, str): self._indicadores = [self._indicadores]
        if isinstance(self._bancos, str): self._bancos = [self._bancos]
        if isinstance(self._columnas, str): self._columnas = [self._columnas]
        
        lista_df = list()
        meta_dfs = list()
        for i in range(len(self._indicadores)):
            indicador = self._indicadores[i]
            data, banco = self.__obtener_json(indicador, banco)
            df, meta = self.__json_a_df(data, banco)
            if banco == 'BIE': df = df[::-1]
            lista_df.append(df)
            meta_dfs.append(meta)

        df = pd.concat(lista_df,axis=1)
        meta = pd.concat(meta_dfs, axis=1)
        try: 
            df.columns = self._columnas
            meta.columns = self._columnas
        except: 
            warnings.warn('Los nombres no coinciden con el número de indicadores')
            df.columns = self._indicadores
            meta.columns = self._indicadores

        if metadatos is False: return df[inicio:fin] 
        else: return df[inicio:fin], meta
        
    def obtener_df(self, 
                   indicadores: 'str|list', 
                   nombres: 'str|list' = None, 
                   clave_area: str = '00',
                   inicio: str = None, 
                   fin: str = None, 
                   banco: str = None, 
                   metadatos: bool = False):
        """
        Regresa un DataFrame con la información de los indicadores proporcionada por el API del INEGI. Si metadatos = True regresa un segundo DataFrame con las claves de los metadatos del indicador. 

        Parametros
        -----------
        indicadores: str/list. Clave(s) de los indicadores a consultar.
        nombres: list/str, opcional. Nombre(s) de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
        clave_area: str. Clave de dos a cinco caracteres que indentifica el área geográfica de acuerdo con el Marco Geoestadístico. Para definir el total nacional se especifica '00'. Este campo solo aplica para los indicadores del Bando de Indicadores (BISE), no aplica para los del Banco de Información Económica (BIE).
                                    Dos dígitos para incluir nivel estatal (ej.01 a 32).
                                    Cinco dígitos dígitos para incluir nivel municipal (ej. 01001).
        inicio: str, opcional. Fecha donde iniciar la serie en formato YYYY(-MM-DD). De no proporcionarse será desde el primer valor disponible. 
        fin: str, opcional. Fecha donde terminar la serie en formato YYYY(-MM-DD). De no proporcionarse será hasta el último valor disponible.
        banco: str, opcional. ['BIE' | 'BISE'] Define el banco al cual pertenecen los indicadores. Puede ser el Banco de Indicadores Económicos (BISE) o el Banco de Información Económica (BIE). Ya que solamente tres claves de indicadores se encuentran en ambos bancos y el resto son diferentes, no es necesario definir este parámetro a menos que los indicadores a consultar sea alguno de los siguientes: ['539260', '539261', '539262'].
        metadatos: bool. En caso se ser verdadero regresa un DataFrame con los metadatos de los indicadores.
        ----------
        
        El DataFrame resultante tiene una columna por cada indicador y un DateTimeIndex con la fecha de los valores. 
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        """     
        self._indicadores = indicadores
        self._columnas = indicadores
        if nombres is not None: 
            self._columnas = nombres
        self.__definir_cve_ent(clave_area)
        return self._consulta(inicio, fin, banco, metadatos)



## Catalogo de Metadatos

    def _consultar_catalogo(self, clave, id, banco):
        liga = '{}{}/{}/es/{}/2.0/{}/?type=json'.format(self.__liga, clave, id, banco, self.__token)
        req = requests.get(liga)
        data = json.loads(req.text)
        return pd.DataFrame(data['CODE'])

    def catalogo_indicadores(self, 
                             banco: str, 
                             indicador: str = None):
        '''
        Regresa un DataFrame con la descripción de algunos o todos los indicadores de un banco. 

        Parametros
        -----------
        banco: str. ['BIE' | 'BISE'] Define el banco al cual pertenecen los indicadores. Puede ser el Banco de Indicadores Económicos (BISE) o el Banco de Información Económica (BIE).
        indicador: str, opcional. Clave del indicador a consultar. En caso de no definirse se regresan todos los indicadores del banco.
        ----------
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        '''
        if indicador is None: indicador = 'null'
        return self._consultar_catalogo('CL_INDICATOR', indicador, banco)

    def consulta_metadatos(self, 
                           metadatos: 'DataFrame|dict'):
        '''
        Regresa un DataFrame con la descripción de los metadatos de una o más series. 

        Parametros
        -----------
        metadatos: DataFrame con los metadatos a consultar obtenido por la función obtener_df cuando metadatos = True. También acepta un diccionario equivalente.
        ----------
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        '''
        if isinstance(metadatos, dict): metadatos = pd.DataFrame.from_dict(dict)
        n_df = metadatos.copy(deep=True)
        for col in metadatos.columns:
            banco = metadatos.loc['BANCO',col]
            for idx in metadatos.index: 
                if idx in ['LASTUPDATE','BANCO']: continue
                id = metadatos.loc[idx,col]
                if id is None or len(id) == 0: continue
                if idx == 'INDICADOR': clave = 'CL_INDICATOR'
                else: clave = 'CL_{}'.format(idx)
                try:
                    desc = self._consultar_catalogo(clave, id, banco)
                    n_df.loc[idx,col] = desc.iloc[0,1]
                except: n_df.loc[idx,col] = 'No hay información'

        return n_df