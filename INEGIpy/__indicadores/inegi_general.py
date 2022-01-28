#Prácticamente ya quedó pero hace falta revisar vris cosas como si conviene cambiar obtener_df para que 
#no se necesite especificar el banco.

#En las series este no es un problema ya que el diccionario con indicadores puede sin roblemas tener el banco 
#pero en IndicadorGeneral lo tiene que llenr el usuario y eso puede ser molesto. 

#Por lo pronto así se queda pero es algo por ver

from .indicador_general import IndicadorGeneral

class INEGI_General(IndicadorGeneral):
    
    def __init__(self, token):
        super().__init__(token)
        self.indicadores = list()
        self.bancos = list()
        self.nombres = list()

    def obtener_df(self, indicadores = None, bancos = None, nombres = None, inicio = None, fin = None):
        """
        Regresa un DataFrame con la información de los indicadores proporcionada por el API del INEGI.
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        Parametros
        -----------
        indicadores: list/str. Lista con los indicadores de las series a obtener. También se puede especificar 
                    en INEGI.IndicadorGeneral.indicadores
        bancos: list/str. Lista con los bancos donde se encuentran las series a obtener. También se puede especificar 
                    en INEGI.IndicadorGeneral.bancos
        nombres: list/str. Lista con los nombres de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
                    También se puede especificar en INEGI.IndicadorGeneral.indicadores()
        inicio: str. Fecha donde iniciar la serie. También se puede especificar en INEGI.Indicador_General.definir_periodo()
                    o en INEGI.IndicadorGeneral.inicio
        fin: str. Fecha donde terminar la serie. También se puede especificar en INEGI.Indicador_General.definir_periodo()
                    o en INEGI.IndicadorGeneral.fin
        ----------

        """
        self._indicadores = self.indicadores
        self._bancos = self.bancos
        self._columnas = self.nombres
        
        if indicadores: self._indicadores = indicadores
        if bancos: self._bancos = bancos
        if nombres: self._columnas = nombres
        elif len(self.nombres) == 0: self._columnas = self._indicadores
        
        if isinstance(self._columnas, str): self._columnas = [self._columnas]
        return super().obtener_df(inicio, fin)



