# se tiene que agregar las opciones disponibles y errores cuando se pida una serie que no exista

from .inegi_general import INEGI_General

class Serie_General(INEGI_General):

    def __init__(self, token):
        super().__init__(token)
        self.serie = None
        self.consulta = dict()

    def _obtener_indicadores(self):
        pass

    def obtener_df(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'serie': self.serie = value
        kwargs.pop('serie', None)
        self._obtener_indicadores()
        return super().obtener_df(**kwargs)

################ Mostrar series disponibles ##################################

# Aún tengo que encontrar la mejor forma de presentar las series disponibles considerando 
# todos los parámetros
# Opciones:
#       1. Mostrar cada parámetro individualmente:
#                   serie.series_disponibles()/sectores_disponibles()/valores_disponibles() etc
#                   ventaja: permite a usuario usar las serpuestas en los parámetros
#                   también podrían llevar parámetros para ver lo que está disponible dado otro parámetro:
#                   por ejemplo, con el pib no hay valores nominales para las series entonces si utilizas
#                   pib.valores_disponibles(sector = primario) solo aparecen los reales 
#                   desventajas: más complicado de codear al punto que puede no valer la pena el costo
#       2. Mostrar todos los distintos parámeteros y sus opciones en una sola función
#                   serie.opciones_disponibles()
#                   ventajas: más fácil de codear y entendible
#                   desventajas: no se puede apreciar las combinaciones que no existen en los casos de los 
#                   diccionarios de indicadores que no son simétricos (como el del pib)
#                   se podría agregar una nota indicando cuales combinaciones no existen