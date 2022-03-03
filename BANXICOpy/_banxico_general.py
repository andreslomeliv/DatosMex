from ._indicador_general import IndicadorGeneral

class Banxico(IndicadorGeneral):
    def __init__(self, token):
        super().__init__(token)
        self.indicadores = list()
        self.nombres = list()

    def obtener_df(self, indicadores = None, nombres = None, inicio = None, fin = None):
        """
        Regresa un DataFrame con la información de los indicadores proporcionada por el API del Banxico.
        Para más información visitar https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#

        Parametros
        -----------
        indicadores: list/str. Lista con los indicadores de las series a obtener. También se puede especificar 
                    en INEGI.IndicadorGeneral.indicadores
        nombres: list/str. Lista con los nombres de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
                    También se puede especificar en INEGI.IndicadorGeneral.indicadores()
        inicio: str. Fecha donde iniciar la serie. También se puede especificar en INEGI.Indicador_General.definir_periodo()
                    o en INEGI.IndicadorGeneral.inicio
        fin: str. Fecha donde terminar la serie. También se puede especificar en INEGI.Indicador_General.definir_periodo()
                    o en INEGI.IndicadorGeneral.fin
        ----------

        """
        self._indicadores = self.indicadores
        self._columnas = self.nombres
        
        if indicadores: 
            self._indicadores = indicadores
            self.indicadores = indicadores
        if nombres: 
            self._columnas = nombres
            self.nombres = nombres
        elif len(self.nombres) == 0: self._columnas = self._indicadores 

        
        if isinstance(self._columnas, str): self._columnas = [self._columnas]
        return super().obtener_df(inicio, fin)





    