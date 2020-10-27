from pib_general import PIB_General
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        self.sectores = []
        self.definir_sectores(['primario','secundario','terciario'])
        self.definir_serie(['real','trimestral desestacionalizada'])
        self._columnas = ['PIB ' + sector for sector in self.sectores]

    def definir_serie(self, serie):
        super().definir_serie(serie)
        valores = serie[0]
        serie = serie[1]
        self._indicadores = [self._indicadores_dict[valores][serie][sector][0] 
                              for sector in self.sectores]
        self._bancos = [self._indicadores_dict[valores][serie][sector][1] for sector
                         in self.sectores]
        return self  

    def definir_sectores(self, sectores):
        self.sectores = sectores
        return self

    def sectores_actuales(self):
        return self.sectores


################################################################################################

