from banxico_general import BanxicoGeneral

class TipoDeCambio(BanxicoGeneral):
    def __init__(self, token):
        super().__init__(token)
        self.__indicadores = ['SF46405','SF46410','SF46406','SF46407','SF290383','SF46411']
