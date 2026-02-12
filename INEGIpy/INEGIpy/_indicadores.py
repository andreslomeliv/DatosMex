import pandas as pd
import requests
import json
import warnings
from numpy import nan
from importlib.resources import files


class Indicadores:
    
    def __init__(self, token: str):
        self.token: str = token # token proporcionado por el INEGI único para cada usuario
        self._liga_base = 'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/' 
        
        # diccionario con la clave de frecuencia del INEGI y el factor por el cual se debe multiplicar
        # el último valor para pasarlo a su mes correspondiente
        # Ejemplo: una serie semestral tiene como clave de frecuencia '4', esto indica que para cada año van
        # a haber dos periodos indicando los dos semestres: "2020/01, 2020/02"
        # El factor del diccionario indicaría que al último dígito lo multiplicamos por 6 para pasarlo a meses
        # las claves que no se encuentran en el diccionario son irregulares y no se van a operar
        self._frecuencias_dict: dict = {
            'BIE': {
                '3':(1,'Y'), # anual
                '4':(3,'Q'), # trimestral
                '8':(1,'M'), # mensual
                '15':(14,'SM') # quincenal
            },
            'BISE': {
                '1':(1,'Y'), # decenal
                '3':(1,'Y'), # anual
                '4':(3,'Q'), # trimestral
                '7':(1,'Y'), # quinquenal
                '8':(1,'M'), # mensual
                '9':(1,'Y'), # bienal
                '16':(1,'Y') # trienal
            }
        }

        # Rangos de catálogo para determinar banco
        self._indcadores_bie = self._cargar_ids()
        
        
############## Obtener Data Frame ########################

# Se definen  los métodos internos y públicos necesarios para obtener la serie y pasarla a un DataFrame

    def __request(self, url: str) -> dict:
        req = requests.get(url)
        if req.status_code != 200:
            raise Exception(
                f"Error INEGI {req.status_code}\nURL: {url}\nRespuesta:\n{req.text}"
            )
        return json.loads(req.text)

    # determinar el banco al cual pertenece el indicador
    def _cargar_ids(self):
        path = files('INEGIpy') / 'data' / 'catalogo_bie.txt'
        with path.open("r", encoding="utf-8") as f:
            return {line.strip() for line in f}
   
    def __obtener_banco(self, indicador: str) -> str:

        if indicador in self._indcadores_bie:
            return "BIE"
        else:
            return "BISE"

        # raise ValueError(f"El indicador {indicador} no aparece ni en BIE ni en BISE.")
    
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
        serie = data.pop('OBSERVATIONS') #con esto se separa la serie real de los metadatos

        # construcción de la serie
        obs_totales = len(serie)
        dic = {
            'fechas': [serie[i]['TIME_PERIOD'] for i in range(obs_totales)],
            'valor': [
                float(serie[i]['OBS_VALUE']) if serie[i]['OBS_VALUE'] not in (None, '') else nan
                for i in range(obs_totales)
            ]
        }

        """
        Se modificó el diccionario 'dic' en la clave 'valor':

        Antes:
            'valor': [float(serie[i]['OBS_VALUE']) if serie[i]['OBS_VALUE'] is not None else nan for i in range(obs_totales)]

        Este código ocasionaba un error en consultas a DENUE donde el dato existía pero estaba en formato string vacío: ''.

        Corrección:
            'valor': [
                float(serie[i]['OBS_VALUE']) if serie[i]['OBS_VALUE'] not in (None, '') else nan
                for i in range(obs_totales)
            ]

        Esta modificación evita el error al convertir cadenas vacías a float, permitiendo exportar valores nulos como nan y dejando al usuario la validación de la información.
        """

        df = pd.DataFrame.from_dict(dic)
        frecuencia = data['FREQ']
        factor, period = self._frecuencias_dict[banco].get(frecuencia) # factor que multiplica el periodo para pasar a fecha y periodo de pd
        if factor: 
            try: 
                cambio_fechas = lambda x: '/'.join(x.split('/')[:-1] + [str(int(x.split('/')[-1])*factor)])
                df["fechas"] = df["fechas"].apply(cambio_fechas)
                if period == 'SM': 
                    df["fechas"] = pd.to_datetime(df["fechas"], format='%Y/%m/%d')
                    df["fechas"] = df["fechas"] + pd.offsets.SemiMonthBegin()
                elif period == 'Y':
                    df["fechas"] = pd.to_datetime(df["fechas"], format='%Y')
                else:
                    df["fechas"] = pd.to_datetime(df["fechas"], format='%Y/%m')

                df = df.set_index("fechas")

            except:
                df["fechas"] = dic["fechas"]
                df = df.set_index("fechas")
                warnings.warn('No se pudo interpretar la fecha correctamente por lo que el índice no es tipo DateTime')
        else:
            df = df.set_index("fechas")
            warnings.warn('No se pudo interpretar la fecha correctamente por lo que el índice no es tipo DateTime')

        # construcción de metadatos
        data['BANCO'] = banco
        meta = pd.DataFrame.from_dict(data, orient='index', columns=['valor'])
            
        return df, meta
    
    def obtener_df(self, 
                   indicadores: 'str|list', 
                   nombres: 'str|list' = None, 
                   clave_area: str = '00',
                   inicio: str = None, 
                   fin: str = None, 
                   banco: str = None, 
                   metadatos: bool = False):
        """
        Regresa un DataFrame con la información de los indicadores proporcionada por el API del INEGI. Si metadatos = True regresa un segundo DataFrame con las claves de los metadatos del indicador. 

        Parametros
        -----------
        indicadores: str/list. Clave(s) de los indicadores a consultar.
        nombres: list/str, opcional. Nombre(s) de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
        clave_area: str. Clave de dos a cinco caracteres que indentifica el área geográfica de acuerdo con el Marco Geoestadístico. Para definir el total nacional se especifica '00'. Este campo solo aplica para los indicadores del Bando de Indicadores (BISE), no aplica para los del Banco de Información Económica (BIE).
                                    Dos dígitos para incluir nivel estatal (ej.01 a 32).
                                    Cinco dígitos dígitos para incluir nivel municipal (ej. 01001).
        inicio: str, opcional. Fecha donde iniciar la serie en formato YYYY(-MM-DD). De no proporcionarse será desde el primer valor disponible. 
        fin: str, opcional. Fecha donde terminar la serie en formato YYYY(-MM-DD). De no proporcionarse será hasta el último valor disponible.
        banco: str, opcional. ['BIE' | 'BISE'] Define el banco al cual pertenecen los indicadores. Puede ser el Banco de Indicadores Económicos (BISE) o el Banco de Información Económica (BIE). Ya que solamente tres claves de indicadores se encuentran en ambos bancos y el resto son diferentes, no es necesario definir este parámetro a menos que los indicadores a consultar sea alguno de los siguientes: ['539260', '539261', '539262'].
        metadatos: bool. En caso se ser verdadero regresa un DataFrame con los metadatos de los indicadores.
        ----------
        
        El DataFrame resultante tiene una columna por cada indicador y un DateTimeIndex con la fecha de los valores. 
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        """
        if nombres is None: 
            nombres = indicadores

        if isinstance(indicadores, str): 
            indicadores = [indicadores]

        if isinstance(nombres, str): 
            nombres = [nombres]

        if len(indicadores) != len(nombres): 
            warnings.warn('Los nombres no coinciden con el número de indicadores, se usan los indicadores como nombre de las columnas.')
            nombres = indicadores
            
        if banco is not None:
            warnings.warn(
                "El parámetro 'banco' está deprecado y será eliminado en versones futuras. Actualmente no tiene efecto.",
                DeprecationWarning,
                stacklevel=2
            )
        
        lista_dfs = list()
        meta_dfs = list()
        for i in range(len(indicadores)):
            indicador = indicadores[i]
            banco = self.__obtener_banco(indicador)
            if banco == "BIE":
                clave_banco = "BIE-BISE" # la version actual del API nombre la clave del BIE cambia a BIE-BISE
            else:
                clave_banco = banco
            url = (
                f"{self._liga_base}INDICATOR/{indicador}/es/{clave_area}/false/"
                f"{clave_banco}/2.0/{self.token}?type=json"
            )
            data = self.__request(url)
            series = data['Series'][0]
            df, meta = self.__json_a_df(series, banco)
            
            # Invierte el orden de las fechas
            df = df[::-1]
            
            lista_dfs.append(df)
            meta_dfs.append(meta)

        df = pd.concat(lista_dfs,axis=1)
        meta_df = pd.concat(meta_dfs, axis=1)

        if len(df.columns) == len(nombres): 
            df.columns = nombres
            meta_df.columns = nombres
        else: 
            warnings.warn('Los nombres no coinciden con el número de indicadores, se usan los indicadores como nombre de las columnas.')
            df.columns = indicadores
            meta_df.columns = indicadores

        if metadatos: 
            return df[inicio:fin], meta_df
        else: 
            return df[inicio:fin] 

