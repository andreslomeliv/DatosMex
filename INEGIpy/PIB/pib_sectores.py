from pib_general import PIB_General
import pandas as pd

token = '92170321-528f-f1dd-5d59-f8613e072746' ###borrar

class PorSectores(PIB_General):

    def __init__(self, token):
        super().__init__(token)
        self._indicadores_dict = {'real':                             
                            {'trimestral desestacionalizada':
                                    {'primario':['493925','BIE'],
                                     'secundario':['493932','BIE'],
                                     'terciario':['493967','BIE']},
                            'trimestral original':
                                    {'primario':['493624','BIE'],
                                     'secundario':['493625','BIE'],
                                     'terciario':['493630','BIE']}}}
        self.__sectores = []
        self.definir_sectores(['primario','secundario','terciario'])
        self.definir_serie(['real','trimestral desestacionalizada'])

    def pib_df(self):
        df = super().pib_df()
        df.columns = ['PIB ' + s for s in self.__sectores]
        self._df = df
        return df

    def definir_serie(self, serie):
        super().definir_serie(serie)
        valores = serie[0]
        serie = serie[1]
        self._indicadores = [self._indicadores_dict[valores][serie][sector][0] 
                              for sector in self.__sectores]
        self._bancos = [self._indicadores_dict[valores][serie][sector][1] for sector
                         in self.__sectores]
        return self  

    def definir_sectores(self, sectores):
        self.__sectores = sectores
        return self

    def sectores_actuales(self):
        return self.__sectores

    def prueba_indicadores(self):
        return self._indicadores