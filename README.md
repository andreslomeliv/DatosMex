 # DatosMex
Proyecto en Python orientado a la creación de librerías para el manejo de bases de datos abiertas en México.
Actualmente se están desarrollando dos librerías: INEGIpy y BANXICOpy. La primera está dedicada a las APIs del INEGI: el Banco de Indicadores, el DENUE, el Servicio de Ruteo y el Catálogo de Claves Únicas Geoestadísticas o Marco Geoestadístico. La segunda está dedicada a la API del Sistema de Inforamción Económica del Banco de México. 

## INEGIpy
Librería de Python para interactuar con las APIs del INEGI.

### Clases:

* **Indicadorres:** clase general para acceder a los indicadores económicos proporcionados por el [constructor de consultas](https://www.inegi.org.mx/servicios/api_indicadores.html) del INEGI.
* **DENUE:** clase para acceder a los datos del [Directorio Estadístico Nacional de Unidades Económicas (DENUE)](https://www.inegi.org.mx/app/mapa/denue/default.aspx).
* **Ruteo:** clase para utilizar el [Servicio de Ruteo de México](http://gaia.inegi.org.mx/mdm6/?v=bGF0OjIzLjMyMDA4LGxvbjotMTAxLjUwMDAwLHo6MSxsOmMxMTFzZXJ2aWNpb3N8dGMxMTFzZXJ2aWNpb3M=).
* **MarcoGeoestadistico:** clase para obtener la información de las [áreas geoestadísticas](https://www.inegi.org.mx/temas/mg/) que define el INEGI en el Censo de Población y Vivienda 2020.

Además de una clase general para obtener los indicadores económicos, se están desarrollando clases particulares para los series de uso común, como:

* PIB
* Inflación 
* Desocupación 

### Uso:
```python
from INEGIpy import Indicadores

# Se requiere un token proporcionado por el INEGI
token = 'foobar'
indicador = Indicadores(token) 

# Indicando los parámetros dentro de las funciones:
indicador.obtener_df(indicadores = '628229', bancos = 'BIE', nombres = 'Inflación General', inicio = '2018-06', fin = '2021-12')

# Indicando los parámetros fuera de las funciones:
indicador.indicadores = '628229'
indicador.bancos = 'BIE'
indicador.nombres = 'Inflación General'
indicador.inicio = '2018-06'
indicador.fin = '2021-12'
indicador.obtener_df()
```
Las consultas ya generadas se mantienen guardadas en el mismo objeto para uso subsecuente a menos que se cambie algún parámetro. Esto funciona en ambas formas: ya sea estableciendo los parámetros dentro o fuera de las funciones.

Los indicadores se pueden obtener del [constructor de consultas](https://www.inegi.org.mx/servicios/api_indicadores.html) proporcionado por el INEGI.

## BANXICOpy
Librería de Python para interactuar con la API del Sistema de Información Económica del Banco de México.

### Clases:
Una clase general para acceder a los indicadores proporcionados por el [catálogo de series](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#) de Banxico.
* Banxico

Además de una clase general para obtener las series, se están desarrollando clases particulares para los series de uso común, como:

* Tipo de Cambio 
* Tasas de interés 
* Balaza de pagos 

### Uso:
```python
from BANXICOpy import Banxico

# Se requiere un token proporcionado por el INEGI
token = 'foobar'
indicador = Banxico(token)

# Indicando los parámetros dentro de las funciones:
indicador.obtener_df(indicadores = ['SF46405','SF46410'], nombres = ['USD','EURO'], inicio = '2020-01-01', fin = '2021-09-14')

# Indicando los parámetros fuera de las funciones:
indicador.indicadores = 'SF44043'
indicador.nombres = 'Base Monetaria Observada'
indicador.inicio = '2010-01-01'
indicador.fin = '2022-01-01'
indicador.obtener_df()
indicador.grafica()
```
Las consultas ya generadas se mantienen guardadas en el mismo objeto para uso subsecuente a menos que se cambie algún parámetro. Esto funciona en ambas formas: ya sea estableciendo los parámetros dentro o fuera de las funciones.

Los indicadores se pueden obtener del [catálogo de series](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#) proporcionado por el Bancon de México.
