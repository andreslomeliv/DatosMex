import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json

class INEGI_General:
    
    def __init__(self, token):
        self.token = token
        self.__liga_base = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'
        self._indicadores_dict = {}
        self._indicadores = []
        self._bancos = None
        self.inicio = None
        self.fin = None
        self.serie = []
        self._df = None
        self._columnas = []
        
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
    
    def __json_a_df(self, data):
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
                'valor':[float(data['Series'][0]['OBSERVATIONS'][i]['OBS_VALUE']) for i in range(obs_totales)]}
        df = pd.DataFrame.from_dict(dic)
        df.set_index(pd.to_datetime(df.fechas),inplace=True, drop=True)
        df = df.drop(['fechas'],axis=1)
        return df

    def __pretty_printer(self, dictionary, niveles = None):
        indent = 0
        for key, value in dictionary.items():
            print('\t'*indent + key)
            if type(value) is dict:
                self.__pretty_printer(value, indent+2)

    def _cambiar_lineas(self, ax, estilo):
        pass

    
    ###### MÉTODOS GENERALES ######
    def series_disponibles(self):
        """
        Regresa los niveles de series disponibles en cada clase. 
        """
        self.__pretty_printer(self._indicadores_dict)

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
                df = self.__json_a_df(data)
                lista_df.append(df)
        
            df = pd.concat(lista_df,axis=1)
            df.columns = self._columnas
            if self._bancos == ['BIE']: df = df[::-1]
            self._df = df
        return self._df[self.inicio:self.fin]   

        
    def grafica(self, estilo = 'colores', show = True, filename = None):
        """
        Regresa los objetos fig y ax de matplotlib con la gráfica generada. 

        Esta función no pretende remplazar el uso de librerías especializadas como Matplotlib o Seaborn, sino automatizar
        estilos de gráficas que puedan ser de uso común. Por ello, la gráfica generada tiene solo ciertos estilos disponibles. 
        Para darle un estilo particular o agregar nuevos elementos es recomendado usar alguna de las librerías especializadas
        directamente con los datos o para manipular los objetos fig y ax que regresa esta función. 

        Parámetros
        -----------
        estilo -- str. ACEPTA: ['colores' (default) | 'blanco y negro']. Estilo de la gráfica. Actualmente solo existen 
        dos estilos: 'colores' y 'blanco y negro'.
        show -- bool. Define si mostrar o no la gráfica. Equivalente a plt.show()
        filename -- nombre y dirección donde guardar la gráfica. Equivalente a plt.savefig()
        -----------
        """
        if self._df is None:
            self.obtener_df()
        color = 'blue' if estilo == 'colores' else 'black'
        fig, ax = plt.subplots()
        self._df.plot(ax=ax,color=color)
        ax.legend().remove()
        if len(self._df.columns)>1: self._cambiar_lineas(ax, estilo)
        sns.despine()
        ax.set_xlabel('')
        ax.ticklabel_format(style='plain',axis='y')
        plt.tight_layout()
        
        if show: plt.show()
        if filename: plt.savefig(filename)
        return fig, ax


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
        return self

    def serie_actual(self):
        return self.serie

    def definir_serie(self, serie):
        """
        serie -- lista con los niveles de información de la serie a obtener. 
        Para mayor información ver self.series_disponilbes
        """
        self.serie = serie
        return 
              
##################################################################################