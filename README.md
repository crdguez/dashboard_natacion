# dashboard_natacion

Aplicación hecha en streamlit para visualizar estadísticas de natacion

Los ficheros que lee la aplicación se encuentran en mi repositorio privado [https://gitlab.com/crdguez/resultados_natacion](https://gitlab.com/crdguez/resultados_natacion)

### Lanzando un contendor docker con Streamlit y la aplicacion *main.py*

He creado un fichero *main.py* con el código de *streamlit*. Si no tengo el docker creado, lo creo con el siguiente comando:

```
docker run -it -p 8502:8502 --name natacion -v $PWD:/app crdguez/streamlit main.py

```

Una vez creado podemos lanzarlo yendo desde un terminal:


```
docker start natacion

```

Y en un navegador: [http://localhost:8501/](http://localhost:8501/) ..
