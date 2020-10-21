import pandas as pd
import pprint
import requests
import json

class INEGI_General:
    
    def __init__(self, token):
        self.token = token
        self.__liga_base = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'
        self._indicadores_dict = {}
        self._indicadores = None
        self._bancos = None
        self.inicio = None
        self.fin = None
        self.serie = []
        self._df = None
        
    ##### MÉTODOS INTERNOS #####

    def __obtener_json(self, indicador, banco):
        """ 
    
        Construye la liga de consulta y obtiene la información resultante del API del
        INEGI. 
        
        Parámetros:
        ------------
        
        indicador: str.  Número del indicador a buscar.
        
        banco: str. Banco de información donde se encuentra el indocador. Puede ser 
                    'BIE' o 'BISE'.
        
       -------------
    
        Regresa un diccionario con la información del indicador proporcionada por el API
        del INEGI en formato JSON. 
    
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
    
        """
        indicador = indicador + '/'
        idioma = 'es/'
        banco = banco + '/2.0/'
        final_liga = str(self.token) + '?type=json'
        liga_api = self.__liga_base + indicador + idioma + '0700/false/' + banco + final_liga
        print(liga_api)
        req = requests.get(liga_api)
        print(req)
        data = json.loads(req.text)
        return data
    
    def __json_a_df(self, data, indicador):
        """ 
        
        Construye un DataFrame con la información resultante del API del INEGI de 
        un solo indicador a la vez.
    
        Parámetros:
        -----------
        data: Dict. JSON obtendio del API del INEGI.
        indicador: str. Se utiliza el indicador de la serie aunque realmente sirve como nombre de 
                        columna.
        -----------
        
        Regresa un objeto tipo DataFrame con la información del indicador proporcionada por el API
        del INEGI en formato JSON. 
    
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
    
        """
        obs_totales = len(data['Series'][0]['OBSERVATIONS'])
        dic = {'fechas':[data['Series'][0]['OBSERVATIONS'][i]['TIME_PERIOD'] for i in range(obs_totales)],
                indicador:[float(data['Series'][0]['OBSERVATIONS'][i]['OBS_VALUE']) for i in range(obs_totales)]}
        df = pd.DataFrame.from_dict(dic)
        df.set_index(pd.to_datetime(df.fechas),inplace=True, drop=True)
        df = df.drop(['fechas'],axis=1)
        return df
    
    ###### MÉTODOS GENERALES ######

    def obtener_df(self):
        """ 
        Regresa un objeto tipo DataFrame con la información de los indicadores proporcionada
        por el API del INEGI.
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
    
        """
        if self._df is None:
            lista_df = []
            
            for i in range(len(self._indicadores)):
                indicador = self._indicadores[i]
                banco = self._bancos[i]
                data = self.__obtener_json(indicador, banco)
                df = self.__json_a_df(data, indicador)
                df.columns = [indicador]
                lista_df.append(df)
        
            df = pd.concat(lista_df,axis=1)
            if self._bancos == ['BIE']: df = df[::-1]
            self._df = df[self.inicio:self.fin]   
        return self._df

    def series_disponibles(self):
        """
        Regresa los niveles de series disponibles en cada clase. 
        """
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self._indicadores_dict)

#################################################################################
# Considerando si borrar estos métodos y solo hacerlos accesibles a través de los
# atributos públicos como self.serie, self.inicio, etc. Por el momento son ambas 
# maneras y que a cada quién use la qeu se acomode mejor.
#################################################################################

    def periodo(self): 
        """
        Regresa los años que utilizados para consultar la serie.
        """ 
        return (self.inicio, self.fin)
    
    def definir_periodo(self, inicio, fin):
        """
        """
        self.inicio = inicio
        self.fin = fin
        if self._df: self._df[inicio:fin]
        return self

    def serie_actual(self):
        return self.serie

    def definir_serie(self, serie):
        """
        serie -- list. [valor, tipo de serie], ejemplo: ['real','trimestral desestacionalizada']. Para ver las 
        series disponibles ver self.series_disponibles()
        """
        self.serie = serie
        return 
              
##################################################################################