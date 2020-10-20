from pib_general import PIB_General
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

token = '92170321-528f-f1dd-5d59-f8613e072746'

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

    def pib_df(self):  ######## checar bien cuánto puedo escribir en pib_general, probablemente puedo hacer 
        df = super().pib_df() #### todo ahí mismo
        df.columns = ['PIB']
        self._df = df
        return df
 
    def grafica(self, show = True, filename = None):
        if self._df is None:
            self.pib_df()
        fig, ax = plt.subplots()
        self._df.plot(ax=ax,color='black')
        sns.despine()
        ax.set_xlabel('')
        ax.legend().remove()
        ax.ticklabel_format(style='plain',axis='y')
        plt.tight_layout()
        
        if show: plt.show()
        #if filename: plt.savefig(filename) revisar pedos con la ruta
        return fig, ax
    
    def definir_serie(self, serie):
        super().definir_serie(serie)
        valores = serie[0]
        serie = serie[1]  
        self._indicadores = [self._indicadores_dict[valores][serie][0]]
        self._bancos = [self._indicadores_dict[valores][serie][1]]
        return self



