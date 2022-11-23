import streamlit as st
# import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from funciones import *
import altair as alt

st.set_page_config(page_title='Resultados Natación', page_icon=':shark:', layout="wide", initial_sidebar_state="expanded", menu_items=None)

# Importamos datos

# df=pd.read_csv('https://gitlab.com/crdguez/resultados_natacion/-/raw/main/prueba.csv')
df=pd.read_csv('https://raw.githubusercontent.com/crdguez/dashboard_natacion/main/importar_datos/base_datos.csv')

df.Puesto = df.Puesto.astype('int')

st.title(':shark: :swimmer: Resultados de natación :swimmer: :shark:')
st.write(':arrow_left: Filtra los datos que quieras con en el menú de la izquierda')


slice = df[['Nombre','Anyo_nac','M_F','Club','Prueba','Tiempo','Time_stamp','Puesto','Pts','Fecha','Competicion','Lugar','Piscina','Temporada']]



# st.sidebar.markdown('---')
st.sidebar.title(':swimmer: :shark: :swimmer: :shark: :swimmer: :shark: :swimmer: :shark:  ')
# st.sidebar.markdown('---')

# st.sidebar.markdown('---')
st.sidebar.header(':star2: :star2: Filtro :star2: :star2:')


# Filtro Temporada
lt=list(slice.Temporada.sort_values().unique())
lt.insert(0,'Todas')
tm = st.sidebar.selectbox('Temporada:',lt,2)
slice = slice if tm == 'Todas' else slice[slice.Temporada == tm]


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
    st.info(':eye: **Recuerda** que la información que ves se corresponde con el filtro de datos aplicado. Si quieres modifícalo con el menú de la izquierda')
    st.image('portada.jpg', caption='Photo by Brian Matangelo on "https://unsplash.com/photos/rAn25CLlyLE"')
    # st.subheader('Filtro activo: ')
    # # filtro = '**Temporada:** '+str(tm)+' - **Competición:** '+str(cp) +' - **Club:** '+str(cl) \
    # #         +' - **Nadador:** ' + str(nad) + ' - **Año:** '+str(an) +' - **Categoría:** '+str(gn) \
    # #         +' - **Prueba:** '+str(pr)
    #
    # dic_filtro = {'Temporada':str(tm),'Competición':str(cp),'Club':str(cl),
    #         'Nadador':str(nad), 'Año':str(an), 'Categoría': str(gn), 'Prueba':str(pr)}
    # st.write(dic_filtro)

with col2:
    st.subheader('Filtro activo: ')
    # filtro = '**Temporada:** '+str(tm)+' - **Competición:** '+str(cp) +' - **Club:** '+str(cl) \
    #         +' - **Nadador:** ' + str(nad) + ' - **Año:** '+str(an) +' - **Categoría:** '+str(gn) \
    #         +' - **Prueba:** '+str(pr)

    dic_filtro = {'Temporada':str(tm),'Competición':str(cp),'Club':str(cl),
            'Nadador':str(nad), 'Año':str(an), 'Categoría': str(gn), 'Prueba':str(pr)}
    st.write(dic_filtro)

    # @st.cache
    csv = convert_df(slice)
    st.download_button(
         label="Descargar datos filtrados en CSV",
         data=csv,
         file_name='datos.csv',
         mime='text/csv',
     )


    st.subheader('Contenidos visibles:')
    opciones = st.multiselect(
        'Añade o elimina:',
        ['Resumen', 'Evolución','Resultados'],
        ['Resumen', 'Evolución','Resultados'])

    # st.write('You selected:', opciones)
    # st.write(':new:')



# Resumen

