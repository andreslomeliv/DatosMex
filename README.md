# DatosMex
Librería general para el manejo de bases de datos abiertas en python.
Actualmente se están desarrollando clases para los datos del Banco de Información Económica (BIE) del INEGI y para el Sistema de Información Económica (SIE) de Banxico.

## INEGIpy
Librería de Python para interactuar con el API del INEGI.

#### Clases en desarrollo:
Una clase general para acceder a los indicadores proporcionados por el constructor de consultas del INEGI
* IndicadorGeneral
Además de un método general para obtener las series, se están desarrollando módulos particulares para los series de uso común, como:
* PIB
  * Total
  * PorSectores
* Inflación
* Desocupación

### Uso:
```python
from DatosMex import INEGI
inegi = INEGI(token)
pib = inegi.PIB.Total.obtener_df(series = ['real','trimestral desestacionalizada'], inicio = '2000', fin = '2019')
indicador = inegi.IndicadorGeneral.obtener_df(indicadores = ['214293'], bancos = ['BIE']) 
```
Los indicadores se pueden obtener del [constructor de consultas](https://www.inegi.org.mx/servicios/api_indicadores.html) proporcionado por el INEGI 


