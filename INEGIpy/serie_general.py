## Problemas
# self.__pretty_printer() no ha funcionado como debe por alguna razón, vale la pena checar bien cuál es la
# mejor manera de presentar en lan terminal las series disponibles en cada clase

from inegi_general import INEGI_General

class Serie_General(INEGI_General):

    def __init__(self, token):
        super().__init__(token)
        self.serie = []

    def __pretty_printer(self, dictionary, niveles = None):
        indent = 0
        for key, value in dictionary.items():
            print('\t'*indent + key)
            if type(value) is dict:
                self.__pretty_printer(value, indent+2)

    def series_disponibles(self):
        """
        Regresa los niveles de series disponibles en cada clase. 
        """
        self.__pretty_printer(self._indicadores_dict)

    def obtener_df(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'serie': self.definir_serie(value)
            if key == 'inicio': self.inicio = value
            if key == 'fin': self.fin = value
        return super().obtener_df()

#################################################################################
# Considerando si borrar estos métodos y solo hacerlos accesibles a través de los
# atributos públicos como self.serie, self.inicio, etc. Por el momento son ambas 
# maneras y que a cada quién use la qeu se acomode mejor.
#################################################################################

    def serie_actual(self):
        return self.serie

    def definir_serie(self, serie):
        """
        serie -- lista con los niveles de información de la serie a obtener. 
        Para mayor información ver self.series_disponilbes
        """
        self._cambios = True
        self.serie = serie
        return 
              
##################################################################################