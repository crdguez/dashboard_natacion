import datetime
import pandas as pd

def separar_columna(df, i, st='\n'):
    return pd.concat([df[list(range(i))],df[i].str.split(st,expand=True), df[list(range(i+1,len(df.columns)))]], axis =1).T.reset_index(drop=True).T[:]

def juntar_columnas(df,i,j) :
#     df[df.columns[list(range(i,j+1))]].apply(lambda x: ''.join(x.dropna().astype(str)),axis=1)
    return pd.concat([df[list(range(i))],df[df.columns[list(range(i,j+1))]].apply(lambda x: ''.join(x.dropna().astype(str)),axis=1),df[list(range(j+1,len(df.columns)))]], axis =1).T.reset_index(drop=True).T[:]



def tabla_a_datos(df, fila_datos = 6, fecha = datetime.datetime(2022,1,20), 
                  prueba = '50m Espalda', piscina = '25m', m_f='M', tipo = 1, 
                 competicion = 'N/A',
                  lugar = 'N/A') :
    
    if tipo == 1 :
#         df2=df[df[0]!='Baja enf.'][df[df[0]!='Baja enf.'][0]!=''].iloc[fila_datos:].reset_index()[range(0,df.columns.size)]
        df2=df[df[4]!=''].iloc[fila_datos:].reset_index()[range(0,df.columns.size)]
        df2.columns=['Puesto','Nombre', 'Anyo_nac', 'Club', 'Tiempo','Pts']

        
    elif tipo == 2 :
#         df2=df[df[0]!='Baja enf.'][df[df[0]!='Baja enf.'][0]!=''].iloc[fila_datos:]
        df2=df[df[3]!=''].iloc[fila_datos:]
        df2[5]=df2[1].apply(lambda x: x.split('\n')[0])
        df2[6]=df2[1].apply(lambda x: x.split('\n')[1])
        # df2.reset_index()[range(0,df.columns.size)]
        df2 = df2.rename(columns={0:'Puesto',1:'nombre_edad',2:'Club',3:'Tiempo',4:'Pts',5:'Nombre',6:'Anyo_nac'})
        df2=df2[['Puesto','Nombre', 'Anyo_nac', 'Club', 'Tiempo','Pts']]
    else :
        df2=df[df[0]!='Baja enf.'][df[df[0]!='Baja enf.'][0]!=''].iloc[fila_datos:]
        df2.columns=['Puesto','Nombre', 'Anyo_nac', 'Club', 'Tiempo','Pts']
        

    df2['Fecha']= fecha
    df2['Prueba']= prueba
    df2['Piscina']= piscina
    df2['M_F']= m_f
    df2['Competicion']=competicion
    df2['Lugar']=lugar
#         df2['Edad'] = (fecha.year + 1 if fecha.month > 8 else fecha.year)-pd.to_numeric(df2['Anyo_nac'])-2000
#         df2['Time_stamp']=df2['Tiempo'].apply(lambda tiempo : pd.to_datetime('00:'+tiempo, format="%M:%S.%f") if len(tiempo.split(':')) == 1 else pd.to_datetime(tiempo, format="%M:%S.%f"))

        
    return df2



def campos_calculados(df) :
    # Añde campos calculados a la tabla
    
    df.Fecha=pd.to_datetime(df.Fecha)
    df.Anyo_nac= pd.to_numeric(df.Anyo_nac) 
    df.Puesto =df.Puesto.str.replace('.','').astype(int)
   
    # Calculamos la edad
    df.loc[df.Fecha.dt.month > 8,'Edad']=df.Fecha.dt.year - df.Anyo_nac - 2000 + 1 
    df.loc[df.Fecha.dt.month <= 8,'Edad']=df.Fecha.dt.year - df.Anyo_nac - 2000

    # Calculamos la temporada
    df.loc[df.Fecha.dt.month > 8,'Temporada']=df.Fecha.dt.year.astype('str')+'-'+(df.Fecha.dt.year +1).astype('str')
    df.loc[df.Fecha.dt.month <= 8,'Temporada']=(df.Fecha.dt.year-1).astype('str')+'-'+df.Fecha.dt.year.astype('str')

    
    # Añadimos una marca temporal
    df['Time_stamp']=df['Tiempo'].apply(lambda tiempo : pd.to_datetime('00:'+tiempo, format="%M:%S.%f") if len(tiempo.split(':')) == 1 else pd.to_datetime(tiempo, format="%M:%S.%f"))
    # Lo anterior lleva un año, si solo quisieramos el tiempo
#     df['Time_stamp']= df['Tiempo'].apply(lambda tiempo : '0:'+tiempo if len(tiempo.split(':')) == 1 else tiempo)
#     df['Time_stamp']=pd.to_datetime(df['Time_stamp'],format='%M:%S.%f').dt.time


    return df

