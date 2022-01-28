import requests
import json
import pandas as pd

class IndicadorGeneral:
    def __init__(self, token):
        self.__token = token
        self.__liga_base = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'
        self._inicio = None
        self._fin = None
        self._indicadores = []
        
    #Método general para obtener la serie de un indicador
    def obtener_df(self, indicador):
        """
        Parámetros
        --------------
        indicador: str. Indicador proporcionado por el Sistema de Información Económica del 
                        Banco de México.

        --------------
        Más información en https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#
        """   
        req = requests.get(self.__liga_base + indicador+'/datos',params={'token':self.__token})
        data = json.loads(req.text)
        n = len(data['bmx']['series'][0]['datos'])
        dict_df = dict(fechas = [data['bmx']['series'][0]['datos'][i]['fecha'] for i in range(n)],
                        vals = [data['bmx']['series'][0]['datos'][i]['dato'] for i in range(n)])
        df = pd.DataFrame.from_dict(dict_df)
        df.index = pd.to_datetime(df.fechas,format='%d/%m/%Y')
        df = df.drop(['fechas'],axis=1)
        df.columns = [indicador]
        return df[self._inicio:self._fin]