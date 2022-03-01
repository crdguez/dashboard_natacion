import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def numero_de_nadadores(df) :
    df=df[['Club','M_F','Anyo_nac','Nombre']].groupby(['Club','M_F','Anyo_nac']).agg(lambda x: len(x.unique())).unstack('M_F').unstack().dropna(axis=1,how='all').fillna(0).astype(int).droplevel(0, axis=1)
    df.loc['Total']=df.sum()
    df['Total']=df.sum(axis=1)

    return df.style.set_table_styles([{'selector': 'th',
                                 'props': [('text-align','center'),('border','0.8px solid red'),('font-weight', 'bold')]},
                                {'selector': 'td',
                                 'props': [('text-align','center'),('border','1px solid black')]},
                               ]
                              ) \
                            .set_caption("Distribución del número de nadadores") \
                            .background_gradient(
                                                    cmap='PuBuGn',
    #                                                 cmap='YlOrRd',
                                                    axis=None,
    #                                                 subset = (df.index[-1:], df.columns[:-1])
                                                   )\


def evolucion_puestos(df,num,anyo,genero) :
    # gráfica con la evolución de Puestos

    df['id']=df.Nombre+"-"+df.Club
    df2=df[(df.Anyo_nac==anyo) & (df.M_F==genero)][['Nombre','Club','Prueba','Puesto','id','Fecha']]
    df2['Fecha_Prueba']=df2['Fecha']+' \n '+df2['Prueba']
    # df4=pd.concat([df2[df2.Prueba==j].sort_values(by='Puesto',ascending=True).head(num) for j in df2.Prueba.unique()])
    df4=pd.concat([df2[df2.Fecha_Prueba==j].sort_values(by='Puesto',ascending=True).head(num) for j in df2.Fecha_Prueba.unique()])

    na = df4.id.unique()

    fg, ax = plt.subplots()
    ax.set_ylabel('Puesto')
    ax.set_title('Evolución de puestos - {}{}'.format(genero,str(anyo)))
    plt.yticks(range(1,num+1))


    for n in na:
        df5=df4[df4.id==n].sort_values(by='Fecha',ascending=True)
        # plt.plot(df5.Prueba, df5.Puesto, label=n)
        # plt.scatter(df5.Prueba, df5.Puesto)
        plt.plot(df5.Fecha_Prueba, df5.Puesto, label=n)
        plt.scatter(df5.Fecha_Prueba, df5.Puesto)

    plt.grid(True, axis='y')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.xticks(rotation=0)

    return fg

def mejores_marcas(df,anyo='',genero='') :
    # df2 = df[(df.Anyo_nac==anyo) & (df.M_F==genero)][['Anyo_nac','M_F','Club','Nombre','Prueba','Tiempo']].groupby(['Anyo_nac','M_F','Club','Nombre','Prueba']).Tiempo.min().unstack('Prueba').fillna('')
    # df2 = df[(df.Anyo_nac==anyo) & (df.M_F==genero)][['Anyo_nac','M_F','Club','Nombre','Prueba','Tiempo']].groupby(['Anyo_nac','M_F','Club','Nombre','Prueba']).Tiempo.min().unstack('Prueba')
    df2 = df[(df.Anyo_nac==anyo) & (df.M_F==genero)] if (anyo !='') & (genero!='') else df
    df2 = df2[['Anyo_nac','M_F','Club','Nombre','Prueba','Tiempo','Time_stamp']].groupby(['Anyo_nac','M_F','Club','Nombre','Prueba']).Time_stamp.min().unstack('Prueba')

    return df2

def graficas_resumen(df) :
    gs = gridspec.GridSpec(2, 2)
    # fg, (ax1,ax2) = plt.subplots(1,2)
    fg=plt.figure()

    # Diagrama de caja y bigotes con la distribución de puestos
    ax2=plt.subplot(gs[0,:])
    ax2.boxplot([df[df.Club==c].Puesto for c in df.Club.unique()],labels=df.Club.unique(),vert=False)
    # plt.xticks(rotation=90)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0)
    ax2.set_xlabel('Puesto')
    ax2.set_title('Distribución de puestos por club')

    # Diagram de sectores con Nadadores
    ax1=plt.subplot(gs[1,0])
    df1 = df[['Nombre','Club']].groupby(['Club']).Nombre.nunique().to_frame().reset_index().rename(columns={'Nombre':'Numero'})
    plt.rc('font', size=6)
    ax1.pie(df1.Numero,labels=df1.Club,
        radius=1.2,
        autopct=lambda pct: "{:.1f}%\n({:d})".format(pct, int(np.round(pct/100.*np.sum(df1.Numero)))),
        wedgeprops=dict(width=0.8, edgecolor='w'))
    ax1.set_title('Distribución del número de nadadores')

    # Distribución de nadadores
    ax3=plt.subplot(gs[1,1])
    df2=df.pivot_table(values = 'Nombre', columns=['Categoria'], index=['Club'], aggfunc=lambda x: len(x.unique())).fillna(0).astype(int)
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=90)
    bot=np.zeros(len(df2.index)).astype(int)
    for i, c in enumerate(df2.columns):
        ax3.bar(df2.index, df2[c], label=c, bottom =bot)
        bot=bot+df2[c]
    ax3.legend(loc='best',bbox_to_anchor=(-0.1, 1))
    ax3.set_title('Distribución del número de nadadores')


    # fg.suptitle('Gráficas resumen', fontsize=16)
    fg.tight_layout()


    return fg
