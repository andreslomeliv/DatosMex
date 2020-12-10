######################## Problemas #######################
# Ya se resolvieron los problemas con la frecuencia de las fechas, aunque no está probado por completo y aún 
# faltan incorporar las frecuencias semanals y decenales o las series con frecuencia irregular
# Mentira, es mejor usa pd.PeriodIndex, hay quue ver qué pedo con eso.

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

        # en el json que regresa el API del inegi viene un valor que indica la frecuencia de la serie, este dicionario
        # tiene como llaves el indicador que le da el INEGI a la frecuencia y como valores el número por el que 
        # se tiene que multiplicar el mes o el día para que la fecha quede en formato Año/mes/día o Año/mes
        # en vez de Año/ No. de periodo, como lo organiza el INEGI. Entonces se leería como:
        # {'4': semestral (el mes se multiplica por 6), '5', cuatrimestral (mes multiplicado por 3), etc..}
        # para más información de cómo organiza las frecuencias el API del INEGI ver los metadatos en el constructor
        # de consultas.
        # Me salté los indicadores anuales o mensuales porque pandas no tiene problemas leyendo esos así como vienen
        # tampoco he incorporado los indicadores decenales ni semanales. 
        self._frecuencias_inegi = {'4':6, '5':4, '6':3, '7':2, '9':15}
        # Esta variable contiene la periodozación particular de la serie, como es un valor por el que se
        # va a multiplicar el mes o el día, por default es igual a 1 para que no haga cambios de no ser 
        # necesario
        self._frecuencia_serie = 1

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
        freq = data['Series'][0]['FREQ']

        dic = {'fechas':[data['Series'][0]['OBSERVATIONS'][i]['TIME_PERIOD'] for i in range(obs_totales)],
                indicador:[float(data['Series'][0]['OBSERVATIONS'][i]['OBS_VALUE']) for i in range(obs_totales)]}

        # Define la frecuencia de la serie
        if freq in self._frecuencias_inegi.keys():
            self._frecuencia_serie = self._frecuencias_inegi[freq]
            dic['fechas'] = self.__formatear_fechas(dic['fechas'])

        df = pd.DataFrame.from_dict(dic)
        df.set_index(pd.to_datetime(df.fechas),inplace=True, drop=True) 
        df = df.drop(['fechas'],axis=1)
        return df

    def __formatear_fechas(self, fechas):
        nuevas_fechas = list()
        for fecha in fechas:
            fecha = fecha.split('/')
            fecha[-1] = str(int(fecha[-1])*self._frecuencia_serie)
            fecha = '/'.join(fecha)
            nuevas_fechas.append(fecha)
        return nuevas_fechas

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

    def obtener_df(self, **kwargs):
        """ 
        Regresa un objeto tipo DataFrame con la información de los indicadores proporcionada
        por el API del INEGI.
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
    
        """
        for key, value in kwargs.items():
            if key == 'inicio': self.inicio  = value
            if key == 'fin': self.fin = value

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
            self._cambios = False
        if len(self._columnas) > 0: self._df.columns = self._columnas
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
        df = self.obtener_df(**kwargs)
        if estilo == 'color': fig, ax = self.__grafica_color(df)
        if estilo == 'blanco y negro': fig, ax = self.__grafica_blanco_negro(df)
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