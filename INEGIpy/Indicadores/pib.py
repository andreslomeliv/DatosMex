import matplotlib.pyplot as plt
import seaborn as sns
#import sys
#from pathlib import Path

#HERE = Path(__file__).parent

#sys.path.append(str(HERE / '../../INEGIpy'))

from .serie_general import Serie_General

class PIB(Serie_General):
    
    def __init__(self, token):
        super().__init__(token)
        self.serie = 'trimestral desestacionalizada'
        self.valores = 'real'
        self.periodo = (None, None)
        self.sectores = 'total'
        self._columnas = ['PIB total']
        self._indicadores_dict = {'trimestral desestacionalizada':
                                        {'total': 
                                            {'real':('493911','BIE'), 
                                             'nominal':('494072','BIE')},
                                        'primario':
                                            {'real':('493925','BIE')},
                                        'secundario': 
                                            {'real':('493932','BIE')},
                                        'terciario': 
                                            {'real':('493967','BIE')}},
                                  'trimestral original':
                                        {'total': 
                                            {'real':('493621','BIE'), 
                                             'nominal':('493717','BIE')},
                                        'primario':
                                            {'real':('493624','BIE')},
                                        'secundario': 
                                            {'real':('493625','BIE')},
                                        'terciario': 
                                            {'real':('493630','BIE')}},
                                  'anual':
                                        {'total': 
                                            {'real':('6207061898','BISE'),
                                             'nominal':('6207061840','BISE')}},
                                  'trimestral acumulada':
                                        {'total': 
                                            {'real':('493669','BIE'),
                                             'nominal':('493765','BIE')}}}
        self.consulta = None
        
    def _obtener_indicadores(self):
        super()._obtener_indicadores()
        dict_indicadores = self._indicadores_dict[self.serie]
        if isinstance(self.sectores, str): self.sectores = [self.sectores]
        indicadores = list()
        bancos = list()
        columnas = list()
        for sector in self.sectores:
            indicadores.append(dict_indicadores[sector][self.valores][0]) 
            bancos.append(dict_indicadores[sector][self.valores][1])
            columnas.append('PIB {}'.format(sector))
        self._indicadores = indicadores
        self._bancos = bancos
        self._columnas = columnas

    def obtener_df(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'sectores': self.sectores = value
            if key == 'valores': self.valores = value
        self._obtener_indicadores()
        return super().obtener_df()

################################################################################
# arreglar marcadores
################################################################################
    def _cambiar_lineas(self, ax, estilo):
        if estilo == 'colores':
            self.__cambiar_colores(ax)
        if estilo == 'blanco y negro':
            self.__cambiar_estilos(ax)
        ax.legend(self._columnas)

    def __cambiar_estilos(self, ax):
        ls = ['--','-.','-']
        for i, line in enumerate(ax.get_lines()):
            line.set_linestyle(ls[i])

    def __cambiar_colores(self, ax):
        palette = sns.color_palette('colorblind',3)[::-1]
        for i, line in enumerate(ax.get_lines()):
            line.set_color(palette[i])