## Catalogo de Metadatos

    def _consultar_catalogo(self, clave, id, banco):
        liga = f'{self._liga_base}{clave}/{id}/es/{banco}/2.0/{self.token}/?type=json'
        req = requests.get(liga)
        data = json.loads(req.text)
        return pd.DataFrame(data['CODE'])

    def catalogo_indicadores(self, 
                             banco: str, 
                             indicador: str = None):
        '''
        Regresa un DataFrame con la descripción de algunos o todos los indicadores de un banco. 

        Parametros
        -----------
        banco: str. ['BIE' | 'BISE'] Define el banco al cual pertenecen los indicadores. Puede ser el Banco de Indicadores Económicos (BISE) o el Banco de Información Económica (BIE).
        indicador: str, opcional. Clave del indicador a consultar. En caso de no definirse se regresan todos los indicadores del banco.
        ----------
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        '''
        if indicador is None: 
            indicador = 'null'

        if banco == 'BIE': 
            banco = 'BIE-BISE'
            
        return self._consultar_catalogo('CL_INDICATOR', indicador, banco)

    def consulta_metadatos(self, 
                           metadatos: pd.DataFrame|dict):
        '''
        Regresa un DataFrame con la descripción de los metadatos de una o más series. 

        Parametros
        -----------
        metadatos: DataFrame con los metadatos a consultar obtenido por la función obtener_df cuando metadatos = True. También acepta un diccionario equivalente.
        ----------
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        '''
        if isinstance(metadatos, dict): metadatos = pd.DataFrame.from_dict(dict)
        n_df = metadatos.copy(deep=True)
        for col in metadatos.columns:
            banco = metadatos.loc['BANCO',col]
            for idx in metadatos.index: 
                if idx in ['LASTUPDATE','BANCO']: continue
                id = metadatos.loc[idx,col]
                if id is None or len(id) == 0: continue
                if idx == 'INDICADOR': clave = 'CL_INDICATOR'
                else: clave = 'CL_{}'.format(idx)
                try:
                    desc = self._consultar_catalogo(clave, id, banco)
                    n_df.loc[idx,col] = desc.iloc[0,1]
                except: n_df.loc[idx,col] = 'No hay información'

        return n_df