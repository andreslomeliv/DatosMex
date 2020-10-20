import pandas as pd
import requests
import json

class INEGI_General:
    
    def __init__(self, token):
        self.token = token
        self._liga_base = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'

    def __obtener_json(self, indicador, banco):
        """ 
    
        Construye la liga de consulta y obtiene la información resultante del API del
        INEGI. Esta función es principalmente para uso interno como en indicador_a_df().
        
        Parámetros:
        ------------
        token: str. Token para acceder al API. 
        
        indicadores: str.  Número del indicador a buscar.
        
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
        liga_api = self._liga_base + indicador + idioma + '0700/false/' + banco + final_liga
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
    
    def _indicadores_a_df(self, indicadores, bancos, inicio, fin):
        """ 
        
        Construye un DataFrame con la información resultante del API del INEGI de 
        varios indicadores a la vez. 
    
        Parámetros:
        -----------        
        indicadores: list. Lista con los números de los indicadores a buscar.
        
        bancos: list. Lista con el banco de información en donde se encuentra los
                      indocadores. Puede ser 'BIE' o 'BISE'. 
           
        inicio: str. Fecha de inicio y fin de la serie. Formato: "%Y/%m"            
        ------------
    
        Regresa un objeto tipo DataFrame con la información de los indicadores proporcionada
        por el API del INEGI.
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
    
        """
        lista_df = []
        
        for i in range(len(indicadores)):
            indicador = indicadores[i]
            banco = bancos[i]
            data = self.__obtener_json(indicador, banco)
            df = self.__json_a_df(data, indicador)
            df.columns = [indicador]
            lista_df.append(df)
       
        df = pd.concat(lista_df,axis=1)
        return df[inicio:fin]    