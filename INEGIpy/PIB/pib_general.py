import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

HERE = Path(__file__).parent

sys.path.append(str(HERE / '../../INEGIpy'))

from inegi_general import INEGI_General

class PIB_General(INEGI_General):
    
    def __init__(self, token):
        super().__init__(token)

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
