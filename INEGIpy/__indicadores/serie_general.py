from .inegi_general import INEGI_General

class Serie_General(INEGI_General):

    def __init__(self, token):
        super().__init__(token)
        self.serie = None
        self.consulta = dict()

    def _obtener_indicadores(self):
        pass

    def series_disponibles(self):
        """
        Regresa los niveles de series disponibles en cada clase. 
        """
        pass

    def obtener_df(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'serie': self.serie = value
            if key == 'inicio': self.inicio = value
            if key == 'fin': self.fin = value
        self._obtener_indicadores()
        return super().obtener_df()