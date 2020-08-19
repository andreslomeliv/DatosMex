# -*- coding: utf-8 -*-
###############################################################################
################################### INEGI.py  #################################
###############################################################################
from .PIB import PIB
import json
from pathlib import Path

class APItoken:
    
    def __init__(self,token):
        self.token = token
        self.PIB = PIB(self.token)
    
    localidades_dict = json.loads(Path('localidades_INEGI.txt').read_text())
