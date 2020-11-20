# -*- coding: utf-8 -*-
###############################################################################
################################### INEGI.py  #################################
###############################################################################
import json

from PIB import PIB 
from indicador_general import IndicadorGeneral

class INEGI:
    
    def __init__(self,token):
        self.token = token
        self.PIB = PIB(self.token)
        self.IndicadorGeneral = IndicadorGeneral(self.token)
    
    #localidades_dict = json.loads(Path('localidades_INEGI.txt').read_text())
