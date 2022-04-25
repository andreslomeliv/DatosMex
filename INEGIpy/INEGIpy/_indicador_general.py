# Aún quedan periodozaciones que no se han resuelto por ser irregulares o por no poder encontrar ejemplos para
# ver qué se tiene que hacer. Por ejemplo, las series decenales y semanales se pueden incorporar sin problema
# pero no encuentro series con esas periocidades para ver el formato que usan. Estoy a la espera de que me 
# me ayuden con esto.


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json

class IndicadorGeneral:
    
    def __init__(self, token):
        self.__token = token # token proporcionado por el INEGI único para cada usuario
        self.__liga_base = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/'
        # vriables para la consulta
        self._indicadores = list() # lista con los indicadores a consultar. cada módulo la llena con sus especificaciones
        self._bancos = list() # lista con los bancos de los indicadores
        self.inicio = None # fecha de inicio de la serie
        self.fin = None # fecha de fin de la serie
        self._df = None # atributo interno con el último DataFrame consultado. Evita llamar al API si no cambiaron los indicadores
        self._columnas = list() # nombres de las columnas. En los módulos de series se llena automáticamente.
        self._indicadores_previos = list() # lista con indicadores previos. Evita llamar al API si no cambiaron los indicadores.
        # diccionario con la clave de frecuencia del INEGI y el factor por el cual se debe multiplicar
        # el último valor para pasarlo a su mes correspondiente
        # Ejemplo: una serie semestral tiene como clave de frecuencia '4', esto indica que para cada año van
        # a haber dos periodos indicando los dos semestres: "2020/01, 2020/02"
        # El factor del diccionario indicaría que al último dígito lo multiplicamos por 6 para pasarlo a meses
        # las claves que no se encuentran en el diccionario son irregulares y no se van a operar
        self.__frecuancias_dict = {'BIE': {'1':(1,'Y'), '2':(1,'Y'), '3':(1,'Y'), '4':(6,'M'), '5':(4,'M'), '6':(3,'Q'), 
                                            '7':(2,'M'), '8':(1,'M'), '9':(14,'SM')},
                                    'BISE': {'1':(1,'Y'), '3':(1,'Y'), '4':(3,'Q'), '7':(14,'SM'), '8':(1,'M'), '9':(1,'Y'), '16':(1,'Y')}}
        
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
        if banco: 
            liga_api = '{}{}/es/0700/false/{}/2.0/{}?type=json'.format(self.__liga_base, indicador, banco, str(self.__token))
            data = self.__request(liga_api)
        else:
            try: 
                banco = 'BIE'
                liga_api = '{}{}/es/0700/false/{}/2.0/{}?type=json'.format(self.__liga_base, indicador, banco, str(self.__token))
                data = self.__request(liga_api)
            except: 
                banco = 'BISE'
                liga_api = '{}{}/es/0700/false/{}/2.0/{}?type=json'.format(self.__liga_base, indicador, banco, str(self.__token))
                data = self.__request(liga_api)

        return data, banco
    
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
        obs_totales = len(data['Series'][0]['OBSERVATIONS'])
        dic = {'fechas':[data['Series'][0]['OBSERVATIONS'][i]['TIME_PERIOD'] for i in range(obs_totales)],
                'valor':[float(data['Series'][0]['OBSERVATIONS'][i]['OBS_VALUE']) for i in range(obs_totales)]}
        df = pd.DataFrame.from_dict(dic)
        frecuencia = data['Series'][0]['FREQ']
        factor, period = self.__frecuancias_dict[banco].get(frecuencia) # factor que multiplica el periodo para pasar a fecha y periodo de pd
        if factor: 
            cambio_fechas = lambda x: '/'.join(x.split('/')[:-1] + [str(int(x.split('/')[-1])*factor)])
            df.fechas = df.fechas.apply(cambio_fechas)
            df.set_index(pd.to_datetime(df.fechas),inplace=True, drop=True)
            df = df.drop(['fechas'],axis=1)
            if period == 'SM': df.index = df.index + pd.offsets.SemiMonthBegin()
        else:
            df.set_index(df.fechas,inplace=True, drop=True)
            df = df.drop(['fechas'],axis=1)
        return df

    # en este módulo solo se definen inicio y fin como variables ya que son las únicas que necesariamente están en
    # cada módulo. El resto de las variables se van definiendo en los módulos que hereden esta clase. 
    def obtener_df(self, inicio, fin):
        if inicio: self.inicio = inicio
        if fin: self.fin = fin
        
        if isinstance(self._indicadores, str): self._indicadores = [self._indicadores]
        if isinstance(self._bancos, str): self._bancos = [self._bancos]

        if self._df is None or self._indicadores != self._indicadores_previos:
            self._indicadores_previos = self._indicadores
            lista_df = []
            for i in range(len(self._indicadores)):
                indicador = self._indicadores[i]
                try: banco = self._bancos[i]
                except: banco = None
                data, banco = self.__obtener_json(indicador, banco)
                df = self.__json_a_df(data, banco)
                if banco == 'BIE': df = df[::-1]
                lista_df.append(df)
        
            df = pd.concat(lista_df,axis=1)
            df.columns = self._columnas
            self._df = df

        return self._df[self.inicio:self.fin] 

