#Según yo solo falta elegir la forma de presentar las series disponibles.

from .serie_general import Serie_General

class PIB(Serie_General):
    
    def __init__(self, token):
        super().__init__(token)
        self.serie = 'trimestral desestacionalizada'
        self.reales = True
        self.sectores = 'total'
        self._columnas = ['PIB total']
        self._indicadores_dict = {'trimestral desestacionalizada':
                                        {'total': 
                                            {'real':('493911','BIE'), 
                                             'nominal':('494072','BIE')},
                                        'primario':
                                            {'real':('493925','BIE')},
                                        'secundario': 
                                            {'real':('493932','BIE')},
                                        'terciario': 
                                            {'real':('493967','BIE')}},
                                  'trimestral original':
                                        {'total': 
                                            {'real':('493621','BIE'), 
                                             'nominal':('493717','BIE')},
                                        'primario':
                                            {'real':('493624','BIE')},
                                        'secundario': 
                                            {'real':('493625','BIE')},
                                        'terciario': 
                                            {'real':('493630','BIE')}},
                                  'anual':
                                        {'total': 
                                            {'real':('6207061898','BISE'),
                                             'nominal':('6207061840','BISE')}},
                                  'trimestral acumulada':
                                        {'total': 
                                            {'real':('493669','BIE'),
                                             'nominal':('493765','BIE')}}}
        #self.consulta = None
        
    def _obtener_indicadores(self):
        super()._obtener_indicadores()
        dict_indicadores = self._indicadores_dict[self.serie]
        if isinstance(self.sectores, str): self.sectores = [self.sectores]
        if self.reales: valores = 'real'
        else: valores = 'nominal'
        indicadores = list()
        bancos = list()
        columnas = list()
        for sector in self.sectores:
            indicadores.append(dict_indicadores[sector][valores][0]) 
            bancos.append(dict_indicadores[sector][valores][1])
            columnas.append('PIB {}'.format(sector))
        self._indicadores = indicadores
        self._bancos = bancos
        self._columnas = columnas
        if self.serie == 'anual': self._periodos = None

    def obtener_df(self, serie = None, sectores = None, reales = True, inicio = None, fin = None):
        """
        Regresa un DataFrame con la información de los indicadores proporcionada por el API del INEGI.
        Para más información visitar https://www.inegi.org.mx/servicios/api_indicadores.html

        Parametros
        -----------
        serie: str. String con el nombre de la serie a obtener. También se puede especificar en INEGI.PIB.serie
        sectores: list/str. Lista sectores a obtener. También se puede especificar en PIB.serie
        reales: bool. True si la serie es en valores reales (precios fijos). False si son valores nominales (precios corrientes)
                      También se puede especificar en PIB.reales
        inicio: str. Fecha donde iniciar la serie. También se puede especificar en PIB.inicio
        fin: str. Fecha donde terminar la serie. También se puede especificar en PIB.fin
        -----------

        """
        if sectores: self.sectores = sectores
        if reales: self.reales = reales
        self._obtener_indicadores() # checa si este se puede quitar
        return super().obtener_df(sectores, inicio, fin)

    def sectores_disponibles(self, serie = None):
        """
        Regresa una lista con los sectores disponibles. Algunas series no tienen todos los sectores por lo que se puede especificar
        la serie para ver qué sectores están disponibles para esa serie en particular.
        
        También es importante anotar que el solamente el PIB Total cuenta con valores nominales, los sectores no.

        Parametros
        -----------
        serie: str. String con el nombre de la serie.
        -----------

        """
        if serie: return list(self._indicadores_dict[serie].keys())
        else: return list(self._indicadores_dict['trimestral desestacionalizada'].keys())