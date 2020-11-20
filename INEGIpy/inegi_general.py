######################## PEDOS #######################
# Hay pedos para manejar las fechas en los datos que no son mensuales o anuales. Esto porque el INEGI da el número
# del periodo en ve del número del mes en el que cae. Por ejemplo, el pib trimestral lo regresa con fechas
# así: [número del trimestre]/[año], entonces si dice "02/2019" indica que es el segundo trimestre del 2019 
# El pedo es que ahorita en la función self.__json_a_df() interpreta "02/2029" como febrero/2019 y no como 
# el segundo trimestre. El mismo pedo pasa con la inflación quincenal, que viene con el formato: 
# [No. de quincena]/[mes]/[año]. Entonces habrá que ver cómo hacer para que trate a los datos que no son mensuales
# o anuales bien, entendiendo la periocidad que le da el inegi a cada serie 

# en las clases/objetos como PIB.Total, PIB.PorSectores, etc., se puede arreglar agruegando un atributo que 
# indique la periocidad del dato, y que self.__json_a_df() use esa variable para determinar el formato correcto
# de las fechas. En IndicadorGeneral va a ser más pedo, pero le puedes pedir al API del INEGI los metadatos 
# donde te indica la periocidad del indicador. Sería más pedo y tendría que hacer un request extra por cada 
# indicador, pero vale la pena para evitar arreglar las fechas cada vez.

# Tal vez valdría la pena hacer clases particulares para las series con periodos no mensuales:
# serie_trimestral, serie_quincenal. Al final según yo son solo esas dos las que cambian, no he visto series 
# que se publiquen en diferentes intervalos como cada seis meses o nada así.

# Aparte de las fechas siguen habiendo errores pendejos que corregir por lo que también hace falta ir testeando
# practicamente todo para ver qué otros pedos salen. Creo que aún hay pedos en evitar que haga requests 
# innecesarios al inegi si no han cambiado las series, entre otras cosas.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json

class INEGI_General:
    
    def __init__(self, token):
        self.token = token
        self.__liga_base = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'
        self._indicadores_dict = {} # diccionario donde van las series de cada clase con su indicador y banco del inegi
        self._indicadores = [] # indicadores seleccionados para obtener el df
        self._bancos = None # bancos donde están los indicadores 
        ## ahorita se tiene que definir manualmente, estaría chido que no fuera así
        self.inicio = None # fecha de inicio del df
        self.fin = None # fecha del fin del df
        self._df = None # guarda el df para no tener que volver a pedirlo cada vez si no se cambiaron los indicadores
        self._columnas = [] # nombres de las columnas del df
        self._cambios = False # indica si cambiaron las series para volver a pedir la información al inegi
        
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
        req = requests.get(liga_api)
        print(liga_api)
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
        df.set_index(pd.to_datetime(df.fechas),inplace=True, drop=True) ### Aquí es donde se equivoca con los 
        ### periodos no mensuales ni anuales. 
        df = df.drop(['fechas'],axis=1)
        return df

    def __grafica_color(self, df):
        fig, ax = plt.subplots()
        cols = df.columns
        n = len(cols)
        palette = sns.color_palette('colorblind')
        for i in range(n):
            serie = df[cols[i]]
            serie.plot(c = palette[i], ax = ax, label=cols[i])
        return fig, ax

    def __grafica_blanco_negro(self, df):
        fig, ax = plt.subplots()
        cols = df.columns
        n = len(cols)
        linestyles = ['-','--','-.',':']
        marcadores = ['s','v','o','p','h','D']
        for i in range(n):
            serie = df[cols[i]]
            if i < 4: serie.plot(c = 'black', style = linestyles[i], ax = ax,label=cols[i])
            else: serie.plot(c = 'black', marker= marcadores[i], ax = ax,label=cols[i])
        return fig, ax
    
    ###### MÉTODOS GENERALES ######

    def obtener_df(self):
        """ 
        Regresa un objeto tipo DataFrame con la información de los indicadores proporcionada
        por el API del INEGI.
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
    
        """
        if self._df is None or self._cambios:
            lista_df = []
            for i in range(len(self._indicadores)):
                indicador = self._indicadores[i]
                banco = self._bancos[i]
                data = self.__obtener_json(indicador, banco)
                df = self.__json_a_df(data, indicador)
                lista_df.append(df)
        
            df = pd.concat(lista_df,axis=1)
            if self._bancos == ['BIE']: df = df[::-1]
            self._df = df
        if len(self._columnas) > 0: df.columns = self._columnas
        return self._df[self.inicio: self.fin]   

        
    def grafica(self, estilo = 'color', show = True, filename = None, **kwargs):
        """
        Regresa los objetos fig y ax de matplotlib con la gráfica generada. 

        Esta función no pretende remplazaroo el uso de librerías especializadas como Matplotlib o Seaborn, sino automatizar
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
        if self._df is None or self._cambios:
            df = self.obtener_df(**kwargs)
        else: df = self._df[self.inicio, self.fin]
        if estilo == 'color': fig, ax = self.__grafica_color(self._df)
        if estilo == 'blanco y negro': fig, ax = self.__grafica_blanco_negro(self._df)
        sns.despine()
        ax.set_xlabel('')
        ax.ticklabel_format(style='plain',axis='y')
        plt.tight_layout()
        
        if len(self._columnas) > 1: ax.legend(self._columnas)
        if show: plt.show()
        if filename: plt.savefig(filename)
        return fig, ax

#####################################################################################################3
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