if 'Resumen' in opciones :

    st.subheader('Resumen: ')

    # Escribimos el número de nadadores
    # st.write('Número de **Nadadores**:')
    # st.write(slice.pivot_table(values = 'Nombre', columns='M_F', index=['Club','Anyo_nac'], aggfunc=lambda x: len(x.unique())).unstack().fillna(0).astype(int))
    slice['Categoria']=slice.Anyo_nac.astype('str')+slice.M_F
    # st.write(slice.pivot_table(values = 'Nombre', columns=['Categoria'], index=['Club'], aggfunc=lambda x: len(x.unique())).fillna(0).astype(int))

    # Diagrama de barras con el número de nadadores
    # st.bar_chart(slice[['Nombre','Club']].groupby(['Club']).Nombre.nunique())


    # Diagramas resumen
    st.write('**Gráficas:**')
    st.pyplot(graficas_resumen(slice))

    st.write(':arrow_down: Pincha si quieres ver:')
    with st.expander("Tabla con el número de nadadores"):
        st.table(numero_de_nadadores(slice))



    # Top Marcas:
    st.write('**Mejores Marcas según FINA**')
    num=st.slider('Elige el número:',5,20,step=5)
    st.write('**Top {}** según **puntuación FINA**'.format(num))
    st.table(slice.sort_values(['Pts'],ascending=False)[['Pts','Nombre','Prueba','Tiempo','Anyo_nac','M_F','Club']].head(num).assign(hack='').set_index('hack'))


    st.write(':arrow_down: Pincha si quieres ver:')
    with st.expander("Mejores marcas personales"):
        st.info("""**Instrucciones:**
        \n - Puedes ver la tabla a pantalla completa si seleccionas las doble flecha de la esquina superior derecha.
        \n - Puedes ordenar por prueba pinchando en la prueba correspondiente.""")
        clubes = st.multiselect(
             'Clubes:',
             slice.Club.unique(),
             slice.Club.unique()
             )
        st.dataframe(mejores_marcas(slice[slice.Club.isin(clubes)]).style.format(lambda s: s[-9:-1],na_rep='-').highlight_null(null_color='grey'))


# Evoluación de Puestos:

if 'Evolución' in opciones :

    st.subheader('Evolución: ')
    num2=st.slider('Elige el puesto:',5,50,step=5, value=10)

    st.write('**Evolución de los {} mejores puestos:**'.format(num2))

    for i in slice[['Anyo_nac','M_F']].drop_duplicates().iterrows():
        anyo, genero = i[1]
        st.write('Puestos')
        st.pyplot(evolucion_puestos(slice, num2, anyo, genero))
        st.write('Marcas Personales')
        # st.dataframe(mejores_marcas(slice, anyo, genero).style.highlight_null())

        st.table(mejores_marcas(slice, anyo, genero).style.format(lambda s: s[-9:-1],na_rep='-').set_table_styles([{'selector': 'td','props': [('border', '1px solid black'),('text-align', 'center')]}, \
                           {'selector': 'tr','props': [('border', '1px solid black')]}, \
                           {'selector': 'th','props': [('border', '1px solid red'),('font-size','12px')]}, \
                           {'selector': 'td','props': [('border', '4px solid black'),('text-align', 'center'),('font-size','14px')]}, \
                          ] \
                         ) \
                         )
        st.write(':arrow_down: Pincha si quieres ver:')
        with st.expander('Tabla dinámica con las Marcas Personales ') :


            st.dataframe(mejores_marcas(slice, anyo, genero).style.format(lambda s: s[-9:-1],na_rep='-').highlight_null(null_color='grey'))




        # st.write(mejores_marcas(slice, anyo, genero).style.format(lambda s: s[-9:-1],na_rep='-').to_html())


# Resultados

if 'Resultados' in opciones :

    st.header('**Resultados:**')

    st.write(':arrow_down: Pincha si quieres ver:')
    with st.expander('Resultados detallados') :
        # Escribimos los datos filtrados
        st.dataframe(slice.assign(hack='').set_index('hack'), height=500)
        #st.dataframe(slice.assign(hack='').set_index('hack'), height=500)


# Creditos
# st.sidebar.header('Autor')
st.header("Créditos")
st.info('* Aplicación desarrollada por **[Carlos Rodríguez](https://github.com/crdguez)** \
    \n * El [código fuente](https://github.com/crdguez/dashboard_natacion) se publica con **licencia libre** \
    \n * Cómo se mantienen los [datos](https://crdguez.gitlab.io/post_sastre/dashboard_natacion/)')
