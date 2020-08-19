# -*- coding: utf-8 -*-
###############################################################################
################################### INEGI.py  #################################
###############################################################################
from .PIB import PIB
import json

class APItoken:
    
    def __init__(self,token):
        self.token = token
        self.PIB = PIB(self.token)
        
    
    with open('localidades_INEGI.txt','r') as file:
        localidades_dict = json.loads(file.read())
        
        