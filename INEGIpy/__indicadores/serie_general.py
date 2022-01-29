# se tiene que agregar errores cuando se pida una serie que no exista

from .indicador_general import IndicadorGeneral

class Serie_General(IndicadorGeneral):

    def __init__(self, token):
        super().__init__(token)
        self.serie = None
        self._indicadores_dict = dict()

    def _obtener_indicadores(self):
        pass

    def obtener_df(self, serie, inicio, fin):
        if serie: self.serie = serie
        self._obtener_indicadores()
        return super().obtener_df(inicio, fin)

    def series_disponibles(self):
        """
        Regresa una lista con las series disponibles en cada módulo.

        """
        return list(self._indicadores_dict.keys())
