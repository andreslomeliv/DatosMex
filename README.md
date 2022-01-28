# DatosMex
Librería general para el manejo de bases de datos abiertas en python.
Actualmente se están desarrollando clases para los datos del Banco de Información Económica (BIE) del INEGI y para el Sistema de Información Económica (SIE) de Banxico.

## INEGIpy
Librería de Python para interactuar con el API del INEGI.

### Clases en desarrollo:
Una clase general para acceder a los indicadores proporcionados por el [constructor de consultas](https://www.inegi.org.mx/servicios/api_indicadores.html) del INEGI
* INEGI_General

Además de un método general para obtener las series, se están desarrollando módulos particulares para los series de uso común, como:

* PIB
* Inflación
* Desocupación

Cada módulo cuenta con dos funciones: ```obtener_df()``` y ```grafica()``` los cuales regresan la información proporcionada por el API del INEGI en ambos formatos.
Los indicadores, series, años y otros parámetros se puden proporcionar como argumentos de las funciones o como atributos públicos de los objetos. 

### Uso:
```python
from INEGIpy import PIB, INEGI_General

# Se requiere un token proporcionado por el INEGI
token = 'foobar'
pib = PIB(token) # Inicializa el objeto PIB
indicador = INEGI_General(token) # inicializa el objeto INEGI_General

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
Los indicadores se pueden obtener del [constructor de consultas](https://www.inegi.org.mx/servicios/api_indicadores.html) proporcionado por el INEGI.
Las consultas ya generadas se mantienen guardadas en el mismo objeto para uso subsecuente a menos que se cambie algún parámetro. Esto funciona en ambas formas: ya sea estableciendo los parámetros dentro o fuera de las funciones.


