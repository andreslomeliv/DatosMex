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
