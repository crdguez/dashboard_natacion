import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def evolucion_puestos(df,num,anyo,genero) :
    df['id']=df.Nombre+"-"+df.Club
    df2=df[(df.Anyo_nac==anyo) & (df.M_F==genero)][['Nombre','Club','Prueba','Puesto','id']]
    df4=pd.concat([df2[df2.Prueba==j].sort_values(by='Puesto',ascending=True).head(num) for j in df2.Prueba.unique()])

    na = df4.id.unique()

    fg, ax = plt.subplots()
    ax.set_ylabel('Puesto')
    ax.set_title('Evolución de puestos - {}{}'.format(genero,str(anyo)))
    plt.yticks(range(1,num+1))


    for n in na:
        df5=df4[df4.id==n]
        plt.plot(df5.Prueba, df5.Puesto, label=n)
        plt.scatter(df5.Prueba, df5.Puesto)

    plt.grid(True, axis='y')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

    return fg

def resumen_puestos(df) :
    # df2=df[['Club','Prueba','Puesto']]
    df2 = df
    fg, ax = plt.subplots()
    plt.boxplot([df2[df2.Club==c].Puesto for c in df2.Club.unique()],labels=df2.Club.unique())
    plt.xticks(rotation=90)
    ax.set_ylabel('Puesto')
    ax.set_title('Distribución de puestos por club')

    return fg
