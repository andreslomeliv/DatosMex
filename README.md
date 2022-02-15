# DatosMex
Librería general para el manejo de bases de datos abiertas en python.
Actualmente se están desarrollando clases para los datos del Banco de Información Económica (BIE) del INEGI y para el Sistema de Información Económica (SIE) de Banxico.

## INEGIpy
Librería de Python para interactuar con el API del INEGI.

### Clases:
Una clase general para acceder a los indicadores proporcionados por el [constructor de consultas](https://www.inegi.org.mx/servicios/api_indicadores.html) del INEGI
* INEGI_General

Además de un método general para obtener las series, se están desarrollando módulos particulares para los series de uso común, como:

* PIB
* Inflación (En desarrollo)
* Desocupación (En desarrollo)

Cada módulo cuenta con dos funciones: ```obtener_df()``` y ```grafica()``` los cuales regresan la información proporcionada por el API del INEGI en ambos formatos.
Los indicadores, series, años y otros parámetros se pueden proporcionar como argumentos de las funciones o como atributos públicos de los objetos. 

### Uso:
```python
from INEGIpy import PIB, INEGI_General

# Se requiere un token proporcionado por el INEGI
token = 'foobar'
pib = PIB(token) 
indicador = INEGI_General(token) 

# Indicando los parámetros dentro de las funciones:
pib.obtener_df(serie = 'trimestral desestacionalizada', sectores = ['total','terciario'], reales = True, inicio = '2000', fin = '2021')
indicador.obtener_df(indicadores = '628229', bancos = 'BIE', nombres = 'Inflación General', inicio = '2018-06', fin = '2021-12')

# Indicando los parámetros fuera de las funciones:
pib.serie = 'trimestral desestacionalizada'
pib.sectores = ['secundario','primario']
pib.reales = True
pib.inicio = '2000'
pib.final = '2022'
pib.obtener_df()
pib.grafica()

indicador.indicadores = '628229'
indicador.bancos = 'BIE'
indicador.nombres = 'Inflación General'
indicador.inicio = '2018-06'
indicador.fin = '2021-12'
indicador.obtener_df()
indicador.grafica()
```
Las consultas ya generadas se mantienen guardadas en el mismo objeto para uso subsecuente a menos que se cambie algún parámetro. Esto funciona en ambas formas: ya sea estableciendo los parámetros dentro o fuera de las funciones.

Los indicadores se pueden obtener del [constructor de consultas](https://www.inegi.org.mx/servicios/api_indicadores.html) proporcionado por el INEGI.

## BANXICOpy
Librería de Python para interactuar con el API del Sistema de Información Económica del Banco de México.

### Clases:
Una clase general para acceder a los indicadores proporcionados por el [catálogo de series](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#) de Banxico.
* Banxico_General

Además de un método general para obtener las series, se están desarrollando módulos particulares para los series de uso común, como:

* Tipo de Cambio (En desarrollo)
* Tasas de interés (En desarrollo)
* Balaza de pagos (En desarrollo)

Cada módulo cuenta con dos funciones: ```obtener_df()``` y ```grafica()``` los cuales regresan la información proporcionada por el API de Banxico en ambos formatos.
Los indicadores, series, años y otros parámetros se pueden proporcionar como argumentos de las funciones o como atributos públicos de los objetos. 

### Uso:
```python
from BANXICOpy import Banxico_General

# Se requiere un token proporcionado por el INEGI
token = 'foobar'
indicador = Banxico_General(token)

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
