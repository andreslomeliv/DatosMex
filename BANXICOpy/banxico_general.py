class BanxicoGeneral:
    def __init__(self, token):
        self.__token = token
        self.__liga = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'
        self.__inicio = None
        self.__fin = None
        self.__indicadores = []

    def indicadores_a_df(self):
        dfs = []
        for indicador in self.__indicadores:
            df = self.__obtener_df(indicador)
            df.columns = [indicador]
            dfs.append(df)
        df = pd.concat(lista_df,axis=1)
        return df
        
    #Método general para obtener la serie de un indicador
    def __obtener_df(self, indicador):
        """
        Parámetros
        --------------
        indicador: str. Indicador proporcionado por el Sistema de Información Económica del 
                        Banco de México.

        --------------
        Más información en https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#
        """   
        req = requests.get(liga_banxico+indicador+'/datos',params={'token':self.__token})
        data = json.loads(req.text)
        n = len(data['bmx']['series'][0]['datos'])
        dict_df = dict(fechas = [data['bmx']['series'][0]['datos'][i]['fecha'] for i in range(n)],
                        vals = [data['bmx']['series'][0]['datos'][i]['dato'] for i in range(n)])
        df = pd.DataFrame.from_dict(dict_df)
        df.index = pd.to_datetime(df.fechas,format='%d/%m/%Y')
        df = df.drop(['fechas'],axis=1)
        df.columns = [indicador]
        return df[inicio:fin]

    