import sys
from pathlib import Path

HERE = Path(__file__).parent

sys.path.append(str(HERE / '../../INEGIpy'))

from inegi_general import INEGI_General

class PIB_General(INEGI_General):
    
    def __init__(self, token):
        super().__init__(token)

    #def grafica_minimalistas(self):
    #    df = self.pib_df()
    #    fig,ax = plt.subplots()
    #    sns.set_palette('gray')
     #   sns.lineplot(data=df)
      #  sns.despine()
       # ax.set_xlabel('')
        #ax.ticklabel_format(style='plain',axis='y')
