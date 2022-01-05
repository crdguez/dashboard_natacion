import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from funciones import *
import altair as alt

st.set_page_config(page_title='Resultados Natación', page_icon=':shark:', layout="centered", initial_sidebar_state="auto", menu_items=None)

# Importamos datos

# df=pd.read_csv('https://gitlab.com/crdguez/resultados_natacion/-/raw/main/prueba.csv')
df=pd.read_csv('https://raw.githubusercontent.com/crdguez/dashboard_natacion/main/importar_datos/base_datos.csv')

df.Puesto = df.Puesto.astype('int')

st.title(':shark: :swimmer: Resultados de natación :swimmer: :shark:')
st.write(':arrow_left: Filtra los datos que quieras con en el menú de la izquierda')


slice = df[['Nombre','Anyo_nac','M_F','Club','Prueba','Tiempo','Puesto','Pts','Fecha','Competicion','Lugar','Piscina','Temporada']]

# st.sidebar.markdown('---')
st.sidebar.title(':swimmer: :shark: :swimmer: :shark: :swimmer: :shark: :swimmer: :shark:  ')
# st.sidebar.markdown('---')

# st.sidebar.markdown('---')
st.sidebar.header(':star2: :star2: Filtro :star2: :star2:')


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

# Filtro Genero
lg=list(slice.M_F.sort_values().unique())
lg.insert(0,'Todos')
gn = st.sidebar.selectbox('Másculino/Femenino:',lg,0)
slice = slice if gn == 'Todos' else slice[slice.M_F==gn]

# Filtro Prueba
lp=list(slice.Prueba.sort_values().unique())
lp.insert(0,'Todas')
pr = st.sidebar.selectbox('Prueba',lp,0)
slice = slice if pr == 'Todas' else slice[slice.Prueba == pr]

# FIN DE BARRA LATERAL

st.sidebar.title(':swimmer: :shark: :swimmer: :shark: :swimmer: :shark: :swimmer: :shark:')


# Contenidos en la página:

col1, col2 = st.columns(2)

with col1:
    st.subheader('Filtro activo: ')
    # filtro = '**Temporada:** '+str(tm)+' - **Competición:** '+str(cp) +' - **Club:** '+str(cl) \
    #         +' - **Nadador:** ' + str(nad) + ' - **Año:** '+str(an) +' - **Categoría:** '+str(gn) \
    #         +' - **Prueba:** '+str(pr)

    dic_filtro = {'Temporada':str(tm),'Competición':str(cp),'Club':str(cl),
            'Nadador':str(nad), 'Año':str(an), 'Categoría': str(gn), 'Prueba':str(pr)}
    st.write(dic_filtro)

with col2:
    st.subheader('Contenidos visibles:')
    opciones = st.multiselect(
        'Añade o elimina:',
        ['Resumen', 'Evolución','Resultados'],
        ['Resumen', 'Evolución','Resultados'])

    # st.write('You selected:', opciones)



# Resumen

if 'Resumen' in opciones :

    st.subheader('Resumen de los resultados : ')

    # Escribimos el número de nadadores
    st.write('Número de **Nadadores**:')
    st.write(slice.pivot_table(values = 'Nombre', columns='M_F', index=['Club','Anyo_nac'], aggfunc=lambda x: len(x.unique())).unstack().fillna(0).astype(int))

    # Diagrama de barras con el número de nadadores
    # st.bar_chart(slice[['Nombre','Club']].groupby(['Club']).Nombre.nunique())
    st.dataframe(slice[['Nombre','Club']].groupby(['Club']).Nombre.nunique().index)

    # Diagrama de tarta con el número de Nadadores
    source = pd.DataFrame(
        {"category": ["a", "b", "c", "d", "e", "f"], "value": [4, 6, 10, 3, 7, 8]}
    )

    base = alt.Chart(source).encode(
        theta=alt.Theta("value:Q", stack=True), color=alt.Color("category:N", legend=None)
    )

    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=140, size=20).encode(text="category:N")

    st.altair_chart(pie + text, use_container_width=True)

    # Diagrama de caja y bigotes con el resumen de puestos
    st.pyplot(resumen_puestos(slice))

    # Mejores Marcas:
    num=st.slider('Top Marcas',5,20,step=5)
    st.write('**Top {}** según **puntuación FINA**'.format(num))
    st.write(slice.sort_values(['Pts'],ascending=False)[['Pts','Nombre','Prueba','Tiempo','Anyo_nac','M_F','Club']].head(num).assign(hack='').set_index('hack'))

# Evoluación de Puestos:

if 'Evolución' in opciones :

    st.subheader('Evolución: ')

    st.write('**Evolución de Puestos**')

    num2=st.slider('Top Puestos',5,50,step=5)

    for i in slice[['Anyo_nac','M_F']].drop_duplicates().iterrows():
        anyo, genero = i[1]
        st.pyplot(evolucion_puestos(slice, num2, anyo, genero))

# Resultados

if 'Resultados' in opciones :

    st.header('**Resultados:**')

    # Escribimos los datos filtrados
    st.dataframe(slice.assign(hack='').set_index('hack'), height=500)


# Creditos
# st.sidebar.header('Autor')
st.header("Créditos")
st.info('* Aplicación desarrollada por **Carlos Rodríguez** \
    \n * El [código fuente](https://github.com/crdguez/dashboard_natacion) se publica con **licencia libre** \
    \n * Cómo se mantienen los [datos](https://crdguez.gitlab.io/post_sastre/dashboard_natacion/)')
