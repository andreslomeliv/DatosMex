
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.append(str(HERE / '../INEGIpy/PIB'))

from pib_total import Total
from pib_sectores import PorSectores


class PIB:
    def __init__(self, token):
        self.token = token
        self.Total = Total(self.token)
        self.PorSectores = PorSectores(self.token)