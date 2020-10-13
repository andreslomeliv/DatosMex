# DatosMEx
Librería general para el manejo de bases de datos abiertas en python.
Actualmente se está desarrollando un módulo para los datos del Banco de Información Económica (BIE) del INEGI y para el Sistema de Información Económica (SIE) de Banxico.

## INEGIpy
Librería de Python para interactuar con el API del INEGI.

#### Módulos en desarrollo:
Además de un método general para obtener las series, se están desarrollando módulos particulares para los series de uso común, como:
* PIB
* Inflación
* Desocupación

### Uso:
```python
from DatosMex.INEGIpy import INEGI
inegi = INEGI(token)
df = inegi.PIB.Total(niveles = ['real','trimestral desestacionalizada'], inicio = '2000', fin = '2019')
```


