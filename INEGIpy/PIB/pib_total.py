from pib_general import PIB_General
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Total(PIB_General):
             
    def __init__(self, token):
        super().__init__(token)
        self._indicadores_dict = {'real':
                            {'anual':['6207061898','BISE'],
                             'trimestral desestacionalizada':['493911','BIE'],
                             'trimestral original':['493621','BIE'],
                             'trimestral acumulada':['493669','BIE']},
                        'nominal':
                            {'anual':['6207061840','BISE'],
                             'trimestral desestacionalizada':['494072','BIE'],
                             'trimestral original':['493717','BIE'],
                             'trimestral acumulada':['493765','BIE']}}
        self.definir_serie(['real', 'anual'])
        self._columnas = ['PIB']
    
    def definir_serie(self, serie):
        super().definir_serie(serie)
        valores = serie[0]
        serie = serie[1]  
        self._indicadores = [self._indicadores_dict[valores][serie][0]]
        self._bancos = [self._indicadores_dict[valores][serie][1]]
        return self



