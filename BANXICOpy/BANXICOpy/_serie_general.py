from ._indicador_general import IndicadorGeneral

class SerieGeneral(IndicadorGeneral):
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