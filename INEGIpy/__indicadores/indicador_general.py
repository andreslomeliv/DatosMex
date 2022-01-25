# este modulo está fallando. Necesito revisarlo bien. 

from .inegi_general import INEGI_General

class IndicadorGeneral(INEGI_General):
    
    def __init__(self, token):
        super().__init__(token)
        self.indicadores = None
        self.bancos = None
        self.nombres = None

    def obtener_df(self, **kwargs):
        """
        Parametros
        -----------
        indicadores: list. Lista con los indicadores de las series a obtener. También se puede especificar 
                    en INEGI.IndicadorGeneral.indicadores()
        bancos: list. Lista con los bancos donde se encuentran las series a obtener. También se puede especificar 
                    en INEGI.IndicadorGeneral.bancos(). 
        nombres: list. Lista con los nombres de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
                    También se puede especificar en INEGI.IndicadorGeneral.indicadores()
        inicio: str. Fecha donde iniciar la serie. También se puede especificar en INEGI.Indicador_General.definir_periodo()
                    o en INEGI.IndicadorGeneral.inicio
        fin: str. Fecha donde terminar la serie. También se puede especificar en INEGI.Indicador_General.definir_periodo()
                    o en INEGI.IndicadorGeneral.fin
        """
        for key, value in kwargs.items():
            if key == 'indicadores': self._indicadores = value
            else: self._indicadores = self.indicadores

            if key == 'bancos': self._bancos = value
            else: self._bancos = self.bancos
            
            if key == 'nombres': self._columnas = value
            else: self._columnas = self.nombres

        kwargs.pop('indicadores', None)
        kwargs.pop('bancos', None)
        kwargs.pop('nombres', None)

        return super().obtener_df(**kwargs)

    