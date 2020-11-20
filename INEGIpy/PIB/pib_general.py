import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

HERE = Path(__file__).parent

sys.path.append(str(HERE / '../../INEGIpy'))

from serie_general import Serie_General

class PIB_General(Serie_General):
    
    def __init__(self, token):
        super().__init__(token)

