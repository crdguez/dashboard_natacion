# dashboard_natacion

Aplicación hecha en streamlit para visualizar estadísticas de natacion

Los ficheros que lee la aplicación se encuentran en mi repositorio privado [https://gitlab.com/crdguez/resultados_natacion](https://gitlab.com/crdguez/resultados_natacion)

### Crear la imagen a partir del Dockefile

Si no tenemos la imagen en local:

```
sudo docker build -t crdguez/mi_streamlit:v2 .
```



### Lanzando un contendor docker con Streamlit y la aplicacion *main.py*

He creado un fichero *main.py* con el código de *streamlit*. Si no tengo el docker creado, lo creo con el siguiente comando:

```
docker run -it -p 8502:8502 --name natacion -v $PWD:/app crdguez/mi_streamlit main.py

```

Una vez creado podemos lanzarlo yendo desde un terminal:


```
docker start natacion

```
Y en el navegador

Network URL: http://172.17.0.2:8501
External URL: http://85.60.254.2:8501
