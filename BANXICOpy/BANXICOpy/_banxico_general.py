import requests
import json
import pandas as pd
import re

class Banxico:
    def __init__(self, token):
        self.__token = token
        self.__liga_base = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series'
        self._indicadores = list()
        self._columnas = list()
        
    def __generar_consulta(self, consulta, params):
        indicadores = ','.join(self._indicadores)
        url = '{}/{}/{}'.format(self.__liga_base, indicadores, consulta)
        req = requests.get(url ,params=params)
        data = json.loads(req.text)
        return data['bmx']['series']
    
    def __json_a_df(self, data, metadatos = False):
        if metadatos is True:
            return pd.DataFrame(data)
        else:
            dfs = list()
            for d in data: 
                    df = pd.DataFrame(d['datos'])
                    df.index = pd.to_datetime(df.fecha,format='%d/%m/%Y')
                    df = df.drop(['fecha'],axis=1)
                    df['dato'] = df['dato'].str.replace(',', '')
                    df['dato'] = df['dato'].str.replace('N/E', 'NaN').astype(float)
                    dfs.append(df)

            df = pd.concat(dfs, axis=1)  
            try: df.columns = self._columnas
            except: raise Exception('El número de columnas no coincide con el número de indicadores')
        return df
    
    def __parametros(self, decimales, incremento):
        params = {'token': self.__token}
        if decimales is False: params['decimales'] = 'sinCeros'
        if incremento is not None: 
            opciones = ['PorcObsAnt','PorcAnual','PorcAcumAnual']
            if incremento not in opciones:
                raise Exception('El incremento debe ser alguna da las siguientes opciones: {}'.format(opciones))
            params['incremento'] = incremento
        return params

    def __definir_valores(self, indicadores, nombres):
        self._indicadores = indicadores
        if nombres is not None: self._columnas = nombres
        elif re.match('.+-.+', indicadores): 
            s,f = re.findall("SF(\d)", indicadores)
            s,f = int(s), int(f)
            self._columnas = ['SF{}'.format(i) for i in range(s,f+1)]
        else: self._columnas = indicadores  
        
        if isinstance(self._columnas, str): self._columnas = [self._columnas]
        if isinstance(self._indicadores, str): self._indicadores = [self._indicadores]


    def obtener_series(self, 
                       indicadores: 'str|list', 
                       nombres: 'str|list' = None, 
                       inicio: str = None, 
                       fin: str = None, 
                       decimales: bool = True,
                       incremento: str = None):
        """
        Regresa un DataFrame con los datos de los indicadores proporcionados por la API de Banxico. 
        
        Nota: esta función concatena todos los indicadores en un solo DataFrame por lo que es recomendable usarla para varias series con una misma frecuencia. En caso de no querer concatenar las series se debe usar un indicador a la vez. 

        Parametros
        -----------
        indicadores: str/list. Calve(s) de los indicadores a consultar. Puede ser hasta un máximo de 20 indicadores a la vez.
        nombres: list/str, opcional. Nombre(s) de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
        inicio: str, opcional. Fecha donde iniciar la serie en formato YYYY(-MM-DD). De no proporcionarse será desde el primer valor disponible. 
        fin: str, opcional. Fecha donde terminar la serie en formato YYYY(-MM-DD). De no proporcionarse será hasta el último valor disponible.
        decimales: bool. En caso de ser verdadero regresa la serie con todos los decimales. Si es falso elimina los ceros decimales al final del punto decimal (los menos significativos).
        incremento: str, opcional. En caso de definir alguna de las opciones regresa la serie como el incremento porcentual de alguna observación previa. Las opciones disponibles son las siguientes:
                            * PorcObsAnt: Porcentaje de incremento con respecto a la observación anterior.
                            * PorcAnual: Porcentaje de incremento con respecto a la misma observación del año anterior.
                            * PorcAcumAnual: Porcentaje de incremento con respecto a la última observación del año anterior.
        ----------

        El DataFrame resultante tiene una columna por cada indicador y un DateTimeIndex con la fecha de los valores. 
        
        Para más información visitar https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#

        """
        self.__definir_valores(indicadores, nombres)
        params = self.__parametros(decimales, incremento)
        data = self.__generar_consulta('datos', params)
        df = self.__json_a_df(data)
        return df[inicio:fin]
    
    def metadatos(self, 
                  indicadores: 'str|list'):
        """
        Regresa un DataFrame con los metadatos de los indicadores proporcionados por la API de Banxico.

        Parametros
        -----------
        indicadores: str/list. Calve(s) de los indicadores a consultar. Puede ser hasta un máximo de 20 indicadores a la vez.
        ----------

        El DataFrame resultante tiene una fila para cada indicador y una columna para cada metadato. 
        
        Para más información visitar https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#

        """
        self.__definir_valores(indicadores, None)
        params = self.__parametros(True, None)
        data = self.__generar_consulta('', params)
        return self.__json_a_df(data, metadatos = True)
        
    def dato_oportuno(self, 
                      indicadores: 'str|list', 
                      nombres: 'str|list' = None,
                      decimales: bool = True,
                      incremento: str = None):
        """
        Regresa un DataFrame con el último dato de los indicadores proporcionados por la API de Banxico.
        
        Nota: esta función concatena todos los indicadores en un solo DataFrame por lo que es recomendable usarla para varias series con una misma frecuencia. En caso de no querer concatenar las series se debe usar un indicador a la vez. 

        Parametros
        -----------
        indicadores: str/list. Calve(s) de los indicadores a consultar. Puede ser hasta un máximo de 20 indicadores a la vez.
        nombres: list/str, opcional. Nombre(s) de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
        decimales: bool. En caso de ser verdadero regresa la serie con todos los decimales. Si es falso elimina los ceros decimales al final del punto decimal (los menos significativos).
        incremento: str, opcional. En caso de definir alguna de las opciones regresa la serie como el incremento porcentual de alguna observación previa. Las opciones disponibles son las siguientes:
                            * PorcObsAnt: Porcentaje de incremento con respecto a la observación anterior.
                            * PorcAnual: Porcentaje de incremento con respecto a la misma observación del año anterior.
                            * PorcAcumAnual: Porcentaje de incremento con respecto a la última observación del año anterior.
        ----------

        El DataFrame resultante tiene una columna por cada indicador y un DateTimeIndex con la fecha de los valores. 
        
        Para más información visitar https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#

        """
        self.__definir_valores(indicadores, nombres)
        params = self.__parametros(decimales, incremento)
        data = self.__generar_consulta('datos/oportuno', params)
        return self.__json_a_df(data)

