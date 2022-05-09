#Prácticamente ya quedó pero hace falta revisar vris cosas como si conviene cambiar obtener_df para que 
#no se necesite especificar el banco.

#En las series este no es un problema ya que el diccionario con indicadores puede sin roblemas tener el banco 
#pero en IndicadorGeneral lo tiene que llenr el usuario y eso puede ser molesto. 

#Por lo pronto así se queda pero es algo por ver

from ._indicador_general import IndicadorGeneral

class Indicadores(IndicadorGeneral):
    
    def __init__(self, token):
        super().__init__(token)
        
    # Las variables de la consulta pueden ser definidos o redefinidos con los parámteros de la función
    def obtener_df(self, 
                   indicadores: 'str|list', 
                   nombres: 'str|list' = None, 
                   inicio: str = None, 
                   fin: str = None):
        """
        Regresa un DataFrame con la información de los indicadores proporcionada por el API del INEGI.

        Parametros
        -----------
        indicadores: str/list. Lista con los indicadores de las series a obtener.
        nombres: list/str, opcional. Lista con los nombres de las columas del DataFrame. De no proporcionarse, se usarán los indicadores.
        inicio: str, opcional. Fecha donde iniciar la serie. De no proporcionarse será desde el primer valor disponible. 
        fin: str, opcional. Fecha donde terminar la serie. De no proporcionarse será hasta el último valor disponible. 
        ----------
        
        El DataFrame resultante tiene una columna por cada indicador y un DateTimeIndex con la fecha de los valores. 
        
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        """     
        self._indicadores = indicadores
        if nombres: 
            self._columnas = nombres
        return super().obtener_df(inicio, fin)



