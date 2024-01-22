# SENNOVA-11113-2023 Project

This project comprises an application and related resources for analyzing and predicting epidemiological risk data, specifically designed to work with data from Metrosalud, a public health institution in Medellín focused on promoting healthy living and providing comprehensive health services. The project allows for the establishment of a structured database to make predictions about cardiovascular risk, including codes for a complete pipeline and all necessary development for the application.


Este proyecto incluye una aplicación y los recursos relacionados para el análisis y la predicción de datos sobre riesgo epidemiológico. Contiene los códigos necesarios para configurar un pipeline completo, así como todo el código necesario para el desarrollo de la aplicación. Esta herramienta permite establecer una base de datos estructurada y realizar predicciones sobre el riesgo cardiovascular. El proyecto fue desarrollado específicamente para procesar y analizar los datos de Metrosalud, la red de salud más grande de Medellín.

## Estructura de Directorios

### Aplicacion
Esta carpeta contiene todos los archivos necesarios para ejecutar la aplicación web Flask.

- `models`: Carpeta que contiene los modelos de Machine Learning serializados con joblib.
- `static`: Contiene archivos estáticos como hojas de estilo CSS, JavaScript y recursos gráficos.
- `templates`: Incluye las plantillas HTML para las vistas de la aplicación Flask.
- `uploads`: Directorio utilizado para almacenar archivos cargados por los usuarios de la aplicación.
- `app.py`: Archivo principal de la aplicación Flask que define las rutas y la lógica del servidor.
- `index.html`: Página de inicio o index de la aplicación web.

### clean_data
Contiene los datos limpios y procesados que se utilizan para el entrenamiento de los modelos o que se generan como resultado de las predicciones.

### raw_data
Almacena los datos en bruto que se utilizan como entrada para el proceso de limpieza y preparación de datos.

### sennova_virtualenv
Esta carpeta incluye el entorno virtual de Python donde están instaladas todas las dependencias necesarias para el proyecto.

### uploads
Directorio usado por la aplicación Flask para guardar temporalmente los archivos que los usuarios suben para su procesamiento.

### .gitignore
Archivo de configuración para Git que especifica intencionadamente los archivos no rastreados que Git debe ignorar.

### data_pipeline.ipynb
Notebook de Jupyter que contiene el código para el proceso de preparación de datos y entrenamiento de los modelos de Machine Learning.

### Manual de usuario.pdf
Documento que proporciona instrucciones detalladas sobre cómo utilizar la aplicación y los modelos de Machine Learning.

### README.md
Archivo que estás leyendo ahora y que proporciona información general sobre el proyecto y cómo navegar por él.

### requirements.txt
Lista de todas las bibliotecas de Python necesarias para ejecutar la aplicación y los scripts asociados.

## Instalación y Uso

Para instalar y ejecutar este proyecto, necesitarás seguir los siguientes pasos:

1. Clona el repositorio en tu máquina local.
2. Navega al directorio del proyecto y crea un entorno virtual.
3. Activa el entorno virtual e instala las dependencias usando `pip install -r requirements.txt`.
4. Ejecuta `python app.py` para iniciar la aplicación Flask.
5. Abre tu navegador web y ve a `http://localhost:5000` para usar la aplicación.

Para más detalles sobre la instalación y el uso, consulta el 'Manual de usuario.pdf'.
