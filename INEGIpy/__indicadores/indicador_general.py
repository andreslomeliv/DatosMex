#Prácticamente ya quedó pero hace falta revisar vris cosas como si conviene cambiar obtener_df para que 
#no se necesite especificar el banco.

#En las series este no es un problema ya que el diccionario con indicadores puede sin roblemas tener el banco 
#pero en IndicadorGeneral lo tiene que llenr el usuario y eso puede ser molesto. 

#Por lo pronto así se queda pero es algo por ver

# también debo checar si es mejor cambiar **kwargs por los parámetros inicializados en None

from .inegi_general import INEGI_General

class IndicadorGeneral(INEGI_General):
    
    def __init__(self, token):
        super().__init__(token)
        self.indicadores = list()
        self.bancos = list()
        self.nombres = list()

    def obtener_df(self, **kwargs):
        """
        Parametros
        -----------
        indicadores: list. Lista con los indicadores de las series a obtener. También se puede especificar 
                    en INEGI.IndicadorGeneral.indicadores()
        bancos: list. Lista con los bancos donde se encuentran las series a obtener. También se puede especificar 
                    en INEGI.IndicadorGeneral.bancos(). 
        nombres: list. Lista con los nombres de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
                    También se puede especificar en INEGI.IndicadorGeneral.indicadores()
        inicio: str. Fecha donde iniciar la serie. También se puede especificar en INEGI.Indicador_General.definir_periodo()
                    o en INEGI.IndicadorGeneral.inicio
        fin: str. Fecha donde terminar la serie. También se puede especificar en INEGI.Indicador_General.definir_periodo()
                    o en INEGI.IndicadorGeneral.fin
        """
        self._indicadores = self.indicadores
        self._bancos = self.bancos
        self._columnas = self.nombres
        for key, value in kwargs.items():
            if key == 'indicadores': 
                self._indicadores = value
                self.indicadores = value
            if key == 'bancos': 
                self._bancos = value
                self.bancos = value
            if key == 'nombres': 
                self._columnas = value
                self.nombres = value
        
        if isinstance(self._columnas, str): self._columnas = [self._columnas]

        kwargs.pop('indicadores', None)
        kwargs.pop('bancos', None)
        kwargs.pop('nombres', None)

        return super().obtener_df(**kwargs)

    