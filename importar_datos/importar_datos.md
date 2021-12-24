Importamos las librerías:


```python
#Importamos librerias

import camelot
import pandas as pd
import datetime
from funciones import tabla_a_datos, campos_calculados
import glob
```

Con *camelot* leemos el pdf que le digamos y extraemos las tablas en bruto:


```python
## Datos a importar

file = 'NATACION_BENJAMIN_1_RESULTADOS_2122.pdf'
# tablas = camelot.read_pdf(file, pages='all', flavor='stream', split_text=' ')
tablas = camelot.read_pdf(file, pages='all', flavor='stream', split_text='\n')
tablas.n
```




    15



Modificamos las tablas para que tengan el formato que nos interese:


```python
# Liga Benjamin

competicion = 'Benjamín, jornada 1'
lugar = 'C.N. Helios'
fecha = datetime.datetime(2021,11,20)


# Modifico tabla 4, que hay un error en ella
df4=tablas[4].df.copy()
df4[1][3]=df4[1][3]+'a'
df4[2][3]=df4[2][3].split('\n')[1]


lista_df=[
tabla_a_datos(tablas[0].df, fila_datos = 4, fecha=fecha, prueba='50m Espalda', m_f='M', tipo=1, competicion=competicion, lugar= lugar),
tabla_a_datos(tablas[1].df, fila_datos = 1, fecha=fecha, prueba='100m Espalda', m_f='M', tipo=2, competicion=competicion, lugar= lugar),
tabla_a_datos(tablas[2].df, fila_datos = 2, fecha=fecha, prueba='100m Espalda', m_f='M', tipo=2, competicion=competicion, lugar= lugar),
tabla_a_datos(tablas[3].df, fila_datos = 3, fecha=fecha, prueba='50m Espalda', m_f='F', tipo=1, competicion=competicion, lugar= lugar),
tabla_a_datos(df4, fila_datos = 3, fecha=fecha, prueba='50m Espalda', m_f='F', tipo=1, competicion=competicion, lugar= lugar),
# tabla_a_datos(tablas[5].df, fila_datos = 4, fecha=fecha, prueba='100m Espalda', m_f='F', tipo=3),
# tabla_a_datos(tablas[6].df, fila_datos = 2, fecha=fecha, prueba='100m Espalda', m_f='F', tipo=3),
tabla_a_datos(tablas[5].df, fila_datos = 4, fecha=fecha, prueba='100m Espalda', m_f='F', tipo=1, competicion=competicion, lugar= lugar),
tabla_a_datos(tablas[6].df, fila_datos = 2, fecha=fecha, prueba='100m Espalda', m_f='F', tipo=1, competicion=competicion, lugar= lugar),
tabla_a_datos(tablas[7].df, fila_datos = 4, fecha=fecha, prueba='50m Libre', m_f='M', tipo=1, competicion=competicion, lugar= lugar),
tabla_a_datos(tablas[8].df, fila_datos = 4, fecha=fecha, prueba='100m Libre', m_f='M', tipo=2, competicion=competicion, lugar= lugar),
# tabla_a_datos(tablas[10].df, fila_datos = 2, fecha=fecha, prueba='100m Libre', m_f='M', tipo=3),
tabla_a_datos(tablas[10].df, fila_datos = 2, fecha=fecha, prueba='100m Libre', m_f='M', tipo=1, competicion=competicion, lugar= lugar),
tabla_a_datos(tablas[11].df[range(6)], fila_datos = 4, fecha=fecha, prueba='50m Libre', m_f='F', tipo=1, competicion=competicion, lugar= lugar),
# tabla_a_datos(tablas[12].df, fila_datos = 4, fecha=fecha, prueba='100m Libre', m_f='F', tipo=3),
tabla_a_datos(tablas[12].df, fila_datos = 4, fecha=fecha, prueba='100m Libre', m_f='F', tipo=1, competicion=competicion, lugar= lugar),
tabla_a_datos(pd.DataFrame({0:['24.'],1:['ROMERO LAFUENTE, Paula'],2:[12],3:['P. San Agustin']
                  , 4:['2:14.80'], 5:['51']}), fila_datos = 0, fecha=fecha, prueba='100m Libre', m_f='F', tipo=1, competicion=competicion, lugar= lugar),

]

# for d in lista_df :
#     display(d)
    
    
campos_calculados(pd.concat(lista_df)).to_csv('competicion_'+competicion+'.csv', index=False)
```

Hacemos un resumen de los datos contando el número de nadadores por club:


```python
# Resumen de datos

df=pd.read_csv('competicion_'+competicion+'.csv')

#df.pivot_table(df, values = 'Nombre',index='M_F', columns=['Club','Anyo_nac'], aggfunc=lambda x: len(x.unique()))
df.pivot_table(values = 'Nombre', columns='M_F', index=['Club','Anyo_nac'], aggfunc=lambda x: len(x.unique())).unstack().fillna(0).astype(int)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>M_F</th>
      <th colspan="4" halign="left">F</th>
      <th colspan="4" halign="left">M</th>
    </tr>
    <tr>
      <th>Anyo_nac</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
      <th>10</th>
      <th>11</th>
      <th>12</th>
      <th>13</th>
    </tr>
    <tr>
      <th>Club</th>
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
      <th>C.N. Helios</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>4</td>
      <td>6</td>
      <td>7</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>C.N. Iz Cuarte</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>C.N. Teruel</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>E.M. El Olivar</th>
      <td>0</td>
      <td>0</td>
      <td>11</td>
      <td>6</td>
      <td>8</td>
      <td>7</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>H2ogo C.N.</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>P. San Agustin</th>
      <td>0</td>
      <td>0</td>
      <td>8</td>
      <td>2</td>
      <td>4</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Stadium Casablanca</th>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Stadium Venecia</th>
      <td>0</td>
      <td>0</td>
      <td>4</td>
      <td>6</td>
      <td>2</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



Por último, añadimos todas las competiciones al archivo *base_datos.csv*:


```python
# Actualizamos la base de datos

import glob

# Buscamos todos los ficheros csv correspondientes a competiciones los concatenamos y los grabamos en base de datos

lista_competiciones = glob.glob('competicion*.csv')
df=pd.concat([pd.read_csv(comp) for comp in lista_competiciones])
df.to_csv('base_datos.csv', index=False)
lista_competiciones
```




    ['competicion_Benjamín, jornada 1.csv']


