# BanxicoPy

BanxicoPy es una librería para interactuar fácilmente con los datos del [Sistema de Información Económica](https://www.banxico.org.mx/SieInternet/) del Banco de México desde Python. Su propósito es apoyar en la creación de consultas automatizadas y en el acceso a la información para el análisis de datos.

Actualmente consiste de solo tres métodos que engloban las funciones disponibles en la API: consulta de series de tiempo, consulta de metadatos y consulta del último dato disponible para todos los indicadores en el repositorio. Cada uno regresa un DataFrame con el resultado de la consulta listo para su uso en Python. También se encuentra en construcción un módulo de Series dedicado a consultas automatizadas de los principales indicadores como las tasas de interés, tipos de cambio, subastas y finanzas públicas.

Para más información y consulta de los indicadores disponibles visita: https://www.banxico.org.mx/SieAPIRest/service/v1/

## Requerimientos

* requests
* pandas

## Instalación 


```pip install BanxicoPy```

## Documentación

```python
class Banxico(token)
```

**Parámetros** 
   * **token:** str. Token proporcionado por el Banco de México.
   
La clase ```Banxico``` contiene los métodos y atributos relacionados a la API del Sistema de Información Económica del Banco de México. Esta API permite consultar los datos y metadatos de los indicadores económicos y financieros disponibles en el repositorio. Las claves de los indicadores y más información sobre la API se pueden obtener en el [catálogo de series](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries). Esta clase requiere un [token generado por el Banco de México](https://www.banxico.org.mx/SieAPIRest/service/v1/token).


### Métodos

#### obtener_serie()

```python
Banxico.obtener_serie(indicadores, 
                      nombres = None, 
                      inicio = None, 
                      fin = None,
                      decimales = True,
                      incremento = None)
```
**Parámetros**
* **indicadores:** str/list. Clave(s) de los indicadores a consultar. Puede ser hasta un máximo de 20 indicadores a la vez. Las claves de los indicadores se pueden enviar individualmente, como una lista o en un rango (ej. "SF1-SF5").
* **nombres:** str/list. Nombre(s) de las columas del DataFrame. De no proporcionarse se usarán los indicadores. 
* **inicio:** str. Fecha donde iniciar la serie en formato YYYY(-MM-DD). De no proporcionarse será desde el primer valor disponible. 
* **fin:** str. Fecha donde terminar la serie en formato YYYY(-MM-DD). De no proporcionarse será hasta el último valor disponible.
* **decimales:** bool. En caso de ser verdadero regresa la serie con todos los decimales. Si es falso elimina los ceros decimales al final del punto decimal (los menos significativos).
* **incremento:** str, opcional. En caso de definir alguna de las opciones regresa la serie como el incremento porcentual de alguna observación previa. Las opciones disponibles son las siguientes:

                        PorcObsAnt: Porcentaje de incremento con respecto a la observación anterior.
                        PorcAnual: Porcentaje de incremento con respecto a la misma observación del año anterior.
                        PorcAcumAnual: Porcentaje de incremento con respecto a la última observación del año anterior.

Regresa un DataFrame con los datos de los indicadores proporcionados por la API de Banxico. El DataFrame resultante tiene una columna por cada indicador y un DateTimeIndex con la fecha de los valores. 
        
Nota: esta función concatena todos los indicadores en un solo DataFrame por lo que es recomendable usarla para varias series con una misma frecuencia. En caso de no querer concatenar las series se debe usar un indicador a la vez.  

##### metadatos()

```python
Banxico.metadatos(indicadores)
```
**Parámetros**
* **indicadores:** str/list. Clave(s) de los indicadores a consultar. Puede ser hasta un máximo de 20 indicadores a la vez. Las claves de los indicadores se pueden enviar individualmente, como una lista o en un rango (ej. "SF1-SF5").

Regresa un DataFrame con los metadatos de los indicadores.

##### dato_oportuno()

```python
Banxico.dato_oportuno(indicadores, 
                      nombres = None,
                      decimales = True
                      incremento = None)
```
**Parámetros**
* **indicadores:** str/list. Clave(s) de los indicadores a consultar. Puede ser hasta un máximo de 20 indicadores a la vez. Las claves de los indicadores se pueden enviar individualmente, como una lista o en un rango (ej. "SF1-SF5").
* **nombres:** str/list. Nombre(s) de las columas del DataFrame. De no proporcionarse se usarán los indicadores. 
* **decimales:** bool. En caso de ser verdadero regresa la serie con todos los decimales. Si es falso elimina los ceros decimales al final del punto decimal (los menos significativos).
* **incremento:** str, opcional. En caso de definir alguna de las opciones regresa la serie como el incremento porcentual de alguna observación previa. Las opciones disponibles son las siguientes:

                        PorcObsAnt: Porcentaje de incremento con respecto a la observación anterior.
                        PorcAnual: Porcentaje de incremento con respecto a la misma observación del año anterior.
                        PorcAcumAnual: Porcentaje de incremento con respecto a la última observación del año anterior.

Regresa un DataFrame con el último dato de los indicadores proporcionados por la API de Banxico.
        
Nota: esta función concatena todos los indicadores en un solo DataFrame por lo que es recomendable usarla para varias series con una misma frecuencia. En caso de no querer concatenar las series se debe usar un indicador a la vez. 

## Uso


```python
# uso actual

from BANXICOpy import Banxico
```


```python
token = '274066f5ed9caabbbbe6417dae8d4359f06ac5c853619436d9c82d55ed58fe83'
bmx = Banxico(token)
```


```python
# varias series dentro de una lista
indicadores = ["SF61745", "SP68257", "SF43718"]
nombres = ["Tasa Objetivo", "UDIS", "Tipo de Cambio"]
df = bmx.obtener_series(indicadores, nombres, inicio = '2017-05-13')
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Tasa Objetivo</th>
      <th>UDIS</th>
      <th>Tipo de Cambio</th>
    </tr>
    <tr>
      <th>fecha</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-05-13</th>
      <td>6.5</td>
      <td>5.745952</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-14</th>
      <td>6.5</td>
      <td>5.746996</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2017-05-15</th>
      <td>6.5</td>
      <td>5.748040</td>
      <td>18.6700</td>
    </tr>
    <tr>
      <th>2017-05-16</th>
      <td>6.5</td>
      <td>5.749085</td>
      <td>18.6183</td>
    </tr>
    <tr>
      <th>2017-05-17</th>
      <td>6.5</td>
      <td>5.750129</td>
      <td>18.6761</td>
    </tr>
  </tbody>
</table>
</div>




```python
# varias series como un rango
df = bmx.obtener_series('SF1-SF5')
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SF1</th>
      <th>SF2</th>
      <th>SF3</th>
      <th>SF4</th>
      <th>SF5</th>
    </tr>
    <tr>
      <th>fecha</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1960-01-01</th>
      <td>6969.0</td>
      <td>7230.0</td>
      <td>NaN</td>
      <td>261.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1960-02-01</th>
      <td>6877.0</td>
      <td>7193.0</td>
      <td>NaN</td>
      <td>315.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1960-03-01</th>
      <td>6745.0</td>
      <td>7079.0</td>
      <td>NaN</td>
      <td>333.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1960-04-01</th>
      <td>6900.0</td>
      <td>7177.0</td>
      <td>NaN</td>
      <td>277.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1960-05-01</th>
      <td>6714.0</td>
      <td>7059.0</td>
      <td>NaN</td>
      <td>346.0</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
# series como tasas de crecimiento
base = bmx.obtener_series('SF44043', 'Base Monetaria', inicio = '2020', incremento='PorcAnual')
base.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Base Monetaria</th>
    </tr>
    <tr>
      <th>fecha</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-01-01</th>
      <td>4.08</td>
    </tr>
    <tr>
      <th>2020-01-02</th>
      <td>4.37</td>
    </tr>
    <tr>
      <th>2020-01-03</th>
      <td>4.47</td>
    </tr>
    <tr>
      <th>2020-01-04</th>
      <td>4.87</td>
    </tr>
    <tr>
      <th>2020-01-05</th>
      <td>4.87</td>
    </tr>
  </tbody>
</table>
</div>




```python
metadatos = bmx.metadatos(indicadores)
metadatos
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>idSerie</th>
      <th>titulo</th>
      <th>fechaInicio</th>
      <th>fechaFin</th>
      <th>periodicidad</th>
      <th>cifra</th>
      <th>unidad</th>
      <th>versionada</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SP68257</td>
      <td>Valor de UDIS</td>
      <td>04/04/1995</td>
      <td>10/08/2022</td>
      <td>Diaria</td>
      <td>Tipo de Cambio</td>
      <td>Unidades de Inversión</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SF61745</td>
      <td>Tasa objetivo</td>
      <td>21/01/2008</td>
      <td>04/08/2022</td>
      <td>Diaria</td>
      <td>Porcentajes</td>
      <td>Sin Unidad</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SF43718</td>
      <td>Tipo de cambio                                ...</td>
      <td>12/11/1991</td>
      <td>03/08/2022</td>
      <td>Diaria</td>
      <td>Tipo de Cambio</td>
      <td>Pesos por Dólar</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>




```python
bmx.dato_oportuno("SF61745", 'tasa_objetivo', incremento='PorcAcumAnual')
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tasa_objetivo</th>
    </tr>
    <tr>
      <th>fecha</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2022-08-04</th>
      <td>40.91</td>
    </tr>
  </tbody>
</table>
</div>


