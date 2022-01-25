# Notas: a veces se vuelve a llamar al API aunque no cambiaron los indicadores, generalmente lo hace la primera
# vez después de haber llamado al df
# se tiene que agregar las opciones disponibles y errores cuando se pida una serie que no exista

from .serie_general import Serie_General

class PIB(Serie_General):
    
    def __init__(self, token):
        super().__init__(token)
        self.serie = 'trimestral desestacionalizada'
        self.valores = 'real'
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
        indicadores = list()
        bancos = list()
        columnas = list()
        for sector in self.sectores:
            indicadores.append(dict_indicadores[sector][self.valores][0]) 
            bancos.append(dict_indicadores[sector][self.valores][1])
            columnas.append('PIB {}'.format(sector))
        self._indicadores = indicadores
        self._bancos = bancos
        self._columnas = columnas

    def obtener_df(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'sectores': self.sectores = value   
            if key == 'valores': self.valores = value
                
        kwargs.pop('sectores', None)
        kwargs.pop('valores', None)

        self._obtener_indicadores() # checa si este se puede quitar
        return super().obtener_df(**kwargs)
