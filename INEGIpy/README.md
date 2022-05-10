# INEGIpy

INEGIpy es una librería para interactuar fácilmente con los datos del Instituto Nacional de Geografía y Estadística (INEGI) desde Python. Su propósito es apoyar en la creación de consultas automatizadas y  en el acceso a la información para el análisis de datos. 

De la información que ofrece el INEGI actualmente se cuenta con una clase dedicada al [Banco de Indicadores](https://www.inegi.org.mx/servicios/api_indicadores.html), otra dedicada al [DENUE](https://www.inegi.org.mx/servicios/api_denue.html), otra a la información del [Marco Geoestadístico](https://www.inegi.org.mx/servicios/catalogoUnico.html) y finalmente una dedicada al [Sistema de Ruteo de México](https://www.inegi.org.mx/servicios/Ruteo/Default.html). 

También se encuentra en constrcción un módulo de Series dedicado a consultas automatizadas de los principales indicadores económicos como el PIB, INPC, Ocupación, etc. 

## Principales características

* Permite un acceso rápido a las bases de datos del INEGI sin necesidad de descargas.
* Regresa la información en DataFrames o GeoDataFrames listos para su uso en Python.
* Para el caso de los indicadores económicos, el DataFrame resultante cuenta con un DateTimeIndex y una columna para cada indicador.
* Para las bases con información georeferenciada (DENUE, Marco Geoestadístico y Ruteo) se regresa un GeoDataFrame listo para realizar operaciones espaciales. 
    * El DENUE obtiene tanto la ubicción de los establecimientos como información sobre la actividad económica y el número de trabajadores.
    * El Marco Geoestadístico permite obtener la información de la población según el [Censo de Población y Vivienda del 2020](https://www.inegi.org.mx/programas/ccpv/2020/) así como la información vectorial de las áreas que se especifiquen en cualquier nivel de agregación espacial. Evita descargar un montón de archivos Shape para realizar mapas y operaciones espaciales.
    * El Servicio de Ruteo además de calcular rutas entre puntos ofrece información georeferenciada sobre diferentes destinos los cuales pueden ser destinos turísticos o lugares de interés como aeropuertos, puertos, servicios médicos, o centros educativos de nivel superior. También ofrece detalles sobre el costo de las rutas y los precios promedio de los combustibles. 

## Requerimientos

* pandas
* numpy
* requests
* shapely
* geopandas

La instalación de GeoPandas puede ser un poco complicada de manejar por lo que se recomieda [instalarla previemente](https://geopandas.org/en/stable/getting_started/install.html).


## Instalación

```pip install INEGIpy```

## Documentación

* [Indicadores](#Indicadores)
    * [obtener_df](#obtener_df)
    * [grafica](#grafica)
    * [Uso](#Uso)  
* [MarcoGeoestadistico](#MarcoGeoestadistico)
    * [Entidades](#Entidades())
    * [Municipios](#Municipios())
    * [LocalidadesAmanzanadas](#LocalidadesAmanzanadas())
    * [LocalidadesRuralesPuntuales](#LocalidadesRuralesPuntuales())
    * [AGEBs](#AGEBs())
    * [Manzanas](#Manzanas())
    * [Vialidades](#Vialidades())
    * [Uso]()
* [DENUE](#DENUE)
    * [Buscar](#Buscar())
    * [Ficha](#Ficha())
    * [Nombre](#Nombre())
    * [BuscarEntidad](#BuscarEntidad())
    * [BuscarAreaAct](#BuscarAreaAct())
    * [Cuantificar](#Cuantificar())
    * [Uso]()
* [Ruteo](#Ruteo)
    * [BuscarDestino](#BuscarDestino())
    * [BuscarLinea](#BuscarLinea())
    * [CalcularRuta](#CalcularRuta())
    * [DetalleRuta](#DetalleRuta())
    * [Combustibles](#Combustibles())
    * [Uso]()
* [Casos de uso](#Casos-de-uso)
    * [Indicadores y MarcoGeoestadistico](#Indicadores-y-MarcoGeoestadistico)
    * [DENUE, Ruteo y MarcoGeoestadistico](#DENUE,-Ruteo-y-MarcoGeoestadistico)

### Indicadores

``` python
class INEGIpy.Indicadores(token)
```

**Parámetros** 
   * **token:** str. Token proporcionado por el INEGI.

La clase ```Indicadores``` contiene los métodos y atributos relacionados a la API del Banco de Indicadores y el Banco de Información Económica. Esta API permite consultar los datos de los indicadores económicos disponibles a nivel nacional, por entidad federativa y municipio. Las claves de los indicadores y más información sobre la API se pueden obtener en el [constructor de consultas](https://www.inegi.org.mx/servicios/api_indicadores.html). Esta clase requiere un [token generado por el INEGI](https://www.inegi.org.mx/app/desarrolladores/generatoken/Usuarios/token_Verify).

#### Métodos

##### obtener_df()

```python
Indicadores.obtener_df(indicadores, 
                       nombres = None, 
                       inicio = None, 
                       fin = None)
```
**Parámetros**
* **indicadores:** str/list. Clave(s) de los indicadores de la consulta. 
* **nombres:** str/list. Nombre(s) de las columas del DataFrame. De no proporcionarse se usarán los indicadores. 
* **inicio:** str. Fecha donde iniciar la serie en formato YYYY(-MM-DD). De no proporcionarse será desde el primer valor disponible. 
* **fin:** str. Fecha donde terminar la serie en formato YYYY(-MM-DD). De no proporcionarse será hasta el último valor disponible.

Regresa un DataFrame con la información de los indicadores. El DataFrame resultante tiene una columna por cada indicador y un DateTimeIndex con la fecha de los valores. 

#### Uso


```python
from INEGIpy import Indicadores
token = 'TuToken'
inegi = Indicadores(token)
```


```python
df = inegi.obtener_df(indicadores = ["289242","289242"], 
                      nombres = ['Indicador Coincidente', 'Indicador Adelantado'], 
                      inicio = '2000', 
                      fin = '2010')

display(df.head())
display(df.tail())
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Indicador Coincidente</th>
      <th>Indicador Adelantado</th>
    </tr>
    <tr>
      <th>fechas</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2005-03-01</th>
      <td>106701738.0</td>
      <td>106701738.0</td>
    </tr>
    <tr>
      <th>2005-06-01</th>
      <td>106999770.0</td>
      <td>106999770.0</td>
    </tr>
    <tr>
      <th>2005-09-01</th>
      <td>107306131.0</td>
      <td>107306131.0</td>
    </tr>
    <tr>
      <th>2005-12-01</th>
      <td>107615497.0</td>
      <td>107615497.0</td>
    </tr>
    <tr>
      <th>2006-03-01</th>
      <td>107928527.0</td>
      <td>107928527.0</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Indicador Coincidente</th>
      <th>Indicador Adelantado</th>
    </tr>
    <tr>
      <th>fechas</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2009-12-01</th>
      <td>113408736.0</td>
      <td>113408736.0</td>
    </tr>
    <tr>
      <th>2010-03-01</th>
      <td>113764977.0</td>
      <td>113764977.0</td>
    </tr>
    <tr>
      <th>2010-06-01</th>
      <td>114114587.0</td>
      <td>114114587.0</td>
    </tr>
    <tr>
      <th>2010-09-01</th>
      <td>114468031.0</td>
      <td>114468031.0</td>
    </tr>
    <tr>
      <th>2010-12-01</th>
      <td>114818957.0</td>
      <td>114818957.0</td>
    </tr>
  </tbody>
</table>
</div>


### MarcoGeoestadistico

``` python
class INEGIpy.MarcoGeoestadistico()
```

La clase ```MarcoGeoestadistico``` contiene los métodos relacionados al [Servicio Web del Catálogo Único de Claves Geoestadísticas](https://www.inegi.org.mx/servicios/catalogoUnico.html), el cual contiene los datos de población del [Censo de Población y Vivienda 2020](https://www.inegi.org.mx/programas/ccpv/2020/) y la información vectorial de las áreas geoestadísticas que define el INEGI en el [Marco Geoestadístico](https://www.inegi.org.mx/temas/mg/): Entidades, Municipios, Localidades, AGEBs, Manzanas y Vialidades. Esta clase permite obtener GeoDataFrames para cada nivel de agregación espacial por lo que resulta principalmente útil para realizar operaciones espaciales y para la elaboración de mapas. También resulta útil para obtener las claves geoestadísticas de entidades, municipios y localidades utilizando el nombre de estas áreas, lo cual permite asociar datos estadísticos y resultados de encuestas a sus respectivas unidades geográficas. 

#### Métodos

##### Entidades()

```python
MarcoGeoestadistico.Entidades(entidades = None, 
                              nombres = None, 
                              as_geodf = True)
```
**Parámetros**
* **entidades:** str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
* **nombres:** str/list. Nombre(s) de los estados a buscar. Si se define este parámetro obtiene las áreas geoestadísticas estatales cuyo nombre contenga el texto proporcionado sin necesidad de proporcionar las claves de las entidades. No distingue entre mayúsculas y minúsculas pero sí considera acentos.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe las claves o nombres de las entidades a consultar y obtiene el DataFrame/GeoDataFrame con la información de las áreas geoestadísticas estatales.
        
Si no se especifíca una entidad regresa la información para todas las Entidades Federativas.

##### Municipios()

```python
MarcoGeoestadistico.Municipios(entidades = None, 
                               municipios = None, 
                               nombres = None, 
                               claves_concatenadas = None, 
                               as_geodf = True)
```
**Parámetros**
* **entidades:** str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
* **municipios:** str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001).
* **nombres:** str/list. Nombre(s) de los municipios a buscar. Si se define este parámetro obtiene las áreas geoestadísticas municipales cuyo nombre contenga el texto proporcionado sin necesidad de proporcionar las claves de los municipios. No distingue entre mayúsculas y minúsculas pero sí considera acentos.
* **claves_concatendas:** str/list. Clave(s) concatenada con los niveles de agregación espacial (ej. 01001).
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe claves de entidades, municipios, claves concatenadas o los nombres de los municipios a consultar y obtiene el DataFrame/GeoDataFrame con la información de las áreas geoestadísticas municipales. 

Si solo se definen las entidades la función regresa todos los municipios de estas entidades. Para consultar municipios en específico se puede hacer a través del nombre de los municipios, definiendo una entidad y las claves de los municipios por separado o definiendo claves concatenadas de entidad y municpio. La diferencia entre definir las claves separadas y las claves concatenadas es que en el primer caso solo se puede definir una entidad y uno o más municipios mientras que las claves concatenadas permiten elegir municipios específicos de diferentes entidades o incluso hacer combinaciones entre consultar municipios específicos y todos los municipios de alguna entidad. 

Si no se especifícan los parámetros regresa un DataFrame con todos los municipios de México. 
        
Nota: si se pasa una lista de áreas con nivel de agregación mayor no se puede definir un municipio en específico a buscar. En este caso se regresan todos los municipios de la lista de mayor agregación. Lo mismo sucede para los siguientes niveles de desagregación: si se define una lista de municipios o entidades no se puede definir una localidad en específico y así sucesivamente.  

##### LocalidadesAmanzanadas()

```python
MarcoGeoestadistico.LocalidadesAmanzanadas(entidades = None, 
                                           municipios = None, 
                                           localidades = None, 
                                           nombres = None, 
                                           claves_concatenadas = None, 
                                           ambito = None, 
                                           as_geodf = True)
```
**Parámetros**
* **entidades:** str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
* **municipios:** str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001).
* **localidades:** str/list. Clave(s) de cuatro dígitos de las localidades a buscar (ej. 0001 )
* **nombres:** str/list. Nombre(s) de las localidades a buscar. Si se define este parámetro obtiene las localidades amanzanadas cuyo nombre contenga el texto proporcionado sin necesidad de proporcionar las claves de las localidades. No distingue entre mayúsculas y minúsculas pero sí considera acentos.
* **claves_concatendas:** str/list. Clave(s) concatenada con los niveles de agregación espacial.
* **ambito**: str. ["urbano"|"rural"] Define el ámbito de las localidades. Si se define un ámbito no se puede definir una localidad en específico y se debe definir tanto entidad como municipio.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe claves de entidades, municipios, localidades, claves concatenadas o los nombres de las localidades a consultar y obtiene el DataFrame/GeoDataFrame con la información de las áreas geoestadísticas a nivel localidad amanzanada.

Al igual que con los municipios, si no se definen las claves de las localidades regresa todas las localidades del último nivel de desagregación definido. Para consultar localidades en específico se puede hacer a través del nombre de las localidades, definiendo una entidad, un municipio y una o más claves de las localidades por separado o definiendo claves concatenadas de entidad, municipio y localidad. La diferencia entre definir las claves separadas y las claves concatenadas es que en el primer caso solo se puede definir una clave para los niveles de agregación previos (solo una entidad y un municipio) mientras que las claves concatenadas permiten elegir localidades específicas de diferentes entidades, municipios o incluso hacer combinaciones entre consultar localidades específicas y todas las localidades de algún nivel previo.

Se debe definir al menos las entidades, de lo contrario no tendrá resultados.

Nota: Si se define un ámbito de las localidades, la función del Servicio Web requiere que se defina una entidad y municipio, de lo contrario no tendrá resultados. En este caso regresa todas las localidades del municipio que correspondan a este ámbito.

##### LocalidadesRuralesPuntuales()

```python
MarcoGeoestadistico.LocalidadesRuralesPuntuales(entidades = None, 
                                                municipios = None, 
                                                localidades = None, 
                                                nombres = None, 
                                                claves_concatenadas = None,
                                                as_geodf = True)
```
**Parámetros**
* **entidades:** str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
* **municipios:** str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001).
* **localidades:** str/list. Clave(s) de cuatro dígitos de las localidades a buscar (ej. 0001 )
* **nombres:** str/list. Nombre(s) de las localidades a buscar. Si se define este parámetro obtiene las localidades amanzanadas cuyo nombre contenga el texto proporcionado sin necesidad de proporcionar las claves de las localidades. No distingue entre mayúsculas y minúsculas pero sí considera acentos.
* **claves_concatendas:** str/list. Clave(s) concatenada con los niveles de agregación espacial.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe claves de entidades, municipios, localidades, claves concatenadas o los nombres de las localidades a consultar y obtiene el DataFrame/GeoDataFrame con la información de las áreas geoestadísticas a nivel localidad rural puntual.

Al igual que con los municipios y las localidades amanzanadas, si no se definen las claves de las localidades regresa todas las localidades del último nivel de desagregación definido. Para consultar localidades en específico se puede hacer a través del nombre de las localidades, definiendo una entidad, un municipio y las claves de las localidades por separado o definiendo claves concatenadas de entidad, municipio y localidad. La diferencia entre definir las claves separadas y las claves concatenadas es que en el primer caso solo se puede definir una clave para los niveles de agregación previos (solo una entidad y un municipio) mientras que las claves concatenadas permiten elegir localidades específicas de diferentes entidades, municipios o incluso hacer combinaciones entre consultar localidades específicas y todas las localidades de algún nivel previo.

Se debe definir al menos las entidades, de lo contrario no tendrá resultados.

##### AGEBs()

```python
MarcoGeoestadistico.AGEBs(entidades = None,
                          municipios = None, 
                          localidades = None, 
                          agebs = None
                          claves_concatenadas = None, 
                          ambito = 'urbano', 
                          as_geodf = True)
```
**Parámetros**
* **entidades:** str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
* **municipios:** str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001).
* **localidades:** str/list. Clave(s) de cuatro dígitos de las localidades a buscar (ej. 0001 )
* **agebs:** str/list. Clave(s) de cuatro dígitos con las AGEBs a buscar (ej. 2000).
* **claves_concatendas:** str/list. Clave(s) concatenada con los niveles de agregación espacial.
* **ambito**: str. ['urbano'|'rural'] Define el ambito de las localidades.  A diferencia de las localidades amanzanadas siempre se debe especificar el ambitos de las AGEBs a buscar. Por default son urbanas.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe claves de entidades, municipios, localidades, agebs o claves concatenadas a consultar y obtiene el DataFrame/GeoDataFrame con la información de las áreas geoestadísticas a nivel Área Geoestadística Básica (AGEB).

Al igual que con las áreas previas, si no se definen las claves de las AGEBs regresa todas las AGEBs del último nivel de desagrecgación definido. Para consultar AGEBs en específico se puede hacer definiendo una entidad, un municipio, una localidad y las claves de las AGEBs por separado o definiendo claves concatenadas de entidad, municipio, localidad y ageb. La diferencia entre definir las claves separadas y las claves concatenadas es que en el primer caso solo se puede definir una clave para los niveles de agregación previos (solo una entidad, un municipio y una localidad) mientras que las claves concatenadas permiten elegir AGEBs específicas de diferentes entidades, municipios o incluso hacer combinaciones entre consultar AGEBs específicas y todos las AGEBs de algún nivel previo.

Se debe definir al menos las entidades, de lo contrario no tendrá resultados.
        
##### Manzanas()

<span style="color:red"> *Advertencia: El GeoJSON que regresa esta función del Servicio Web del Catálogo Único de Claves Geoestadísticas contiene varias celdas vacías. Ya he enviado correos al INEGI respecto a este problema pero aún no recibo respuesta así que por lo pronto esta función aún regresa un GeoDataFrame con las celdas vacías.*</span>

```python
MarcoGeoestadistico.Manzanas(entidades = None,
                             municipios = None, 
                             localidades = None,
                             claves_concatenadas = None, 
                             ambito = 'urbano', 
                             as_geodf = True)
```
**Parámetros**
* **entidades:** str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
* **municipios:** str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001).
* **localidades:** str/list. Clave(s) de cuatro dígitos de las localidades a buscar (ej. 0001 )
* **claves_concatendas:** str/list. Clave(s) concatenada con los niveles de agregación espacial.
* **ambito**: str. ["urbano"|'rural'] Define el ambito de las localidades. Si se define un ámbito se debe definir entidad, municipio y localidad.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe claves de entidades, municipios, localidades o claves concatenadas a consultar y obtiene el DataFrame/GeoDataFrame con la información de las áreas geoestadísticas a nivel manzana.

A diferencia de las áreas previas, no se pueden elegir manzanas en específico. El nivel de desagregación menor que se puede definir es de localidad. Igual sigue aplicando la diferencia entre definir las claves de manera separa y las calves concatenadas: las claves concatenadas permien diferentes combinaciones de entidades, municipios y localidades.

Se debe definir al menos las entidades, de lo contrario no tendrá resultados.

Nota: Si se define un ámbito de las manzanas, la función del Servicio Web requiere que se defina una entidad, municipio y localidad, de lo contrario no tendrá resultados. En este caso regresa todas las manzanas de la localidad que correspondan a este ámbito.

##### Vialidades()

```python
MarcoGeoestadistico.Vialidades(entidades,
                               municipios, 
                               localidades = None,
                               claves_concatenadas = None,  
                               as_geodf = True)
```
**Parámetros**
* **entidades:** str/list. Clave(s) AGEE de dos dígitos (01 a 32) de las entidades federativas a buscar.
* **municipios:** str/list. Clave(s) AGEM de tres dígitos de los municipios a buscar (ej. 001).
* **localidades:** str/list. Clave(s) de cuatro dígitos de las localidades a buscar (ej. 0001 )
* **claves_concatendas:** str/list. Clave(s) concatenada con los niveles de agregación espacial.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe claves de entidades, municipios, localidades o claves concatenadas a consultar y obtiene el DataFrame/GeoDataFrame con la información de las vialidades de un municipio o localidad.

Al igual que con las manzanas, el nivel de desagregación menor que se puede definir es de localidad y sigue aplicando la diferencia entre definir las claves de manera separa y las calves concatenadas.

Se debe definir al menos entidad y municipio, de lo contrario no tendrá resultados. 

Para más información consultar: https://www.inegi.org.mx/servicios/catalogoUnico.html

#### Uso


```python
from INEGIpy import MarcoGeoestadistico

marco = MarcoGeoestadistico()
```


```python
edos = marco.Entidades(nombres = ['ciudad de méxico','méxico','querétaro','san luis','nuevo león'])
edos.plot()
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_12_1.png)
    



```python
nl_municipios = marco.Municipios(entidades='19')
display(nl_municipios.head(10))
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>geometry</th>
      <th>cvegeo</th>
      <th>cve_agee</th>
      <th>cve_agem</th>
      <th>nom_agem</th>
      <th>cve_cab</th>
      <th>pob</th>
      <th>pob_fem</th>
      <th>pob_mas</th>
      <th>viv</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>POLYGON ((-99.26413 25.91413, -99.26396 25.914...</td>
      <td>19013</td>
      <td>19</td>
      <td>013</td>
      <td>China</td>
      <td>0001</td>
      <td>9930</td>
      <td>4969</td>
      <td>4961</td>
      <td>3268</td>
    </tr>
    <tr>
      <th>1</th>
      <td>POLYGON ((-100.50415 24.45637, -100.49612 24.4...</td>
      <td>19014</td>
      <td>19</td>
      <td>014</td>
      <td>Doctor Arroyo</td>
      <td>0001</td>
      <td>36088</td>
      <td>18028</td>
      <td>18060</td>
      <td>9229</td>
    </tr>
    <tr>
      <th>2</th>
      <td>POLYGON ((-100.59196 25.25505, -100.58917 25.2...</td>
      <td>19017</td>
      <td>19</td>
      <td>017</td>
      <td>Galeana</td>
      <td>0001</td>
      <td>40903</td>
      <td>20459</td>
      <td>20444</td>
      <td>11185</td>
    </tr>
    <tr>
      <th>3</th>
      <td>POLYGON ((-99.92667 25.41633, -99.92575 25.415...</td>
      <td>19038</td>
      <td>19</td>
      <td>038</td>
      <td>Montemorelos</td>
      <td>0001</td>
      <td>67428</td>
      <td>33859</td>
      <td>33569</td>
      <td>20912</td>
    </tr>
    <tr>
      <th>4</th>
      <td>POLYGON ((-100.06809 25.99270, -100.06272 25.9...</td>
      <td>19025</td>
      <td>19</td>
      <td>025</td>
      <td>General Zuazua</td>
      <td>0001</td>
      <td>102149</td>
      <td>50305</td>
      <td>51844</td>
      <td>29632</td>
    </tr>
    <tr>
      <th>5</th>
      <td>POLYGON ((-100.39313 26.39482, -100.39268 26.3...</td>
      <td>19045</td>
      <td>19</td>
      <td>045</td>
      <td>Salinas Victoria</td>
      <td>0001</td>
      <td>86766</td>
      <td>42631</td>
      <td>44135</td>
      <td>25430</td>
    </tr>
    <tr>
      <th>6</th>
      <td>POLYGON ((-100.01204 26.16508, -100.00888 26.1...</td>
      <td>19028</td>
      <td>19</td>
      <td>028</td>
      <td>Higueras</td>
      <td>0001</td>
      <td>1386</td>
      <td>662</td>
      <td>724</td>
      <td>422</td>
    </tr>
    <tr>
      <th>7</th>
      <td>POLYGON ((-100.18769 26.32793, -100.18853 26.3...</td>
      <td>19051</td>
      <td>19</td>
      <td>051</td>
      <td>Villaldama</td>
      <td>0001</td>
      <td>3573</td>
      <td>1786</td>
      <td>1787</td>
      <td>1267</td>
    </tr>
    <tr>
      <th>8</th>
      <td>POLYGON ((-99.01603 26.09548, -99.00699 26.085...</td>
      <td>19015</td>
      <td>19</td>
      <td>015</td>
      <td>Doctor Coss</td>
      <td>0001</td>
      <td>1360</td>
      <td>703</td>
      <td>657</td>
      <td>494</td>
    </tr>
    <tr>
      <th>9</th>
      <td>POLYGON ((-99.80176 25.98994, -99.80161 25.989...</td>
      <td>19016</td>
      <td>19</td>
      <td>016</td>
      <td>Doctor González</td>
      <td>0001</td>
      <td>3256</td>
      <td>1584</td>
      <td>1672</td>
      <td>1029</td>
    </tr>
  </tbody>
</table>
</div>



```python
# definir las claves en su forma concatenada en vez de separadas por nivel de agregación permite realizar dioferentes combinaciones entre áreas:
# si se definen de manera separada una vez que se da una lista de áreas ya no se pueden definir los niveles siguiente. Es decir, si se pasa una lista de estados 
# no se puede definir un municipio, de manera que las posibilidades se reducen a una lista de estados, un estado con una lista de municipios, 
# un estado y un municipio con una lsita de localidades, y así sucesivamente. 

localidades = marco.LocalidadesAmanzanadas(entidades = '09', municipios = ['002','003','004','005'], as_geodf = False)
display(localidades)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cvegeo</th>
      <th>cve_agee</th>
      <th>cve_agem</th>
      <th>cve_loc</th>
      <th>nom_loc</th>
      <th>ambito</th>
      <th>latitud</th>
      <th>longitud</th>
      <th>altitud</th>
      <th>pob</th>
      <th>viv</th>
      <th>cve_carta</th>
      <th>estatus</th>
      <th>periodo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>090020001</td>
      <td>09</td>
      <td>002</td>
      <td>0001</td>
      <td>Azcapotzalco</td>
      <td>URBANO</td>
      <td>19.4841028</td>
      <td>-99.1843606</td>
      <td>2244</td>
      <td>432205</td>
      <td>134204</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>090030001</td>
      <td>09</td>
      <td>003</td>
      <td>0001</td>
      <td>Coyoacán</td>
      <td>URBANO</td>
      <td>19.3502139</td>
      <td>-99.1621456</td>
      <td>2247</td>
      <td>614447</td>
      <td>191646</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>090040063</td>
      <td>09</td>
      <td>004</td>
      <td>0063</td>
      <td>Santa Rosa</td>
      <td>RURAL</td>
      <td>19.3233383</td>
      <td>-99.2949614</td>
      <td>2857</td>
      <td>818</td>
      <td>204</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>090040010</td>
      <td>09</td>
      <td>004</td>
      <td>0010</td>
      <td>Cruz Blanca</td>
      <td>RURAL</td>
      <td>19.3177850</td>
      <td>-99.3240103</td>
      <td>2982</td>
      <td>728</td>
      <td>192</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>090040050</td>
      <td>09</td>
      <td>004</td>
      <td>0050</td>
      <td>La Venta</td>
      <td>RURAL</td>
      <td>19.3343756</td>
      <td>-99.3102128</td>
      <td>2862</td>
      <td>486</td>
      <td>124</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>5</th>
      <td>090040073</td>
      <td>09</td>
      <td>004</td>
      <td>0073</td>
      <td>Los Aguacates</td>
      <td>RURAL</td>
      <td>19.3699019</td>
      <td>-99.3107319</td>
      <td>2725</td>
      <td>514</td>
      <td>129</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2017-02-28</td>
    </tr>
    <tr>
      <th>6</th>
      <td>090040054</td>
      <td>09</td>
      <td>004</td>
      <td>0054</td>
      <td>Puerto las Cruces (Monte las Cruces)</td>
      <td>RURAL</td>
      <td>19.2948611</td>
      <td>-99.3476211</td>
      <td>3200</td>
      <td>1233</td>
      <td>323</td>
      <td>E14A38</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>7</th>
      <td>090040020</td>
      <td>09</td>
      <td>004</td>
      <td>0020</td>
      <td>San Lorenzo Acopilco</td>
      <td>URBANO</td>
      <td>19.3310047</td>
      <td>-99.3256817</td>
      <td>2936</td>
      <td>26042</td>
      <td>6627</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>8</th>
      <td>090040001</td>
      <td>09</td>
      <td>004</td>
      <td>0001</td>
      <td>Cuajimalpa de Morelos</td>
      <td>URBANO</td>
      <td>19.3573503</td>
      <td>-99.2997922</td>
      <td>2780</td>
      <td>186693</td>
      <td>52530</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>9</th>
      <td>090050001</td>
      <td>09</td>
      <td>005</td>
      <td>0001</td>
      <td>Gustavo A. Madero</td>
      <td>URBANO</td>
      <td>19.4829453</td>
      <td>-99.1134708</td>
      <td>2230</td>
      <td>1173351</td>
      <td>340301</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
  </tbody>
</table>
</div>



```python
# en cambio, las claves concatenadas permiten diferentes municipios de diferentes entidades o incluso hacer combinaciones entre los niveles de agregación 

localidades = marco.LocalidadesAmanzanadas(claves_concatenadas = ['01','09002','190310357'], as_geodf = False)
display(localidades.tail())
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cvegeo</th>
      <th>cve_agee</th>
      <th>cve_agem</th>
      <th>cve_loc</th>
      <th>nom_loc</th>
      <th>ambito</th>
      <th>latitud</th>
      <th>longitud</th>
      <th>altitud</th>
      <th>pob</th>
      <th>viv</th>
      <th>cve_carta</th>
      <th>estatus</th>
      <th>periodo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>392</th>
      <td>010050106</td>
      <td>01</td>
      <td>005</td>
      <td>0106</td>
      <td>La Tomatina</td>
      <td>RURAL</td>
      <td>21.9014614</td>
      <td>-102.4151539</td>
      <td>1962</td>
      <td>1076</td>
      <td>249</td>
      <td>F13D18</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>393</th>
      <td>010050007</td>
      <td>01</td>
      <td>005</td>
      <td>0007</td>
      <td>Los Arquitos</td>
      <td>RURAL</td>
      <td>21.9234458</td>
      <td>-102.3857450</td>
      <td>1908</td>
      <td>1214</td>
      <td>252</td>
      <td>F13D18</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>394</th>
      <td>010050019</td>
      <td>01</td>
      <td>005</td>
      <td>0019</td>
      <td>Cieneguitas</td>
      <td>RURAL</td>
      <td>21.8954869</td>
      <td>-102.4265219</td>
      <td>1990</td>
      <td>208</td>
      <td>54</td>
      <td>F13D18</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>395</th>
      <td>090020001</td>
      <td>09</td>
      <td>002</td>
      <td>0001</td>
      <td>Azcapotzalco</td>
      <td>URBANO</td>
      <td>19.4841028</td>
      <td>-99.1843606</td>
      <td>2244</td>
      <td>432205</td>
      <td>134204</td>
      <td>E14A39</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
    <tr>
      <th>396</th>
      <td>190310357</td>
      <td>19</td>
      <td>031</td>
      <td>0357</td>
      <td>Anzures</td>
      <td>URBANO</td>
      <td>25.6905483</td>
      <td>-100.1183050</td>
      <td>0397</td>
      <td>5222</td>
      <td>1521</td>
      <td>G14C26</td>
      <td>1</td>
      <td>2015-06-01</td>
    </tr>
  </tbody>
</table>
</div>



```python
# podemos usar los valores de una tabla para apoyar en la búsqueda de otros valores cuando no se tenga la clave previamente
cve_concatenada = nl_municipios[nl_municipios.nom_agem == 'Monterrey'].cvegeo.iloc[0]
print('Clave Concatenada de Monterrey: {}'.format(cve_concatenada))
mty_agebs = marco.AGEBs(claves_concatenadas=cve_concatenada)
mty_agebs.plot()
```

    Clave Concatenada de Monterrey: 19039
    




    <AxesSubplot:>




    
![png](./README_PNGs/output_16_2.png)
    



```python
muns = ['021','039','046','048','049','019','026','006'] #claves de municipios correspondientes a la Zona Metropolitana de Monterrey
zmmty_manzanas = marco.Manzanas(entidades = '19', municipios = muns)
zmmty_manzanas.plot()
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_17_1.png)
    



```python
mty_vialidades = marco.Vialidades(entidades='19',municipios='039')
display(mty_vialidades.head())
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>geometry</th>
      <th>cve_agee</th>
      <th>cve_agem</th>
      <th>cve_loc</th>
      <th>cve_via</th>
      <th>nomvial</th>
      <th>tipovial</th>
      <th>ambito</th>
      <th>sentido</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>LINESTRING (-100.37921 25.77703, -100.37914 25...</td>
      <td>19</td>
      <td>039</td>
      <td>0001</td>
      <td>10523</td>
      <td>Canal de Aztlán</td>
      <td>Calle</td>
      <td>Urbana</td>
      <td>Dos sentidos</td>
    </tr>
    <tr>
      <th>1</th>
      <td>LINESTRING (-100.24432 25.51150, -100.24430 25...</td>
      <td>19</td>
      <td>039</td>
      <td>0001</td>
      <td>04897</td>
      <td>El Barro</td>
      <td>Calle</td>
      <td>Urbana</td>
      <td>Dos sentidos</td>
    </tr>
    <tr>
      <th>2</th>
      <td>LINESTRING (-100.39648 25.76720, -100.39619 25...</td>
      <td>19</td>
      <td>039</td>
      <td>0001</td>
      <td>10621</td>
      <td>Almanzora</td>
      <td>Calle</td>
      <td>Urbana</td>
      <td>Dos sentidos</td>
    </tr>
    <tr>
      <th>3</th>
      <td>LINESTRING (-100.38965 25.77122, -100.38990 25...</td>
      <td>19</td>
      <td>039</td>
      <td>0001</td>
      <td>14309</td>
      <td>Paseo de la Reserva</td>
      <td>Calle</td>
      <td>Urbana</td>
      <td>Dos sentidos</td>
    </tr>
    <tr>
      <th>4</th>
      <td>LINESTRING (-100.36222 25.77592, -100.36264 25...</td>
      <td>19</td>
      <td>039</td>
      <td>0001</td>
      <td>09818</td>
      <td>15 de Abril</td>
      <td>Privada</td>
      <td>Urbana</td>
      <td>Dos sentidos</td>
    </tr>
  </tbody>
</table>
</div>


### DENUE

``` python
class INEGIpy.DENUE(token)
```
**Parámetros** 
   * **token:** token proporcionado por el INEGI.

La clase ```DENUE``` contiene los métodos relacionados a la API del [Directorio Estadístico Nacional de Unidades Económicas](https://www.inegi.org.mx/servicios/api_denue.html), el cual permite consultar los datos de identificación, ubicación, actividad económica y tamaño de más de 5 millones de establecimientos a nivel nacional, por entidad federativa y municipio. Los métodos de esta clase permiten obtener un DataFrame o un GeodataFrame con la información de los establecimientos dadas ciertas condiciones como una ubicación y un radio, nombre del establecimiento, ubicación geográfica, actividad económica y estrato. Esta clase requiere un [token generado por el INEGI](https://www.inegi.org.mx/app/desarrolladores/generatoken/Usuarios/token_Verify).

Para cada establecimiento el INEGI proporciona la siguiente información: 
* CLEE
* Id de establecimiento
* Nombre del establecimiento
* Razón social
* Clase de la actividad económica
* Estrato (Personal ocupado)
* Tipo de la vialidad
* Calle
* Número exterior
* Número interior
* Colonia
* Código postal
* Localidad, municipio y entidad federativa
* Teléfono
* Correo electrónico
* Página de internet
* Tipo de establecimiento
* Longitud
* Latitud

#### Métodos

##### Buscar()

```python
DENUE.Buscar(condiciones, 
             latitud, 
             longitud, 
             distancia, 
             as_geodf = True)
```
**Parámetros**
* **condiciones:** str/list. Palabra(s) a buscar en el nombre del establecimiento, razón social, calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad. Para buscar todos los establecimientos se deberá ingresar la palabra "todos".
* **latitud:** float. Latitud que define el punto en el mapa a partir del cual se hará la consulta alrededor.
* **longitud:** float. Longitud que define el punto en el mapa a partir del cual se hará la consulta alrededor.
* **distancia:** int. Distancia en metros a partir de las coordenadas que definen el radio de búsqueda. La distancia máxima es de 5 000 metros.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe una o más condiciones, una coordenada y la distancia radial en metros con lo cual realiza una consulta de todos los establecimientos que cumplan las condiciones definidas dentro de la cirunferencia.

Regresa un DataFrame o GeoDataFrame con la información de los establecimientos consultados. 

##### Ficha()

```python
DENUE.Ficha(clave, 
            as_geodf = True)
```
**Parámetros**
* **clave:** str. ID única del establecimiento.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Recibe la clave única de un establecimiento y obtiene su información.

Regresa un DataFrame o GeoDataFrame con la información de la consulta. 

##### Nombre()

```python
DENUE.Nombre(nombre, 
             entidad = '00', 
             registro_inicial = 1, 
             registro_final = 10, 
             as_geodf = True)
```
**Parámetros**
* **nombre:** str. Nombre del establecimiento ó razón social.
* **entidad:** str. Clave de dos dígitos de la entidad federativa (01 a 32). Para incluir todas las entidades se especifica 00.
* **registro_inicial:** int. Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
* **registro_final:** int. Número de registro final que se mostrará en los resultados de la búsqueda.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Realiza una consulta de todos los establecimientos por nombre o razón social. La consulta puede ser acotada por entidad federativa. 

Regresa un DataFrame o GeoDataFrame con la información de la consulta. 

##### BuscarEntidad()

```python
DENUE.BuscarEntidad(condiciones, 
                    entidad = '00', 
                    registro_inicial = 1, 
                    registro_final = 10, 
                    as_geodf = True):
```
**Parámetros**
* **condiciones:** str/list. Palabra(s) a buscar en el nombre del establecimiento, razón social, calle, colonia, clase de la actividad económica, entidad federativa, municipio y localidad. Para buscar todos los establecimientos se deberá ingresar la palabra "todos".
* **entidad:** str. Clave de dos dígitos de la entidad federativa (01 a 32). Para incluir todas las entidades se especifica 00.
* **registro_inicial:** int. Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
* **registro_final:** int. Número de registro final que se mostrará en los resultados de la búsqueda.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Realiza una consulta de todos los establecimientos que cumplan las condiciones definidas y puede ser acotada por entidad federativa.

Regresa un DataFrame o GeoDataFrame con la información de la consulta. 

##### BuscarAreaAct()

```python
DENUE.BuscarAreaActEstr(nombre,
                        clave_area = '', 
                        clave_actividad = '',
                        registro_inicial = 1, 
                        registro_final = 10, 
                        clave_establecimiento = '0', 
                        estrato = '0'
                        as_geodf = True)
```
**Parámetros**
* **nombre:** str. Nombre del establecimiento a buscar.
* **clave_area**: str. Clave de dos a dieciseis caracteres que indentifica el área geográfica de acuerdo con el Marco Geoestadístico. En caso de no definir una clave se regresan todos los establecimientos del país.
                                    Dos caracteres para definir un estado (ej. 01 a 32).
                                    Cinco caracteres dígitos para definir un municipio (ej. 01001).
                                    Nueve caracteres para definir una localidad (ej. 010010001).
                                    Trece caracteres para definir una Área Geoestadística Básica (AGEB) (ej. 010010001216A).
                                    Dieciseis caracteres para definir una manzana (ej. 010010001465A004).
* **clave_actividad**: str. Clave de dos a seis dígitos que identifica el área de actividad económica del establecimiento de acuerdo con el [Sistema de Clasificación Industrial de América del Norte 2018](https://www.inegi.org.mx/app/scian/). En caso de no definir una clave se regresan todas las áreas.
                                    Dos dígitos para definir un sector (ej.46).
                                    Tres dígitos para definir un subsector (ej. 464).
                                    Cuatro dígitos para definir una rama (ej. 4641).
                                    Cinco dígitos para definir una subrama (ej. 46411).
                                    Seis dígitos para definir una clase (ej. 464111).
* **registro_inicial:** int. Número de registro a partir del cuál se mostrarán los resultados de la búsqueda.
* **registro_final:** int. Número de registro final que se mostrará en los resultados de la búsqueda.
* **clave_establecimiento:** str. Clave única del establecimiento. Para incluir todos los establecimientos se especifica 0.
* **estrato**: str. Clave de un dígito que identifica el estrato del establecimiento (cantidad de trabajadores). Para incluir todos los tamaños se especifica 0.
                                    1. Para incluir de 0 a 5 personas.
                                    2. Para incluir de 6 a 10 personas.
                                    3. Para incluir de 11 a 30 personas.
                                    4. Para incluir de 31 a 50 personas.
                                    5. Para incluir de 51 a 100 personas.
                                    6. Para incluir de 101 a 250 personas.
                                    7. Para incluir de 251 y más personas.
* **as_geodf:** bool. Si el valor es verdadero regresa un GeoDataFrame para facilitar el análisis espacial. 

Realiza una consulta de todos los establecimientos con la opción de acotar la búsqueda por área geográfica, actividad económica, nombre, clave del establecimiento y estrato económico.

El INEGI divide esta función en dos: BuscarAreaAct y BuscarAreaActEstr. La diferencia entre ambas es que la segunda permite definir el estrato económico de los establecimientos y la primera no. Sin embargo, la segunda función permite la opción de buscar para todos los estratos cuando esta variable es igual a '0' lo cual hace que los resultados de ambas funciones sean iguales. Es por ello que en esta clase solo se definió un método para la segunda función ya que esta es más general y puede regresar los mismos resultados que la primera. A pesar de esto se conserva el nombre de la primera función por facilidad. 

Regresa un DataFrame o GeoDataFrame con la información de la consulta. 

##### Cuantificar()

```python
DENUE.Cuantificar(clave_area = '0', 
                  clave_actividad = '0', 
                  estrato = '0')
```
**Parámetros**
* **clave_area**: str/list. Clave(s) de dos a nueve caracteres que indentifican el área geográfica de acuerdo con el Marco Geoestadístico. Esta función solo permite definir hasta nivel localidad. En caso de no definir una clave se regresan todos los establecimientos del país.
                                    Dos caracteres para definir un estado (ej. 01 a 32).
                                    Cinco caracteres dígitos para definir un municipio (ej. 01001).
                                    Nueve caracteres para definir una localidad (ej. 010010001).
* **clave_actividad**: str/list. Clave(s) de dos a seis dígitos que identifican el área de actividad económica de los establecimientos de acuerdo con el [Sistema de Clasificación Industrial de América del Norte 2018](https://www.inegi.org.mx/app/scian/). Para incluir todas las actividades se especifica 0.
                                    Dos dígitos para definir un sector (ej.46).
                                    Tres dígitos para definir un subsector (ej. 464).
                                    Cuatro dígitos para definir una rama (ej. 4641).
                                    Cinco dígitos para definir una subrama (ej. 46411).
                                    Seis dígitos para definir una clase (ej. 464111).
* **estrato**: str. Clave de un dígito que identifica el estrato del establecimiento (cantidad de trabajadores). Para incluir todos los tamaños se especifica 0.
                                    1. Para incluir de 0 a 5 personas.
                                    2. Para incluir de 6 a 10 personas.
                                    3. Para incluir de 11 a 30 personas.
                                    4. Para incluir de 31 a 50 personas.
                                    5. Para incluir de 51 a 100 personas.
                                    6. Para incluir de 101 a 250 personas.
                                    7. Para incluir de 251 y más personas.

Realiza un conteo de todos los establecimientos con la opción de acotar la búsqueda por área geográfica, actividad económica y estrato.
        
A diferencia de las otras funciones permite múltiples claves para definir áreas geográficas y actividades económicas. 
        
Otra diferencia importante es que el resultado de esta consulta no regresa valores de las coordenadas para obtener un GeoDataFrame.

Regresa un DataFrame con las siguientes columnas:
* **AE:** Clave de la actividad económica.
* **AG:** Clave del Área Geoestadística.
* **Total:** Número de establecimientos que cumplen las condiciones definidas. 

#### Uso


```python
from INEGIpy import DENUE
token = 'TuToken'
denue = DENUE(token)
```


```python
df = denue.Buscar('papeleria', latitud = 19.32593, longitud = -99.17253, distancia = 3_000)
df.plot()
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_22_1.png)
    



```python
df = denue.Ficha(clave = '993591', as_geodf=False)
display(df)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CLEE</th>
      <th>Id</th>
      <th>Nombre</th>
      <th>Razon_social</th>
      <th>Clase_actividad</th>
      <th>Estrato</th>
      <th>Tipo_vialidad</th>
      <th>Calle</th>
      <th>Num_Exterior</th>
      <th>Num_Interior</th>
      <th>...</th>
      <th>Ubicacion</th>
      <th>Telefono</th>
      <th>Correo_e</th>
      <th>Sitio_internet</th>
      <th>Tipo</th>
      <th>Longitud</th>
      <th>Latitud</th>
      <th>CentroComercial</th>
      <th>TipoCentroComercial</th>
      <th>NumLocal</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>09003465311009331000000000U4</td>
      <td>993591</td>
      <td>PAPELERIA COPY PLUS</td>
      <td></td>
      <td>Comercio al por menor de artículos de papelería</td>
      <td>0 a 5 personas</td>
      <td>CALLE</td>
      <td>DALIAS</td>
      <td>351</td>
      <td></td>
      <td>...</td>
      <td>COYOACÁN, Coyoacán, CIUDAD DE MÉXICO</td>
      <td></td>
      <td>COPYPLUS@LIVE.COM.MX</td>
      <td></td>
      <td>Fijo</td>
      <td>-99.17327717</td>
      <td>19.32546362</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>1 rows × 22 columns</p>
</div>



```python
df = denue.Nombre(nombre = 'oxxo', registro_final= 5, as_geodf=False)
display(df)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CLEE</th>
      <th>Id</th>
      <th>Nombre</th>
      <th>Razon_social</th>
      <th>Clase_actividad</th>
      <th>Estrato</th>
      <th>Tipo_vialidad</th>
      <th>Calle</th>
      <th>Num_Exterior</th>
      <th>Num_Interior</th>
      <th>...</th>
      <th>Ubicacion</th>
      <th>Telefono</th>
      <th>Correo_e</th>
      <th>Sitio_internet</th>
      <th>Tipo</th>
      <th>Longitud</th>
      <th>Latitud</th>
      <th>tipo_corredor_industrial</th>
      <th>nom_corredor_industrial</th>
      <th>numero_local</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>05027468411000082000008448S0</td>
      <td>241407</td>
      <td>OXXO GAS SUC. AEROPUERTO RAMOS SLW</td>
      <td>SERVICIOS GASOLINEROS DE MEXICO SA DE CV</td>
      <td>Comercio al por menor de gasolina y diesel</td>
      <td>6 a 10 personas</td>
      <td>BOULEVARD</td>
      <td>MIGUEL RAMOS ARIZPE</td>
      <td>157</td>
      <td></td>
      <td>...</td>
      <td>RAMOS ARIZPE, Ramos Arizpe, COAHUILA DE ZARAGOZA</td>
      <td></td>
      <td>ATENCIONCLIENTES@OXXOGAS.COM</td>
      <td>WWW.OXXOGAS.COM</td>
      <td>Fijo</td>
      <td>-100.93934020</td>
      <td>25.54427014</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>05030468411001072000008448S7</td>
      <td>241447</td>
      <td>OXXO GAS SUC. ISIDRO LOPEZ</td>
      <td>SERVICIOS GASOLINEROS DE MEXICO SA DE CV</td>
      <td>Comercio al por menor de gasolina y diesel</td>
      <td>6 a 10 personas</td>
      <td>CALLE</td>
      <td>Isidro López Zertuche</td>
      <td>2600</td>
      <td>0</td>
      <td>...</td>
      <td>SALTILLO, Saltillo, COAHUILA DE ZARAGOZA</td>
      <td></td>
      <td>ATENCIONCLIENTES@OXXOGAS.COM</td>
      <td>WWW.OXXOGAS.COM</td>
      <td>Fijo</td>
      <td>-100.99782115</td>
      <td>25.44916466</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>05030468411000203000008448S6</td>
      <td>242057</td>
      <td>OXXO GAS SUC. ROTONDA</td>
      <td>SERVICIOS GASOLINEROS DE MEXICO SA DE CV</td>
      <td>Comercio al por menor de gasolina y diesel</td>
      <td>11 a 30 personas</td>
      <td>BOULEVARD</td>
      <td>PRESIDENTE CARDENAS</td>
      <td>1332</td>
      <td>0</td>
      <td>...</td>
      <td>SALTILLO, Saltillo, COAHUILA DE ZARAGOZA</td>
      <td></td>
      <td>ATENCIONCLIENTES@OXXOGAS.COM</td>
      <td>WWW.OXXOGAS.COM</td>
      <td>Fijo</td>
      <td>-100.98514108</td>
      <td>25.42521447</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>05030468411000932000008448S5</td>
      <td>241448</td>
      <td>OXXO GAS SUC. SAN RAMON MTD</td>
      <td>SERVICIOS GASOLINEROS DE MEXICO SA DE CV</td>
      <td>Comercio al por menor de gasolina y diesel</td>
      <td>6 a 10 personas</td>
      <td>PERIFERICO</td>
      <td>Luis Echeverría</td>
      <td>6133</td>
      <td>0</td>
      <td>...</td>
      <td>SALTILLO, Saltillo, COAHUILA DE ZARAGOZA</td>
      <td></td>
      <td>ATENCIONCLIENTES@OXXOGAS.COM</td>
      <td>WWW.OXXOGAS.COM</td>
      <td>Fijo</td>
      <td>-100.97589129</td>
      <td>25.41574357</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>05030468411000972001008448S6</td>
      <td>241449</td>
      <td>OXXO GAS SUC. VILLAFERRE SLW</td>
      <td>SERVICIOS GASOLINEROS DE MEXICO SA DE CV</td>
      <td>Comercio al por menor de gasolina y diesel</td>
      <td>11 a 30 personas</td>
      <td>BOULEVARD</td>
      <td>VENUSTIANO CARRANZA</td>
      <td>7625</td>
      <td></td>
      <td>...</td>
      <td>SALTILLO, Saltillo, COAHUILA DE ZARAGOZA</td>
      <td></td>
      <td></td>
      <td></td>
      <td>Fijo</td>
      <td>-100.96658880</td>
      <td>25.49452935</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>5 rows × 22 columns</p>
</div>



```python
df = denue.BuscarEntidad('papeleria', entidad='09', registro_final = 5, as_geodf=False)
display(df)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CLEE</th>
      <th>Id</th>
      <th>Nombre</th>
      <th>Razon_social</th>
      <th>Clase_actividad</th>
      <th>Estrato</th>
      <th>Tipo_vialidad</th>
      <th>Calle</th>
      <th>Num_Exterior</th>
      <th>Num_Interior</th>
      <th>...</th>
      <th>Ubicacion</th>
      <th>Telefono</th>
      <th>Correo_e</th>
      <th>Sitio_internet</th>
      <th>Tipo</th>
      <th>Longitud</th>
      <th>Latitud</th>
      <th>tipo_corredor_industrial</th>
      <th>nom_corredor_industrial</th>
      <th>numero_local</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>09007433410000391001000000U7</td>
      <td>744113</td>
      <td>@PUNTO103</td>
      <td></td>
      <td>Comercio al por menor de artículos de papelería</td>
      <td>6 a 10 personas</td>
      <td>CALLE</td>
      <td>BATALLA DE LOMA ALTA</td>
      <td>1261</td>
      <td>0</td>
      <td>...</td>
      <td>IZTAPALAPA, Iztapalapa, CIUDAD DE MÉXICO</td>
      <td></td>
      <td>INTERNET_PUNTO103@HOTMAIL.COM</td>
      <td></td>
      <td>Fijo</td>
      <td>-99.07598675</td>
      <td>19.38021053</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>09012465311010991000000000U0</td>
      <td>915779</td>
      <td>1001 ARTICULOS</td>
      <td></td>
      <td>Comercio al por menor de artículos de papelería</td>
      <td>0 a 5 personas</td>
      <td>PRIVADA</td>
      <td>GUANAJUATO</td>
      <td>71</td>
      <td></td>
      <td>...</td>
      <td>TLALPAN, Tlalpan, CIUDAD DE MÉXICO</td>
      <td></td>
      <td></td>
      <td></td>
      <td>Fijo</td>
      <td>-99.18847911</td>
      <td>19.28477654</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>09015465311019173000003309S2</td>
      <td>6760792</td>
      <td>187 OFFICE MAX</td>
      <td>OPERADORA OMX SA DE CV</td>
      <td>Comercio al por menor de artículos de papelería</td>
      <td>11 a 30 personas</td>
      <td>CALLE</td>
      <td>ISABEL LA CATÓLICA</td>
      <td>39</td>
      <td></td>
      <td>...</td>
      <td>CUAUHTÉMOC, Cuauhtémoc, CIUDAD DE MÉXICO</td>
      <td></td>
      <td></td>
      <td></td>
      <td>Fijo</td>
      <td>-99.13651997</td>
      <td>19.43194609</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>09002465311006551000000000U2</td>
      <td>742977</td>
      <td>309- 310- 316 PAPELERIA PROHOGAR</td>
      <td></td>
      <td>Comercio al por menor de artículos de papelería</td>
      <td>0 a 5 personas</td>
      <td>CALLE</td>
      <td>12</td>
      <td>0</td>
      <td>309</td>
      <td>...</td>
      <td>AZCAPOTZALCO, Azcapotzalco, CIUDAD DE MÉXICO</td>
      <td></td>
      <td></td>
      <td></td>
      <td>Fijo</td>
      <td>-99.15394547</td>
      <td>19.47588543</td>
      <td>MERCADO PUBLICO</td>
      <td>MERCADO PUBLICO SEDECO PRO HOGAR</td>
      <td>309, 310 Y 316</td>
    </tr>
    <tr>
      <th>4</th>
      <td>09002465311009171000000000U6</td>
      <td>9201165</td>
      <td>407 PAPELERIA</td>
      <td></td>
      <td>Comercio al por menor de artículos de papelería</td>
      <td>0 a 5 personas</td>
      <td>CALLE</td>
      <td>12</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>AZCAPOTZALCO, Azcapotzalco, CIUDAD DE MÉXICO</td>
      <td></td>
      <td></td>
      <td></td>
      <td>Fijo</td>
      <td>-99.15394547</td>
      <td>19.47588543</td>
      <td>MERCADO PUBLICO</td>
      <td>MERCADO PUBLICO SEDECO PRO HOGAR</td>
      <td>407</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 22 columns</p>
</div>



```python
df = denue.BuscarAreaAct('soriana', clave_area = '09003', clave_actividad = '46', as_geodf = False)
display(df)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CLEE</th>
      <th>Id</th>
      <th>Nombre</th>
      <th>Razon_social</th>
      <th>Clase_actividad</th>
      <th>Estrato</th>
      <th>Tipo_vialidad</th>
      <th>Calle</th>
      <th>Num_Exterior</th>
      <th>Num_Interior</th>
      <th>...</th>
      <th>CLASE_ACTIVIDAD_ID</th>
      <th>EDIFICIO_PISO</th>
      <th>SECTOR_ACTIVIDAD_ID</th>
      <th>SUBSECTOR_ACTIVIDAD_ID</th>
      <th>RAMA_ACTIVIDAD_ID</th>
      <th>SUBRAMA_ACTIVIDAD_ID</th>
      <th>EDIFICIO</th>
      <th>Tipo_Asentamiento</th>
      <th>Fecha_Alta</th>
      <th>AreaGeo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>09003461110029761000000000U8</td>
      <td>7717912</td>
      <td>ABARROTES SORIANA</td>
      <td></td>
      <td>Comercio al por menor en tiendas de abarrotes,...</td>
      <td>0 a 5 personas</td>
      <td>CALLE</td>
      <td>PASCLE</td>
      <td>252</td>
      <td></td>
      <td>...</td>
      <td>461110</td>
      <td></td>
      <td>46</td>
      <td>461</td>
      <td>4611</td>
      <td>46111</td>
      <td></td>
      <td>COLONIA</td>
      <td>2019-11</td>
      <td>090030001</td>
    </tr>
    <tr>
      <th>1</th>
      <td>09003462111000116000008292S5</td>
      <td>6313488</td>
      <td>CENTROS COMERCIALES SORIANA SUCURSAL 300 MIRAM...</td>
      <td>TIENDAS SORIANA SA DE CV</td>
      <td>Comercio al por menor en supermercados</td>
      <td>101 a 250 personas</td>
      <td>PEATONAL</td>
      <td>1 Oriente (Avenida Canal de Miramontes)</td>
      <td>2600</td>
      <td>0</td>
      <td>...</td>
      <td>462111</td>
      <td></td>
      <td>46</td>
      <td>462</td>
      <td>4621</td>
      <td>46211</td>
      <td></td>
      <td>COLONIA</td>
      <td>2010-07</td>
      <td>090030001</td>
    </tr>
    <tr>
      <th>2</th>
      <td>09003461122004151001000000U6</td>
      <td>908875</td>
      <td>POLLERIA SORIANO</td>
      <td></td>
      <td>Comercio al por menor de carne de aves</td>
      <td>11 a 30 personas</td>
      <td>CALLE</td>
      <td>MARIQUITA SANCHEZ</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>461122</td>
      <td></td>
      <td>46</td>
      <td>461</td>
      <td>4611</td>
      <td>46112</td>
      <td></td>
      <td>COLONIA</td>
      <td>2014-12</td>
      <td>090030001</td>
    </tr>
    <tr>
      <th>3</th>
      <td>09003462111000206000008292S4</td>
      <td>6313076</td>
      <td>SORIANA PLAZA CANTIL</td>
      <td>TIENDAS SORIANA SA DE CV</td>
      <td>Comercio al por menor en supermercados</td>
      <td>101 a 250 personas</td>
      <td>AVENIDA</td>
      <td>Aztecas</td>
      <td>270</td>
      <td>0</td>
      <td>...</td>
      <td>462111</td>
      <td></td>
      <td>46</td>
      <td>462</td>
      <td>4621</td>
      <td>46211</td>
      <td></td>
      <td>COLONIA</td>
      <td>2010-07</td>
      <td>090030001</td>
    </tr>
    <tr>
      <th>4</th>
      <td>09003462111000166000008292S0</td>
      <td>6315772</td>
      <td>TIENDAS SORIANA SUC 288 GRAN SUR</td>
      <td>TIENDAS SORIANA SA DE CV</td>
      <td>Comercio al por menor en supermercados</td>
      <td>101 a 250 personas</td>
      <td>AVENIDA</td>
      <td>AVENIDA DEL IMÁN</td>
      <td>151</td>
      <td>0</td>
      <td>...</td>
      <td>462111</td>
      <td></td>
      <td>46</td>
      <td>462</td>
      <td>4621</td>
      <td>46211</td>
      <td></td>
      <td>COLONIA</td>
      <td>2010-07</td>
      <td>090030001</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 34 columns</p>
</div>



```python
df = denue.Cuantificar(clave_area = '09003', clave_actividad = ['464111', '464112'], estrato= '1') #farmacias con y sin minisuper en Coyoacán
display(df)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AE</th>
      <th>AG</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>464111</td>
      <td>09003</td>
      <td>293</td>
    </tr>
    <tr>
      <th>1</th>
      <td>464112</td>
      <td>09003</td>
      <td>46</td>
    </tr>
  </tbody>
</table>
</div>


### Ruteo

``` python
class INEGIpy.Ruteo(token)
```
**Parámetros** 
   * **token:** token proporcionado por el INEGI.
   
La clase ```Ruteo``` contiene los métodos relacionados a la API del [Sistema de Ruteo de México](https://www.inegi.org.mx/servicios/Ruteo/Default.html). Esta API utiliza la Red Nacional de Caminos y todas sus especificaciones técnicas, para generar el resultado de acuerdo a las restricciones de circulación en el mundo real como sentidos de circulación vehicular, pasos a desnivel, distribuidores viales, enlaces, retornos glorietas, y maniobras prohibidas. Además, considera tres posibles rutas: preferentemente libre, preferentemente cuota y la ruta sugerida para dar alternativas de traslado o viaje con diferente coste. Además permite obtener información georeferenciada de los destinos que incluye la Red Nacional de Caminos como localidades urbanas y rurales o sitios de interés como aeropuertos, puertos, servicios médicos, centros educativos de nivel superior, playas, cascadas, zonas arqueológicas, museos, pueblos mágicos, y muchos más. 

Para el cálculo de rutas el INEGI define dos formas de marcar el inicio y final: 
* **Destino:** Sitio de partida o llegada para una ruta. Están integrados por localidades, instalaciones de transporte como aeropuertos y puertos, así como sitios de interés contenidos en la Red Nacional de Caminos.
* **Línea:** Es cualquier segmento de la Red Nacional de Caminos.

Los destinos y líneas se obtienen de sus respectivas funciones ```BuscarDestino``` y ```BuscarLinea```, los DataFrames resultantes de estas funciones contienen los valores necesarios para las funciones de ruteo. Las funciones de ruteo reciben estos DataFrames o diccionarios equivalentes para calcular las rutas.

#### Métodos

##### BuscarDestino()

```python
Ruteo.BuscarDestino(busqueda, 
                    cantidad, 
                    proyeccion = 'GRS80')
```
**Parámetros**
* **busqueda:** str. Define el nombre o parte del destino que se desea encontrar. Se puede utilizar una coma para especificar la entidad federativa, p. e. “San Juan, Jalisco”.
* **cantidad:** int. Número de destinos que se desea obtener. 
* **proyeccion:** str. Define la proyección de los puntos resultantes. GRS80 para coordenadas geográficas y MERC para coordenadas Spherical Mercator. Por default será GRS80. 
        
Permite buscar destinos como localidades urbanas y rurales, así como los sitios de interés que pueden ser instalaciones de servicios como aeropuertos, puertos, servicios médicos, centros educativos de nivel superior, así como sitios atractivos para el turismo como playas, cascadas, zonas arqueológicas, museos, pueblos mágicos, y más. El DataFrame resultante contiene los valores necesarios para calcular una ruta desde o hacia el destino.

Obtiene un GeoDataFrame con la información de las siguientes columnas:

* **id_dest:** identificador único del destino.*
* **ent_abr:** abreviación de la entidad federativa en donde se encuentra el destino.
* **nombre:** nombre del destino.
* **geometry:** geometría del punto geográfico del destino.

**Valor necesario para calcular una ruta desde o hacia el destino definido*

##### BuscarLinea()

```python
Ruteo.BuscarLinea(lat, 
                  lng, 
                  escala = 1_000_000, 
                  proyeccion = 'GRS80')
```
**Parámetros**
* **lat:** float. Latitud de la coordenada.
* **lng:** float. Longitud de la coordenada.
* **escala:** int. Valor de la escala de visualización. Por default es 1,000,000.
* **proyeccion:** str. Define la proyección de los puntos resultantes. GRS80 para coordenadas geográficas y MERC para coordenadas Spherical Mercator. Por default será GRS80. 
        
Obtiene un GeoDataFrame con la información de la línea registrada en la Red Nacional de Caminos más cercana a una coordenada. El DataFrame resultante contiene los valores necesarios para calcular una ruta desde o hacia la coordenada:

* **id_routing_net:** identificador de la línea.*
* **source:** source de la línea.*
* **target:** target de la línea.*
* **nombre:** nombre de la línea (carretera, camino o avenida).
* **geometry:** geometría de un punto de la línea más cercano a las coordenadas enviadas.

**Valores necesarios para calcular una ruta desde o hacia la coordenada definida*

##### CalcularRuta()

```python
Ruteo.CalcularRuta(linea_inicial = None, 
                   linea_final = None, 
                   destino_inicial = None, 
                   destino_final = None, 
                   tipo_vehiculo = 0, 
                   ruta = 'optima', 
                   ejes_excedentes = 0, 
                   saltar_lineas = None, 
                   proyeccion = 'GRS80')
```
**Parámetros**
* **linea_inicial:** DataFrame con las columnas id_routing_net, source y target de la línea inicial obtenido por la función BuscarLinea. También acepta un diccionario con la misma información.
* **linea_final:** DataFrame con las columnas id_routing_net, source y target de la línea final obtenido por la función BuscarLinea. También acepta un diccionario con la misma información.
* **destino_inicial:** DataFrame con la columna id_dest del destino inicial obtenido por la función BuscarDestino. También acepta el valor de id_dest en string o integer. 
* **destino_final:** DataFrame con la columna id_dest del destino final obtenido por la función BuscarDestino. También acepta el valor de id_dest en string o integer. 
* **tipo_vehiculo:** int. Clave de un dígito que identifica el tipo de vehículo con el cual calcular la ruta. Por default es 0. 
                                0: Motocicleta
                                1: Automóvil
                                2: Autobús dos ejes
                                3: Autobús tres ejes
                                4: Autobús cuatro ejes
                                5: Camión dos ejes
                                6: Camión tres ejes
                                7: Camión cuatro ejes
                                8: Camión cinco ejes
                                9: Camión seis ejes
                                10: Camión siete ejes
                                11: Camión ocho ejes
                                12: Camión nueve ejes
* **ruta:** str. ["optima" | "libre" | "cuota"]. Tipo de ruta que se desea obtener. 
* **ejes_excedentes:** int. Clave de un dígito que identifica el número de ejes excedentes del vehículo. Por default es 0.
                                0: Sin ejes excedentes
                                1: un eje excedente
                                2: dos ejes excedentes
                                3: tres ejes excedentes
                                4: cuatro ejes excedentes
                                5: cinco ejes excedentes
* **saltar_lineas:** list. Lista con los id_routing_net de las líneas por las cuales la ruta no pasará por ningún motivo. Por default es None.
* **proyeccion:** str. Define la proyección de los puntos resultantes. GRS80 para coordenadas geográficas y MERC para coordenadas Spherical Mercator. Por default será GRS80. 
        
Obtiene un GeoDataFrame con la ruta calculada por Sistema de Ruteo de México y la Red Nacional de Caminos. Se puede obtener rutas de línea-línea, destino-destino, línea-destino y destino-linea. El DataFrame resultante contine las columnas:

* **long_km:** longitud en kilómetros de la ruta.
* **tiempo_min:** tiempo promedio en minutos de traslado de la ruta.
* **peaje:** False si la ruta no pasa por alguna caseta de cobro y True si pasa por al menos una.
* **costo_caseta:** cantidad en pesos que pagará al transitar por esta ruta.
* **eje_excedente:** cantidad en pesos que pagaría al transitar por esta ruta en caso que el parámetro e sea mayor o igual a 1. Si e es igual a cero, no se devolverá este resultado.
* **advertencia:** devuelve una advertencia cuando la ruta tiene algunas características específicas que el usuario debiera conocer.
* **geometry:** geometría de la línea con la ruta.


##### DetalleRuta()

```python
Ruteo.DetalleRuta(linea_inicial = None, 
                  linea_final = None, 
                  destino_inicial = None, 
                  destino_final = None, 
                  tipo_vehiculo = 0, 
                  ruta = 'optima', 
                  ejes_excedentes = 0, 
                  saltar_lineas = None, 
                  proyeccion = 'GRS80')
```
**Parámetros**
* **linea_inicial:** DataFrame con las columnas id_routing_net, source y target de la línea inicial obtenido por la función BuscarLinea. También acepta un diccionario con la misma información.
* **linea_final:** DataFrame con las columnas id_routing_net, source y target de la línea final obtenido por la función BuscarLinea. También acepta un diccionario con la misma información.
* **destino_inicial:** DataFrame con la columna id_dest del destino inicial obtenido por la función BuscarDestino. También acepta el valor de id_dest en string o integer. 
* **destino_final:** DataFrame con la columna id_dest del destino final obtenido por la función BuscarDestino. También acepta el valor de id_dest en string o integer. 
* **tipo_vehiculo:** int. Clave de un dígito que identifica el tipo de vehículo con el cual calcular la ruta. Por default es 0. 
                                0: Motocicleta
                                1: Automóvil
                                2: Autobús dos ejes
                                3: Autobús tres ejes
                                4: Autobús cuatro ejes
                                5: Camión dos ejes
                                6: Camión tres ejes
                                7: Camión cuatro ejes
                                8: Camión cinco ejes
                                9: Camión seis ejes
                                10: Camión siete ejes
                                11: Camión ocho ejes
                                12: Camión nueve ejes
* **ruta:** str. ["optima"|"libre"|"cuota"]. Tipo de ruta que se desea obtener. 
* **ejes_excedentes:** int. Clave de un dígito que identifica el número de ejes excedentes del vehículo. Por default es 0.
                                0: Sin ejes excedentes
                                1: un eje excedente
                                2: dos ejes excedentes
                                3: tres ejes excedentes
                                4: cuatro ejes excedentes
                                5: cinco ejes excedentes
* **saltar_lineas:** list. Lista con los id_routing_net de las líneas por las cuales la ruta no pasará por ningún motivo. Por default es None.
* **proyeccion:** str. Define la proyección de los puntos resultantes. GRS80 para coordenadas geográficas y MERC para coordenadas Spherical Mercator. Por default será GRS80. 

Obtiene un GeoDataFrame con los detalles de la ruta calculada por Sistema de Ruteo de México y la Red Nacional de Caminos. Se puede obtener rutas de línea-línea, destino-destino, línea-destino y destino-linea. El DataFrame resultante contine las columnas:

* **direccion:** Dirección de giro y nombre de la carretera, camino o vialidad.
* **long_m:** Longitud del segmento en metros.
* **tiempo_min:** Tiempo de recorrido del segmento en minutos.
* **costo_caseta:** Cantidad en pesos a pagar por transitar por el segmento.
* **punto_caseta:** Geometría de la caseta asociada al segmento (en caso de existir una asociación).
* **eje_excedente:** Cantidad en pesos a pagar por los ejes excedentes.
* **giro:** Valor numérico que indica hacia donde se debe girar.
                                0: Continúe derecho
                                1: Gire a la izquierda
                                2: Gire a la derecha
                                3: Gire ligeramente a la izquierda
                                4: Gire ligeramente a la derecha
* **geometry:** Geometría con los puntos que marcan a los segmentos.
                                
##### Combustibles()

```python
Ruteo.Combustibles()
```
Regresa un DataFrame con los 4 tipos de combustibles más comunes y su costo promedio que se consultan el primer día hábil de cada semana en la página web de la [Comisión Reguladora de Energía del Gobierno Federal](https://www.gob.mx/cre)

Nota: el dato que provee esta API solo es una referencia en función del precio promedio nacional excluyendo las 7 regiones sobre la frontera. También lo que refiere al gas LP el precio es un promedio ponderado que publica la Comisión Reguladora de Energía.

El DataFrame resultante contine las columnas:

* **tipo_costo:** Tipo y costo promedio del combustible.
* **costo:** Costo promedio del combustible.
* **tipo:** Nombre del combustible.

#### Uso


```python
from INEGIpy import Ruteo
token = 'TuToken'
ruteo = Ruteo(token)
```


```python
destino_inicial = ruteo.BuscarDestino(busqueda = 'palacio de bellas artes, ciudad de m', cantidad = 1)
destino_final = ruteo.BuscarDestino(busqueda = 'zócalo, ciudad de m', cantidad = 1)
display(destino_inicial)
display(destino_final)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ent_abr</th>
      <th>id_dest</th>
      <th>nombre</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CDMX</td>
      <td>6773</td>
      <td>Palacio de Bellas Artes, Cuauhtémoc</td>
      <td>POINT (-99.14137 19.43524)</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ent_abr</th>
      <th>id_dest</th>
      <th>nombre</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CDMX</td>
      <td>4437</td>
      <td>Plaza de la Constitución, Cuauhtémoc</td>
      <td>POINT (-99.13320 19.43263)</td>
    </tr>
  </tbody>
</table>
</div>



```python
linea_inicial = ruteo.BuscarLinea(lat = 19.435237353, lng = -99.141374223) # equvalente a buscar bellas artes pero con las coordenadas
linea_final = ruteo.BuscarLinea(lat = 19.4326290000001, lng = -99.133203) # equivalente a buscar zócalo con las coordenadas
display(linea_inicial)
display(linea_final)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>source</th>
      <th>id_routing_net</th>
      <th>nombre</th>
      <th>target</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>701895</td>
      <td>695491</td>
      <td>Eje vial Central Lázaro Cárdenas</td>
      <td>701896</td>
      <td>POINT (-99.14070 19.43514)</td>
    </tr>
  </tbody>
</table>
</div>



<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>source</th>
      <th>id_routing_net</th>
      <th>nombre</th>
      <th>target</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>769724</td>
      <td>1475230</td>
      <td>Calle Plaza de la Constitución</td>
      <td>769725</td>
      <td>POINT (-99.13332 19.43328)</td>
    </tr>
  </tbody>
</table>
</div>



```python
ruta_optima = ruteo.CalcularRuta(linea_inicial = linea_inicial, linea_final = linea_final, tipo_vehiculo = 1, ruta = 'optima')

# Las siguientes combinaciones serían equivalentes:
#ruteo.CalcularRuta(linea_inicial = linea_inicial, destino_final = destino_final, tipo_vehiculo = 1, ruta = 'optima')
#ruteo.CalcularRuta(destino_inicial = destino_inicial, linea_final = linea_final, tipo_vehiculo = 1, ruta = 'optima')
#ruteo.CalcularRuta(destino_inicial = destino_inicial, destino_final = destino_final, tipo_vehiculo = 1, ruta = 'optima')

display(ruta_optima)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>costo_caseta</th>
      <th>tiempo_min</th>
      <th>advertencia</th>
      <th>long_km</th>
      <th>peaje</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>3.79</td>
      <td></td>
      <td>2.53</td>
      <td>False</td>
      <td>MULTILINESTRING ((-99.13344 19.43195, -99.1326...</td>
    </tr>
  </tbody>
</table>
</div>



```python
detalle_ruta = ruteo.DetalleRuta(linea_inicial = linea_inicial, linea_final = linea_final, tipo_vehiculo = 1, ruta = 'optima')
display(detalle_ruta)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>eje_excedente</th>
      <th>costo_caseta</th>
      <th>tiempo_min</th>
      <th>long_m</th>
      <th>punto_caseta</th>
      <th>direccion</th>
      <th>giro</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>None</td>
      <td>Inicia recorrido en Eje vial Central Lázaro Cá...</td>
      <td>0</td>
      <td>POINT (-99.14085 19.43421)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.911682</td>
      <td>607.788044</td>
      <td>None</td>
      <td>Continúe por Eje vial Central Lázaro Cárdenas ...</td>
      <td>0</td>
      <td>POINT (-99.14085 19.43421)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.402828</td>
      <td>268.551789</td>
      <td>None</td>
      <td>Gire a la derecha en Calle República de Perú</td>
      <td>2</td>
      <td>POINT (-99.14002 19.43966)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.639794</td>
      <td>426.529251</td>
      <td>None</td>
      <td>Gire a la derecha en Calle Ignacio Allende</td>
      <td>2</td>
      <td>POINT (-99.13746 19.43956)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.215491</td>
      <td>143.660612</td>
      <td>None</td>
      <td>Continúe por Calle Bolívar</td>
      <td>0</td>
      <td>POINT (-99.13802 19.43573)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.662375</td>
      <td>441.583560</td>
      <td>None</td>
      <td>Gire a la izquierda en Calle 5 de Mayo</td>
      <td>1</td>
      <td>POINT (-99.13822 19.43444)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.136318</td>
      <td>90.878944</td>
      <td>None</td>
      <td>Gire a la derecha en Calle Monte de Piedad</td>
      <td>2</td>
      <td>POINT (-99.13404 19.43397)</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.826011</td>
      <td>550.674086</td>
      <td>None</td>
      <td>Continúe por Calle Plaza de la Constitución</td>
      <td>1</td>
      <td>POINT (-99.13411 19.43315)</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>None</td>
      <td>¡Haz llegado a tu destino!</td>
      <td>0</td>
      <td>POINT (-99.13411 19.43315)</td>
    </tr>
  </tbody>
</table>
</div>



```python
combustibles = ruteo.Combustibles()
display(combustibles)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tipo</th>
      <th>tipo_costo</th>
      <th>costo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Magna</td>
      <td>Magna $19.80/l</td>
      <td>19.80</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Premium</td>
      <td>Premium $21.09/l</td>
      <td>21.09</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Diésel</td>
      <td>Diésel $21.26/l</td>
      <td>21.26</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Gas</td>
      <td>Gas $10.01/l</td>
      <td>10.01</td>
    </tr>
  </tbody>
</table>
</div>


## Casos de uso

### Indicadores y MarcoGeoestadistico


```python
from INEGIpy import Indicadores, MarcoGeoestadistico
```


```python
token = 'TuToken'
inegi = Indicadores(token)
marco = MarcoGeoestadistico()
```


```python
indicadores = [str(i) for i in range(472080,472112)] # indicadores del PIB real por entidad federativa
entidades = marco.Entidades()
nombres = entidades.nom_agee.tolist() # nombres de las entidades
pib_edos = inegi.obtener_df(indicadores = indicadores, nombres = nombres, inicio = '2019')
display(pib_edos)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Aguascalientes</th>
      <th>Baja California</th>
      <th>Baja California Sur</th>
      <th>Campeche</th>
      <th>Coahuila de Zaragoza</th>
      <th>Colima</th>
      <th>Chiapas</th>
      <th>Chihuahua</th>
      <th>Ciudad de México</th>
      <th>Durango</th>
      <th>...</th>
      <th>Quintana Roo</th>
      <th>San Luis Potosí</th>
      <th>Sinaloa</th>
      <th>Sonora</th>
      <th>Tabasco</th>
      <th>Tamaulipas</th>
      <th>Tlaxcala</th>
      <th>Veracruz de Ignacio de la Llave</th>
      <th>Yucatán</th>
      <th>Zacatecas</th>
    </tr>
    <tr>
      <th>fechas</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-01-01</th>
      <td>222456.200</td>
      <td>575342.251</td>
      <td>158953.105</td>
      <td>517311.384</td>
      <td>603930.571</td>
      <td>109109.572</td>
      <td>261697.349</td>
      <td>572966.871</td>
      <td>3133078.905</td>
      <td>204061.056</td>
      <td>...</td>
      <td>290611.760</td>
      <td>368672.808</td>
      <td>398162.683</td>
      <td>580759.016</td>
      <td>448890.121</td>
      <td>517422.426</td>
      <td>103566.865</td>
      <td>801624.782</td>
      <td>263372.187</td>
      <td>151905.742</td>
    </tr>
    <tr>
      <th>2020-01-01</th>
      <td>204142.637</td>
      <td>553945.092</td>
      <td>121577.942</td>
      <td>482973.093</td>
      <td>535373.609</td>
      <td>101068.064</td>
      <td>251650.751</td>
      <td>539293.544</td>
      <td>2848733.731</td>
      <td>190239.040</td>
      <td>...</td>
      <td>220550.379</td>
      <td>340576.121</td>
      <td>370202.628</td>
      <td>549564.663</td>
      <td>464512.613</td>
      <td>473593.124</td>
      <td>91004.963</td>
      <td>737040.168</td>
      <td>243120.969</td>
      <td>145571.953</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 32 columns</p>
</div>



```python
# sacamos la tasa de crecimiento
cambios_pcts = pib_edos.pct_change()
display(cambios_pcts)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Aguascalientes</th>
      <th>Baja California</th>
      <th>Baja California Sur</th>
      <th>Campeche</th>
      <th>Coahuila de Zaragoza</th>
      <th>Colima</th>
      <th>Chiapas</th>
      <th>Chihuahua</th>
      <th>Ciudad de México</th>
      <th>Durango</th>
      <th>...</th>
      <th>Quintana Roo</th>
      <th>San Luis Potosí</th>
      <th>Sinaloa</th>
      <th>Sonora</th>
      <th>Tabasco</th>
      <th>Tamaulipas</th>
      <th>Tlaxcala</th>
      <th>Veracruz de Ignacio de la Llave</th>
      <th>Yucatán</th>
      <th>Zacatecas</th>
    </tr>
    <tr>
      <th>fechas</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-01-01</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-01-01</th>
      <td>-0.082324</td>
      <td>-0.03719</td>
      <td>-0.235133</td>
      <td>-0.066378</td>
      <td>-0.113518</td>
      <td>-0.073701</td>
      <td>-0.03839</td>
      <td>-0.05877</td>
      <td>-0.090756</td>
      <td>-0.067735</td>
      <td>...</td>
      <td>-0.241082</td>
      <td>-0.07621</td>
      <td>-0.070223</td>
      <td>-0.053713</td>
      <td>0.034802</td>
      <td>-0.084707</td>
      <td>-0.121293</td>
      <td>-0.080567</td>
      <td>-0.076892</td>
      <td>-0.041696</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 32 columns</p>
</div>



```python
cambios_pcts = cambios_pcts.stack().reset_index()
cambios_pcts.columns = ['fechas','nom_agee','cambio_pct_pib_real']
display(cambios_pcts.head())
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fechas</th>
      <th>nom_agee</th>
      <th>cambio_pct_pib_real</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2020-01-01</td>
      <td>Aguascalientes</td>
      <td>-0.082324</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020-01-01</td>
      <td>Baja California</td>
      <td>-0.037190</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2020-01-01</td>
      <td>Baja California Sur</td>
      <td>-0.235133</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2020-01-01</td>
      <td>Campeche</td>
      <td>-0.066378</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2020-01-01</td>
      <td>Coahuila de Zaragoza</td>
      <td>-0.113518</td>
    </tr>
  </tbody>
</table>
</div>



```python
entidades = entidades.merge(cambios_pcts, how = 'left')
entidades.cambio_pct_pib_real = entidades.cambio_pct_pib_real*100
display(entidades.head())
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>geometry</th>
      <th>cvegeo</th>
      <th>cve_agee</th>
      <th>nom_agee</th>
      <th>nom_abrev</th>
      <th>pob</th>
      <th>pob_fem</th>
      <th>pob_mas</th>
      <th>viv</th>
      <th>fechas</th>
      <th>cambio_pct_pib_real</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>POLYGON ((-102.28787 22.41649, -102.28753 22.4...</td>
      <td>01</td>
      <td>01</td>
      <td>Aguascalientes</td>
      <td>Ags.</td>
      <td>1425607</td>
      <td>728924</td>
      <td>696683</td>
      <td>386671</td>
      <td>2020-01-01</td>
      <td>-8.232435</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MULTIPOLYGON (((-117.10047 32.53656, -117.0992...</td>
      <td>02</td>
      <td>02</td>
      <td>Baja California</td>
      <td>BC</td>
      <td>3769020</td>
      <td>1868431</td>
      <td>1900589</td>
      <td>1149563</td>
      <td>2020-01-01</td>
      <td>-3.719031</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MULTIPOLYGON (((-112.75825 27.97538, -112.7574...</td>
      <td>03</td>
      <td>03</td>
      <td>Baja California Sur</td>
      <td>BCS</td>
      <td>798447</td>
      <td>392568</td>
      <td>405879</td>
      <td>240660</td>
      <td>2020-01-01</td>
      <td>-23.513327</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MULTIPOLYGON (((-90.37936 20.84833, -90.38182 ...</td>
      <td>04</td>
      <td>04</td>
      <td>Campeche</td>
      <td>Camp.</td>
      <td>928363</td>
      <td>471424</td>
      <td>456939</td>
      <td>260824</td>
      <td>2020-01-01</td>
      <td>-6.637838</td>
    </tr>
    <tr>
      <th>4</th>
      <td>POLYGON ((-102.31079 29.87695, -102.31050 29.8...</td>
      <td>05</td>
      <td>05</td>
      <td>Coahuila de Zaragoza</td>
      <td>Coah.</td>
      <td>3146771</td>
      <td>1583102</td>
      <td>1563669</td>
      <td>901249</td>
      <td>2020-01-01</td>
      <td>-11.351795</td>
    </tr>
  </tbody>
</table>
</div>



```python
ax = entidades.plot(column = 'cambio_pct_pib_real', 
                    cmap = 'hot',
                    legend = True, 
                    legend_kwds={'label':'Cambio (%)', 'orientation':"horizontal"},
                    figsize = (8,8),
                    edgecolor = 'black',
                    linewidth = 0.5)
ax.set_title('Cambio Porcentual del PIB real por Entidad Federeativa \n 2019 - 2020')
ax.set_axis_off()
```


    
![png](./README_PNGs/output_44_0.png)
    


### DENUE, Ruteo y MarcoGeoestadistico

#### Negocios a 5km de una coordenada

##### Distancia radial


```python
from INEGIpy import DENUE, MarcoGeoestadistico, Ruteo
import geopandas as gpd
import pandas as pd
```


```python
token = 'TuToken'
denue = DENUE(token)
marco = MarcoGeoestadistico()
token_ruteo = 'TuOtroToken'
ruteo = Ruteo(token_ruteo)
```


```python
# construimos una capa para la zona a buscar
zocalo = ruteo.BuscarDestino(busqueda = 'zócalo, ciudad de m', cantidad = 1)
display(zocalo)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ent_abr</th>
      <th>id_dest</th>
      <th>nombre</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CDMX</td>
      <td>4437</td>
      <td>Plaza de la Constitución, Cuauhtémoc</td>
      <td>POINT (-99.13320 19.43263)</td>
    </tr>
  </tbody>
</table>
</div>



```python
# utilizamos el DENUE para obtener una capa con los establecimientos en un radio de 5 km 
# inicié queriendo ver todos los establecimientos pero son demasiados para hacer buenos visuales así que acoté a solo los Oxxos
lat, lng = zocalo.geometry.iloc[0].y, zocalo.geometry.iloc[0].x
estabs = denue.Buscar('oxxo',lat,lng,5000)

ax = zocalo.plot(color='yellow', zorder=2, markersize=50)
estabs.plot(ax=ax, alpha=0.3, color='red', zorder=1)
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_51_1.png)
    



```python
# utilizamos el marco geostadistico para obtener la capa del area geografica sobre la que plotear
# Si no conoces la clave de alguna entidad, municipio o localidad la puedes buscar por nombre en el marco geoestadístico

# regresa todas las manzanas en CDMX
muns = marco.Municipios(entidades='09')

ax = muns.plot(alpha = 0.5)
zocalo.plot(ax=ax, color='yellow', zorder=2, markersize=20)
estabs.plot(ax=ax, color='red', alpha=0.4)
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_52_1.png)
    



```python
# reducimos a solo los municipios en el area con un join espacial

muns = gpd.sjoin(muns, estabs).dissolve('cve_agem') 

ax = muns.plot(alpha = 0.5)
zocalo.plot(ax=ax, color='yellow', zorder=2, markersize=20)
estabs.plot(ax=ax, color='red', alpha=0.4)
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_53_1.png)
    



```python
# ya podemos hacer operaciones y obtener datos como las distancias al punto definido:
# para poder tener las distancias en metros necesitamos cambiar los crs de los geodataframes
zocalo = zocalo.to_crs('EPSG:6372')
estabs = estabs.to_crs('EPSG:6372')
muns = muns.to_crs('EPSG:6372')

estabs['distancia_radial'] = estabs.geometry.distance(zocalo.geometry.iloc[0])
```


```python
# podemos ver que la distancia mínima son 300 metros, la máxima es cercana a los 5 km y la media es de 3.1 km

estabs.distancia_radial.min(), estabs.distancia_radial.max(), estabs.distancia_radial.mean()
```




    (217.4387129171983, 4983.678746895861, 3130.050858409257)




```python
ax = muns.plot(alpha = 0.5, figsize=(8,8))
zocalo.plot(ax=ax, color='yellow', zorder=2, markersize=20)
estabs.plot(ax=ax, alpha=0.4, column='distancia_radial', legend = True, legend_kwds={'label':'Distancia (m)','orientation':"horizontal"})
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_56_1.png)
    



```python
# podemos mejorar el mapa si usamos un nivel de agregación menor

agebs = marco.AGEBs(entidades = '09', municipios = muns.index.tolist())
agebs = agebs.to_crs('EPSG:6372')
agebs = agebs[agebs.geometry.intersects(zocalo.geometry.iloc[0].buffer(5000))]

ax = agebs.plot(alpha = 0.4, figsize=(8,8), zorder=1)
zocalo.plot(ax=ax, color='yellow', zorder=3, markersize=30)
estabs.plot(ax=ax, alpha=0.6, column='distancia_radial',
            legend = True, legend_kwds={'label':'Distancia (m)','orientation':"horizontal"}, zorder=2)
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_57_1.png)
    



```python
# para mejorar el mapa también podemos plotear las vialidades

vialidades = marco.Vialidades(entidades='09', municipios=muns.index.tolist())
vialidades = vialidades.to_crs('EPSG:6372')
agebs_dis = agebs.dissolve(by='cve_ent')
vialidades = vialidades[vialidades.geometry.intersects(agebs_dis.geometry.iloc[0])]

ax = agebs_dis.plot(alpha = 0.5, figsize=(8,8), zorder=1)
vialidades.plot(ax=ax, color='white', alpha=0.5, zorder=2)
zocalo.plot(ax=ax, color='yellow', zorder=3, markersize=60)
estabs.plot(ax=ax, alpha=0.9, column='distancia_radial', cmap='Reds',
            legend = True, legend_kwds={'label':'Distancia (m)','orientation':"horizontal"},zorder=4)
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_58_1.png)
    


##### Distancia en ruta


```python
# primero obtenemos la calle más cerca del punto inicial definido
# Para estopodemos usar la función BuscarLinea del módulo de ruteo

linea_i =  ruteo.BuscarLinea(lat, lng)
display(linea_i)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>source</th>
      <th>id_routing_net</th>
      <th>nombre</th>
      <th>target</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>769724</td>
      <td>1475230</td>
      <td>Calle Plaza de la Constitución</td>
      <td>769725</td>
      <td>POINT (-99.13332 19.43328)</td>
    </tr>
  </tbody>
</table>
</div>



```python
# Para calcular una ruta se requiere la utilizar la función BuscarLinea (o BuscarDestino dependiendo de lo que se busca) con el fin de obtener la línea final de la ruta
# Como tenemos varios puntos finales más bien sería una lista de líneas

# Noté que en ocasiones el Sistema de Ruteo no encuentra información para una coordenada si la escala no está correcta por lo que aumenté el valor default de 
# la escala a 1,000,000 lo cual resolvió el problema para las coordenadas resultantes del DENUE sin embargo es importante tenerlo en cuenta para otras bases. 

lineas_f = [ruteo.BuscarLinea(estabs.Latitud.iloc[i], estabs.Longitud.iloc[i]) for i in range(estabs.shape[0])]
len(lineas_f)
```




    385




```python
# una vez con las líneas resultantes de cada oxxo usamos la función CalcularRuta para obtener la rúta óptima desdse el punto inicial en el zócalo
# solo debemos darle como argumentos los DataFrames resultantes

# El INEGI no me ha respondido sobre límites o preferencias de uso pero noté que las primeras 280 rutas las calcula más rápido y a partir de ahí se alenta
# en lo que me responen estoy pausando cada 100 requests por si es una cuestión de límites aunque también puede ser que esas rutas tomen más tiempo por ser más largas
# el tiempo en el que corre la celda se acortó con el time.sleep(30) así que sí puede ser una cuesstión de límites
import time

rutas = []
for j in range(len(lineas_f)):
    r = ruteo.CalcularRuta(linea_i, lineas_f[j])
    rutas.append(r)
    if j%100 == 0: time.sleep(30)
    
len(rutas)
```




    385




```python
rutas = gpd.GeoDataFrame(pd.concat(rutas,axis=0).reset_index(drop=True))
display(rutas.head())
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>costo_caseta</th>
      <th>tiempo_min</th>
      <th>advertencia</th>
      <th>long_km</th>
      <th>peaje</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>0.50</td>
      <td></td>
      <td>0.34</td>
      <td>False</td>
      <td>MULTILINESTRING ((-99.13322 19.43332, -99.1333...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.0</td>
      <td>1.31</td>
      <td></td>
      <td>0.90</td>
      <td>False</td>
      <td>MULTILINESTRING ((-99.13344 19.43195, -99.1326...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.0</td>
      <td>1.26</td>
      <td></td>
      <td>1.06</td>
      <td>False</td>
      <td>MULTILINESTRING ((-99.13236 19.43078, -99.1330...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.0</td>
      <td>0.50</td>
      <td></td>
      <td>0.34</td>
      <td>False</td>
      <td>MULTILINESTRING ((-99.13322 19.43332, -99.1333...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.0</td>
      <td>1.90</td>
      <td></td>
      <td>1.31</td>
      <td>False</td>
      <td>MULTILINESTRING ((-99.13236 19.43078, -99.1314...</td>
    </tr>
  </tbody>
</table>
</div>



```python
# con las rutas ya podemos tener la distancia y clasificar así los puntos
# la columna long_km y el length que calcula Shapely difiere por metros, ambos son de fácil acceso así que cualquiera se puede usar

estabs['distancia_ruta'] = rutas.long_km
```


```python
# Finalmente podemos visualizar los oxxos que se encuentran a 5 km en ruta 

ax = agebs_dis.plot(alpha = 0.5, figsize=(8,8), zorder=1)
vialidades.plot(ax=ax, color='white', alpha=0.3, zorder=2)
zocalo.plot(ax=ax, color='yellow', zorder=3, markersize=60)
estabs[estabs.distancia_ruta <= 5].plot(ax=ax, alpha=0.9, column='distancia_ruta', cmap='Reds',
            legend = True, legend_kwds={'label':'Distancia (Km)','orientation':"horizontal"},zorder=4)
```




    <AxesSubplot:>




    
![png](./README_PNGs/output_65_1.png)
    

