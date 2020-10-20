import matplotlib.pyplot as plt
import pprint
import seaborn as sns
import sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent

sys.path.append(str(HERE / '../../INEGIpy'))

from inegi_general import INEGI_General

class PIB_General(INEGI_General):
    
    def __init__(self, token):
        super().__init__(token)
        self._indicadores_dict = {}
        self._indicadores = None
        self._bancos = None
        self._inicio = None
        self._fin = None
        self._serie = []
        self._df = None
        
    def series_disponibles(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self._indicadores_dict)
              

    #def grafica_minimalistas(self):
    #    df = self.pib_df()
    #    fig,ax = plt.subplots()
    #    sns.set_palette('gray')
     #   sns.lineplot(data=df)
      #  sns.despine()
       # ax.set_xlabel('')
        #ax.ticklabel_format(style='plain',axis='y')
        
    def pib_df(self):
        df = self._indicadores_a_df(self._indicadores, self._bancos,
                                    self._inicio, self._fin)
        if self._bancos == ['BIE']: df = df[::-1]
        return df

    def años(self):
        return (self._inicio, self._fin)
    
    def definir_años(self, inicio, fin):
        self._inicio = inicio
        self._fin = fin
        if self._df: self._df[inicio:fin]
        return self

    def serie_actual(self):
        return self._serie

    def definir_serie(self, serie):
        """
        serie -- list. [valor, tipo de serie], ejemplo: ['real','trimestral desestacionalizada']. Para ver las 
        series disponibles ver self.series_disponibles()
        """
        self._serie = serie
        return 