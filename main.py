import streamlit as st
import pandas as pd
import numpy as np

# Importamos datos

df=pd.read_csv('https://gitlab.com/crdguez/resultados_natacion/-/raw/main/prueba.csv')
df.Puesto = df.Puesto.astype('int')

st.title('Resultados de natación')


# # Bloque de prueba para meter un campo de búsqueda
#
# club = st.selectbox('Club', list(df.Club.unique()))
#
# st.write(df[df.Club==club])
#
# st.write('Filtro de **Resultados**:')
#
# bu = st.text_input('Buscar Nadador: (Los apellidos van en mayúsculas)')
#
# # st.write(bu)
# # bu = st.selectbox('Buscar:',list(datos_act['Alumno'].unique()))
#
# st.write(df[:-2]) if bu == '' else st.write(df[df.Nombre.str.contains(bu)])



slice = df[['Nombre','Anyo_nac','M_F','Club','Prueba','Tiempo','Puesto','Pts','Fecha','Competicion','Lugar','Piscina','Temporada']]


# Filtro Temporada

lt=list(slice.Temporada.sort_values().unique())
lt.insert(0,'Todas')

tm = st.sidebar.selectbox('Temporada:',lt,1)
slice = slice if lt == 'Todas' else slice[slice.Temporada == tm]


# Filtro Competición

lx=list(slice.Competicion.sort_values().unique())
lx.insert(0,'Todas')

cp = st.sidebar.selectbox('Competición:',lx,0)
slice = slice if cp == 'Todas' else slice[slice.Competicion == cp]


# filtro Club

lc=list(df.Club.sort_values().unique())
lc.insert(0,'Todos')

cl =st.sidebar.selectbox('Club',lc,0)
slice = slice if cl == 'Todos' else slice[slice.Club==cl]

# Filtro Nombre

ln=list(slice.Nombre.sort_values().unique())
ln.insert(0,'Todos')

nad = st.sidebar.selectbox('Nadador',ln,0)
slice = slice if nad == 'Todos' else slice[slice.Nombre==nad]

# Filtro Año

la=list(slice.Anyo_nac.sort_values().unique())
la.insert(0,'Todos')

an = st.sidebar.selectbox('Año Nacimiento',la,0)
slice = slice if an == 'Todos' else slice[slice.Anyo_nac==an]


# Filtro Prueba

lp=list(slice.Prueba.sort_values().unique())
lp.insert(0,'Todas')

pr = st.sidebar.selectbox('Prueba',lp,0)
slice = slice if pr == 'Todas' else slice[slice.Prueba == pr]


# Escribimos el número de nadadores

st.header('Temporada: '+str(tm)+'- Competición'+str(cp))

st.write('Número de **Nadadores**:')

st.write(slice.pivot_table(values = 'Nombre', columns='M_F', index=['Club','Anyo_nac'], aggfunc=lambda x: len(x.unique())).unstack().fillna(0).astype(int))

st.header('**Resultados:**')
st.write('Filtra, si quieres, en el menú de la izquierda')



# Escribimos los datos filtrados

st.table(slice)
