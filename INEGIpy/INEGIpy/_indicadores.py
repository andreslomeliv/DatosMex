import pandas as pd
import requests
import json
import warnings
from numpy import nan

class Indicadores:

    def __init__(self, token):
        self.token = token
        self.base_url = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/"

        # Rangos de catálogo para determinar banco
        self.BIE_min = 656
        self.BIE_max = 1802018

        self.BISE_min = 472979
        self.BISE_max = 8999999735

    # ---------------------------------------------------------
    # Determinar banco (BIE o BISE) por rango numérico
    # ---------------------------------------------------------
    def _saber_fuente(self, indicador: str) -> str:
        indicador_int = int(indicador)

        if self.BIE_min <= indicador_int <= self.BIE_max:
            return "BIE"

        if self.BISE_min <= indicador_int <= self.BISE_max:
            return "BISE"

        raise ValueError(f"⚠️ El indicador {indicador} no aparece ni en BIE ni en BISE.")

    # ---------------------------------------------------------
    # Request genérico a la API
    # ---------------------------------------------------------
    def _request(self, url: str) -> dict:
        req = requests.get(url)
        if req.status_code != 200:
            raise Exception(
                f"⚠️ Error INEGI {req.status_code}\nURL: {url}\nRespuesta:\n{req.text}"
            )
        return json.loads(req.text)

    # ---------------------------------------------------------
    # JSON de serie → DataFrame de valores
    # ---------------------------------------------------------
    def _json_a_df(self, serie_json: dict) -> pd.DataFrame:
        serie = serie_json["OBSERVATIONS"]

        fechas = [obs["TIME_PERIOD"] for obs in serie]
        valores = [
            float(obs["OBS_VALUE"]) if obs["OBS_VALUE"] is not None else nan
            for obs in serie
        ]

        df = pd.DataFrame({"fechas": fechas, "valor": valores})
        df["fechas"] = pd.to_datetime(df["fechas"], errors="coerce")
        df = df.set_index("fechas")

        return df

    # ---------------------------------------------------------
    # JSON de serie → DataFrame de metadatos
    # ---------------------------------------------------------
    def _json_a_meta(self, serie_json: dict, nombre_columna: str, banco: str) -> pd.DataFrame:
        meta = {
            "INDICADOR": serie_json.get("INDICADOR"),
            "FREQ": serie_json.get("FREQ"),
            "TOPIC": serie_json.get("TOPIC"),
            "UNIT": serie_json.get("UNIT"),
            "UNIT_MULT": serie_json.get("UNIT_MULT"),
            "NOTE": serie_json.get("NOTE"),
            "SOURCE": serie_json.get("SOURCE"),
            "LASTUPDATE": serie_json.get("LASTUPDATE"),
            "STATUS": serie_json.get("STATUS"),
            "BANCO": banco,
        }

        meta_df = pd.DataFrame.from_dict(meta, orient="index", columns=[nombre_columna])
        return meta_df

    # ---------------------------------------------------------
    # CONSULTA PRINCIPAL
    # ---------------------------------------------------------
    def obtener_df(self, indicadores, nombres=None, clave_area="00",
                   inicio=None, fin=None, metadatos=False):
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

        
        if isinstance(indicadores, str):
            indicadores = [indicadores]

        if nombres is None:
            nombres = indicadores

        if isinstance(nombres, str):
            nombres = [nombres]

        dfs = []
        metas = []

        for ind, nombre in zip(indicadores, nombres):
            ind = str(ind)

            banco = self._saber_fuente(ind)

            url = (
                f"{self.base_url}INDICATOR/{ind}/es/{clave_area}/false/"
                f"{banco}/2.0/{self.token}?type=json"
            )

            data_json = self._request(url)
            serie_json = data_json["Series"][0]

            # Serie de valores
            df_ind = self._json_a_df(serie_json)
            df_ind.columns = [nombre]

            dfs.append(df_ind)

            # Metadatos
            if metadatos:
                meta_df = self._json_a_meta(serie_json, nombre, banco)
                metas.append(meta_df)

        # Unir indicadores por fechas
        df_final = pd.concat(dfs, axis=1)

        
        if inicio:
            df_final = df_final[df_final.index >= pd.to_datetime(inicio)]
        if fin:
            df_final = df_final[df_final.index <= pd.to_datetime(fin)]

        if metadatos:
            meta_final = pd.concat(metas, axis=1)
            return df_final, meta_final

        return df_final

    # =========================================================
    # ========   C A T Á L O G O S   D E   C Ó D I G O S  ======
    # =========================================================
    def _consultar_catalogo(self, clave: str, id_code: str, banco_api: str) -> pd.DataFrame:
        """
        clave: 'CL_INDICATOR', 'CL_FREQ', 'CL_TOPIC', etc.
        id_code: código específico o 'null'
        banco_api:
          - 'BIE-BISE' para catálogos del BIE
          - 'BISE' para catálogos del BISE
        """
        url = (
            f"{self.base_url}{clave}/{id_code}/es//{banco_api}/2.0/"
            f"{self.token}?type=json"
        )

        data = self._request(url)

        
        if "Data" in data:
            return pd.DataFrame(data["Data"])
        elif "CODE" in data:
            return pd.DataFrame(data["CODE"])
        else:
            return pd.DataFrame()

    def catalogo_indicadores(self, banco: str, indicador: str = None) -> pd.DataFrame:
        '''
        Regresa un DataFrame con la descripción de algunos o todos los indicadores de un banco. 

        Parametros
        -----------
        banco: str. ['BIE' | 'BISE'] Define el banco al cual pertenecen los indicadores. Puede ser el Banco de Indicadores Económicos (BISE) o el Banco de Información Económica (BIE).
        indicador: str, opcional. Clave del indicador a consultar. En caso de no definirse se regresan todos los indicadores del banco.
        ----------
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        '''
        banco = banco.upper()

        if banco == "BIE":
            banco_api = "BIE-BISE"
        elif banco == "BISE":
            banco_api = "BISE"
        else:
            raise ValueError("banco debe ser 'BIE' o 'BISE'.")

        id_code = "null" if indicador is None else str(indicador)

        df_cat = self._consultar_catalogo("CL_INDICATOR", id_code, banco_api)
        return df_cat

    # ---------------------------------------------------------
    # Metadatos con descripciones
    # ---------------------------------------------------------
    def consulta_metadatos(self, metadatos: pd.DataFrame) -> pd.DataFrame:
        '''
        Regresa un DataFrame con la descripción de los metadatos de una o más series. 

        Parametros
        -----------
        metadatos: DataFrame con los metadatos a consultar obtenido por la función obtener_df cuando metadatos = True. También acepta un diccionario equivalente.
        ----------
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html
        '''
            
        if isinstance(metadatos, dict):
            meta_df = pd.DataFrame(metadatos)
        else:
            meta_df = metadatos.copy()

        meta_desc = meta_df.copy()

        for col in meta_df.columns:
            banco = meta_df.loc["BANCO", col]

            # Elegir banco_api para catálogos
            banco_api = "BIE-BISE" if banco == "BIE" else "BISE"

            for idx in meta_df.index:
                if idx in ["LASTUPDATE", "BANCO", "STATUS", "NOTE"]:
                    continue

                code = meta_df.loc[idx, col]
                if code is None or str(code).strip() == "":
                    continue

                if idx == "INDICADOR":
                    clave = "CL_INDICATOR"
                else:
                    clave = f"CL_{idx}"

                try:
                    cat = self._consultar_catalogo(clave, str(code), banco_api)
                    if not cat.empty:
                        # Buscar columna tipo Description
                        desc_cols = [c for c in cat.columns if c.lower().startswith("desc")]
                        if desc_cols:
                            meta_desc.loc[idx, col] = cat.iloc[0][desc_cols[0]]
                except Exception:
                    
                    pass

        return meta_desc
