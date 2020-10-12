# -*- coding: utf-8 -*-
## código de la clase PIB
import matplotlib.pyplot as plt
import pprint
import seaborn as sns
import pandas as pd
from . import metodos_generales as mg

class Total:
              
    indicadores_dict = {'real':
                            {'anual':['6207061898','BISE'],
                             'trimestral desestacionalizada':['493911','BIE'],
                             'trimestral original':['493621','BIE'],
                             'trimestral acumulada':['493669','BIE']},
                        'nominal':
                            {'anual':['6207061840','BISE'],
                             'trimestral desestacionalizada':['494072','BIE'],
                             'trimestral original':['493717','BIE'],
                             'trimestral acumulada':['493765','BIE']}}
            
    def __init__(self,token):
        self.token = token
              
    def niveles(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.indicadores_dict)

    def pib_df(self,niveles=['real','anual'],localidad='0700',
               inicio=None,fin=None):
        valores = niveles[0]
        serie = niveles[1]  
        indicador = self.indicadores_dict[valores][serie][0]
        banco = self.indicadores_dict[valores][serie][1]
        df = mg.indicador_a_df(self.token,indicador,banco,localidad)
        df.columns = ['PIB']
        if banco == 'BIE': df = df[::-1]
        return df[inicio:fin]
 
    def grafica_minimalista(self,niveles=['real','anual'],localidad='00',
                            inicio=None,fin=None):
        df = self.pib_df(niveles,localidad,inicio,fin)
        fig,ax = plt.subplots()
        df.plot(ax=ax,color='black')
        sns.despine()
        ax.set_xlabel('')
        ax.legend().remove()
        ax.ticklabel_format(style='plain',axis='y')
        plt.tight_layout()

class PorSector:
        
    def __init__(self,token):
        self.token = token 
        
    indicadores_dict = {'real':                             
                            {'trimestral desestacionalizada':
                                    {'primario':['493925','BIE'],
                                     'secundario':['493932','BIE'],
                                     'terciario':['493967','BIE']},
                            'trimestral original':
                                    {'primario':['493624','BIE'],
                                     'secundario':['493625','BIE'],
                                     'terciario':['493630','BIE']}}}

    def niveles(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.indicadores_dict)
        
   
    def pib_df(self,niveles=['real','trimestral desestacionalizada'],
               sectores=['primario','secundario','terciario'],
               localidad=['0700'],inicio=None,fin=None):
        valores = niveles[0]
        serie = niveles[1]
        indicadores = [self.indicadores_dict[valores][serie][sector][0] 
                       for sector in sectores]
        bancos = [self.indicadores_dict[valores][serie][sector][1] for sector
                  in sectores]
        df = mg.indicadores_a_df(self.token,indicadores,bancos,localidad)
        df.columns = ['PIB ' + s for s in sectores]
        df = df[::-1]
        return df[inicio:fin]


    def grafica_minimalistas(self,
                              niveles=['real','trimestral desestacionalizada'],
                              sectores=['primario','secundario','terciario'],
                              localidad='00',inicio=None,fin=None):
        df = self.pib_df(niveles,sectores,localidad,inicio,fin)
        fig,ax = plt.subplots()
        sns.set_palette('gray')
        sns.lineplot(data=df)
        sns.despine()
        ax.set_xlabel('')
        ax.ticklabel_format(style='plain',axis='y')

class PIB:
    
    def __init__(self,token):
        self.token = token
        self.Total = Total(self.token)
        self.PorSector = PorSector(self.token)

    