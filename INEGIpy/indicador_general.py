##################################################################
######### PEDOSPEDOSPEDOSPEDOS
###################################################################3333333
# No debe volver a hacer requests al api si no se cambiaron los indicadores
## ni cada vez que se llame la función grafica()

from inegi_general import INEGI_General

class IndicadorGeneral(INEGI_General):
    
    def __init__(self, token):
        super().__init__(token)

    def definir_indicadores(self, indicadores):
        if self._indicadores != indicadores: self._cambios = True
        self._indicadores = indicadores

    def definir_nombres(self, nombres):
        if self._columnas != nombres: self._cambios = True
        self._columnas = nombres

    def definir_bancos(self, bancos):
        self._bancos = bancos

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
            if key == 'indicadores': self.definir_indicadores(value)
            if key == 'bancos': self.definir_bancos(value)
            if key == 'nombres': self.definir_nombres(value)
            if key == 'inicio': self.inicio = value
            if key == 'fin': self.fin = value
        return super().obtener_df()

    