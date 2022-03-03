# se tiene que agregar errores cuando se pida una serie que no exista

from ._indicador_general import IndicadorGeneral

class Serie_General(IndicadorGeneral):

    def __init__(self, token):
        super().__init__(token)
        self.serie = None
        self._indicadores_dict = dict()

    def _obtener_indicadores(self):
        pass

    # cada objeto que hereda a IndicadorGeneral va agregando nuevas variables a obtener_df() que permiten modificar
    # la consulta dentro de la función. En este caso todos los módulos que hereden este objeto pueden definir la serie
    # de la consulta por lo que se define aquí. Cada módulo agrega las variables faltantes particulares par la consulta
    # Ejemplo: el módulo PIB agrega si los valores son reales o nominales y los sectores del PIB.
    
    def obtener_df(self, serie, inicio, fin):
        if serie: self.serie = serie
        self._obtener_indicadores()
        return super().obtener_df(inicio, fin)

    # esta función tal vez deje de funcionar de esta forma en otras series pero por lo pronto así se define
    def series_disponibles(self):
        """
        Regresa una lista con las series disponibles en cada módulo.

        """
        return list(self._indicadores_dict.keys())
