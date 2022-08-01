import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class Banxico:
    def __init__(self, token):
        self.__token = token
        self.__liga_base = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'
        self._indicadores = list()
        self._columnas = list()

    def __indicador_a_df(self, indicador):
        """
        Parámetros
        --------------
        indicador: str. Indicador proporcionado por el Sistema de Información Económica del 
                        Banco de México.

        --------------
        Más información en https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#
        """   
        req = requests.get(self.__liga_base + indicador +'/datos',params={'token':self.__token})
        data = json.loads(req.text)
        n = len(data['bmx']['series'][0]['datos'])
        dict_df = dict(fechas = [data['bmx']['series'][0]['datos'][i]['fecha'] for i in range(n)],
                        vals = [data['bmx']['series'][0]['datos'][i]['dato'] for i in range(n)])
        df = pd.DataFrame.from_dict(dict_df)
        df.index = pd.to_datetime(df.fechas,format='%d/%m/%Y')
        df = df.drop(['fechas'],axis=1)
        df.columns = [indicador]
        df[indicador] = df[indicador].str.replace('N/E', 'NaN').astype(float)
        return df

    def _generar_consulta(self, inicio, fin):

        lista_df = []
        for indicador in self._indicadores:
            df = self.__indicador_a_df(indicador)
            lista_df.append(df)
    
        df = pd.concat(lista_df,axis=1)
        df.columns = self._columnas

        return self._df[inicio:fin] 

    def obtener_df(self, 
                   indicadores: 'str|list', 
                   nombres: 'str|list' = None, 
                   inicio: str = None, 
                   fin: str = None):
        """
        Regresa un DataFrame con la información de los indicadores proporcionada por el API del Banxico.

        Parametros
        -----------
        indicadores: str/list. Lista con los indicadores de las series a obtener. 
        nombres: list/str, opcional. Lista con los nombres de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
                    También se puede especificar en INEGI.IndicadorGeneral.indicadores()
        inicio: str, opcional. Fecha donde iniciar la serie. De no proporcionarse será desde el primer valor disponible. 
        fin: str, opcional. Fecha donde terminar la serie. De no proporcionarse será hasta el último valor disponible. 
        ----------

        El DataFrame resultante tiene una columna por cada indicador y un DateTimeIndex con la fecha de los valores. 
        
        Para más información visitar https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#

        """
        
        self._indicadores = indicadores
        if nombres: self._columnas = nombres
        else: self._columnas = indicadores

        
        if isinstance(self._columnas, str): self._columnas = [self._columnas]
        if isinstance(self._indicadores, str): self._indicadores = [self._indicadores]
        return self._generar_consulta(inicio, fin)





# ##################### Graficar ######################

#     def __cambiar_lineas(self, ax, estilo):
#         if estilo == 'colores':
#             self.__cambiar_colores(ax)
#         if estilo == 'blanco y negro':
#             self.__cambiar_estilos(ax)
#         ax.legend(self._columnas)

#     def __cambiar_estilos(self, ax):
#         # checar cuál es la mejor manera de elejir los estilos
#         line_styles = ['-','-.','--',':']
#         markers = ['o','v','s','x','D']
#         for i, line in enumerate(ax.get_lines()):
#             if i <= 3: line.set_linestyle(line_styles[i])
#             else: line.set_marker(markers[i-4])

#     def __cambiar_colores(self, ax):
#         palette = sns.color_palette('colorblind',len(self._columnas))[::-1]
#         for i, line in enumerate(ax.get_lines()):
#             line.set_color(palette[i])

#     def grafica(self, estilo = 'colores', show = True, filename = None, **kwargs):
#         """
#         Construye un gráfico con la consulta definida. En caso de querer cambiar la consulta se pueden indicar los parámetros
#         deseados: inicio, fin, indicador, serie, o cualquiera de los parámetros particulares de la serie.

#         NOTA:
#         Esta función no pretende remplazar el uso de librerías especializadas como Matplotlib o Seaborn, sino automatizar
#         estilos de gráficas que puedan ser de uso común. Por ello, la gráfica generada tiene solo ciertos estilos disponibles. 
#         Para darle un estilo particular o agregar nuevos elementos es recomendado usar alguna de las librerías especializadas
#         directamente con los datos o para manipular los objetos fig y ax que regresa esta función. 

#         Parámetros
#         -----------
#         estilo -- str. ACEPTA: ['colores' (default) | 'blanco y negro']. Estilo de la gráfica. Actualmente solo existen 
#         dos estilos: 'colores' y 'blanco y negro'.
#         show -- bool. Define si mostrar o no la gráfica. Equivalente a plt.show()
#         filename -- nombre y dirección donde guardar la gráfica. Equivalente a plt.savefig()
#         -----------

#         Regresa los objetos fig y ax de matplotlib con la gráfica generada. 

#         """
#         df = self.obtener_df(**kwargs)
#         color = 'blue' if estilo == 'colores' else 'black'
#         fig, ax = plt.subplots()
#         df.plot(ax=ax,color=color)
#         ax.legend().remove()
#         if len(df.columns)>1: self.__cambiar_lineas(ax, estilo)
#         sns.despine()
#         ax.set_xlabel('')
#         ax.ticklabel_format(style='plain',axis='y')
#         plt.tight_layout()
        
#         if show: plt.show()
#         if filename: plt.savefig(filename)
#         return fig, ax