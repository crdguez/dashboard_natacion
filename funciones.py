import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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
