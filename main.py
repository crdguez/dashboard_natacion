import streamlit as st
import pandas as pd
import numpy as np

st.title('Resultados de natación')

st.header('Última competición')

st.write('**Nadadores** por club y año:')

df=pd.read_csv('https://gitlab.com/crdguez/resultados_natacion/-/raw/main/prueba.csv')
# st.write(df)

st.write(df.pivot_table(values = 'Nombre', columns='M_F', index=['Club','Anyo_nac'], aggfunc=lambda x: len(x.unique())).unstack().fillna(0).astype(int))

st.write('Filtro de **Resultados**:')

bu = st.text_input('Buscar Nadador: (Los apellidos van en mayúsculas)')

# st.write(bu)
# bu = st.selectbox('Buscar:',list(datos_act['Alumno'].unique()))

st.write(df[:-2]) if bu == '' else st.write(df[df.Nombre.str.contains(bu)])