##################### Graficar #######################

# define los métodos públicos e internos para elaborar una gráfica base con la serie consultada
# por default utiliza la última consulta generada o definida aunque se puede redefinir variables de la consulta 
# dentro de la función.

    def __cambiar_lineas(self, ax, estilo):
        if estilo == 'colores':
            self.__cambiar_colores(ax)
        if estilo == 'blanco y negro':
            self.__cambiar_estilos(ax)
        ax.legend(self._columnas)

    def __cambiar_estilos(self, ax):
        # checar cuál es la mejor manera de elejir los estilos
        line_styles = ['-','-.','--',':']
        markers = ['o','v','s','x','D']
        for i, line in enumerate(ax.get_lines()):
            if i <= 3: line.set_linestyle(line_styles[i])
            else: line.set_marker(markers[i-4])

    def __cambiar_colores(self, ax):
        palette = sns.color_palette('colorblind',len(self._columnas))[::-1]
        for i, line in enumerate(ax.get_lines()):
            line.set_color(palette[i])

    def grafica(self, estilo = 'colores', show = True, filename = None, **kwargs):
        """
        Construye un gráfico con la consulta definida. En caso de querer cambiar la consulta se pueden indicar los parámetros deseados: inicio, fin, indicador, serie, o cualquiera de los parámetros particulares de la serie.

        NOTA:
        Esta función no pretende remplazar el uso de librerías especializadas como Matplotlib o Seaborn, sino automatizar estilos de gráficas que puedan ser de uso común. Por ello, la gráfica generada tiene solo ciertos estilos disponibles. 
        Para darle un estilo particular o agregar nuevos elementos es recomendado usar alguna de las librerías especializadas directamente con los datos o para manipular los objetos fig y ax que regresa esta función. 

        Parámetros
        -----------
        estilo -- str. ACEPTA: ['colores' (default) | 'blanco y negro']. Estilo de la gráfica. Actualmente solo existen 
        dos estilos: 'colores' y 'blanco y negro'.
        show -- bool. Define si mostrar o no la gráfica. Equivalente a plt.show()
        filename -- nombre y dirección donde guardar la gráfica. Equivalente a plt.savefig()
        -----------

        Regresa los objetos fig y ax de matplotlib con la gráfica generada. 

        """
        df = self.obtener_df(**kwargs)
        color = 'blue' if estilo == 'colores' else 'black'
        fig, ax = plt.subplots()
        df.plot(ax=ax,color=color)
        ax.legend().remove()
        if len(self._df.columns)>1: self.__cambiar_lineas(ax, estilo)
        sns.despine()
        ax.set_xlabel('')
        ax.ticklabel_format(style='plain',axis='y')
        plt.tight_layout()
        
        if show: plt.show()
        if filename: plt.savefig(filename)
        return fig, ax

    