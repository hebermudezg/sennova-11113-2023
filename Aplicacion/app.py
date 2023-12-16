# Importing libraries 
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import plotly.express as px
import pandas as pd
import json
from plotly.utils import PlotlyJSONEncoder
import joblib
from flask import request
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Reemplaza con una clave secreta real
app.config['UPLOAD_FOLDER'] = 'uploads'


# Carga de los modelos previamente entrenados
#logistic_model = joblib.load('models/logistic_model.joblib')
#random_forest_model = joblib.load('models/random_forest_model.joblib')

# Asegurar que la carpeta de subidas exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


USER_CREDENTIALS = {'username': 'adminis', 'password': '123'}

df = pd.read_csv('../clean_data/cleaned_data.csv')

def filter_dataframe(gender, smoking):
    df_filtered = df
    if gender:
        df_filtered = df_filtered[df_filtered['VRXSEXO'] == gender]
    if smoking:
        df_filtered = df_filtered[df_filtered['TABAQUISMO'] == smoking]
    return df_filtered

def create_age_distribution_plot(df_filtered):
    # Configuración del gráfico
    fig = px.histogram(df_filtered, x="AGE", 
                       title="Distribución de Edades",
                       labels={'AGE': 'Edad'},
                       color_discrete_sequence=['#85C1E9'], # Color azul claro
                       template='simple_white', # Fondo blanco simple
                       opacity=0.8, # Transparencia del histograma
                       marginal='rug') # Línea de densidad en el margen

    # Mejorar la legibilidad y estilo
    fig.update_layout(
        title={'text': "Distribución de Edades de los Pacientes",
               'y':0.9,
               'x':0.5,
               'xanchor': 'center',
               'yanchor': 'top'},
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        ),
        xaxis_title="Edad",
        yaxis_title="Cantidad",
        plot_bgcolor='white', # Fondo del gráfico
    )

    return json.dumps(fig, cls=PlotlyJSONEncoder)

# plot 1
def create_bmi_gender_plot(df_filtered):
    # Calculando el promedio de IMC por género
    bmi_avg_per_gender = df_filtered.groupby('VRXSEXO')['NIMC'].mean().reset_index()

    # Configuración del gráfico
    fig = px.bar(bmi_avg_per_gender, x="VRXSEXO", y="NIMC",
                 title="Promedio de Índice de Masa Corporal por Género",
                 labels={'VRXSEXO': 'Género', 'NIMC': 'Índice de Masa Corporal'},
                 color='VRXSEXO', 
                 color_discrete_map={'M': '#3498DB', 'F': '#FFC0CB'}, # Azul para M y Rosa para F
                 template='simple_white') # Fondo blanco simple

    # Mejorar la legibilidad y estilo
    fig.update_layout(
        title={'text': "Promedio de Índice de Masa Corporal por Género",
               'y':0.9,
               'x':0.5,
               'xanchor': 'center',
               'yanchor': 'top'},
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        ),
        xaxis_title="Género",
        yaxis_title="Índice de Masa Corporal",
        plot_bgcolor='white', # Fondo del gráfico
    )

    return json.dumps(fig, cls=PlotlyJSONEncoder)

# plot 2
def create_blood_pressure_plot(df_filtered):
    # Configuración del gráfico
    fig = px.scatter(df_filtered, x="NPASS", y="NPADS",
                     title="Relación entre Presión Arterial Sistólica y Diastólica",
                     labels={'NPASS': 'Presión Sistólica (mm Hg)', 'NPADS': 'Presión Diastólica (mm Hg)'},
                     color_discrete_sequence=['#17BECF'], # Color uniforme para todos los puntos
                     template='simple_white') # Fondo blanco simple

    # Mejorar la legibilidad y estilo
    fig.update_layout(
        title={'text': "Relación entre Presión Arterial Sistólica y Diastólica",
               'y':0.9,
               'x':0.5,
               'xanchor': 'center',
               'yanchor': 'top'},
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        ),
        xaxis_title="Presión Sistólica (mm Hg)",
        yaxis_title="Presión Diastólica (mm Hg)",
        plot_bgcolor='white', # Fondo del gráfico
    )

    return json.dumps(fig, cls=PlotlyJSONEncoder)

# plot 3
def create_smoking_prevalence_plot(df_filtered):
    # Conteo de la prevalencia de tabaquismo
    smoking_counts = df_filtered['TABAQUISMO'].value_counts().reset_index()
    smoking_counts.columns = ['TABAQUISMO', 'COUNT']

    # Configuración del gráfico
    fig = px.bar(smoking_counts, x='TABAQUISMO', y='COUNT',
                 title="Prevalencia de Tabaquismo",
                 labels={'TABAQUISMO': 'Estado de Tabaquismo', 'COUNT': 'Cantidad'},
                 color='TABAQUISMO',
                 color_discrete_sequence=['#1F77B4', '#FF7F0E', '#2CA02C'], # Colores para las categorías
                 template='simple_white') # Fondo blanco simple

    # Mejorar la legibilidad y estilo
    fig.update_layout(
        title={'text': "Prevalencia de Tabaquismo",
               'y':0.9,
               'x':0.5,
               'xanchor': 'center',
               'yanchor': 'top'},
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        ),
        xaxis_title="Estado de Tabaquismo",
        yaxis_title="Cantidad",
        plot_bgcolor='white', # Fondo del gráfico
    )

    return json.dumps(fig, cls=PlotlyJSONEncoder)

# plot 4
def create_age_gender_distribution_plot(df_filtered):
    fig = px.histogram(df_filtered, x="AGE", color="VRXSEXO",
                       barmode='overlay',  # Modo superposición para apilar los histogramas
                       nbins=30,           # Número de bins
                       opacity=0.6,        # Transparencia de las barras
                       title="Distribución de Edades por Género",
                       labels={"AGE": "Edad", "VRXSEXO": "Género"},
                       color_discrete_map={"M": "blue", "F": "magenta"})  # Colores por género

    # Mejorar la legibilidad y estilo del gráfico
    fig.update_layout(
        yaxis_title="Cantidad",
        xaxis_title="Edad",
        legend_title="Género",
        template="simple_white"
    )
    return json.dumps(fig, cls=PlotlyJSONEncoder)

# Función para el gráfico de comparación de la presión arterial sistólica por sexo
def create_bp_comparison_plot(df_filtered):
    fig = px.box(df, x='VRXSEXO', y='NPASS', 
                 title='Comparación de la Presión Arterial Sistólica por Sexo',
                 labels={'VRXSEXO': 'Sexo', 'NPASS': 'Presión Arterial Sistólica'})
    return json.dumps(fig, cls=PlotlyJSONEncoder)

# Función para el gráfico de comparación del Índice de Masa Corporal entre fumadores y no fumadores
def create_bmi_comparison_plot(df_filtered):
    fig = px.box(df, x='TABAQUISMO', y='NIMC', 
                 title='Comparación del Índice de Masa Corporal entre Fumadores y No Fumadores',
                 labels={'TABAQUISMO': 'Tabaquismo', 'NIMC': 'Índice de Masa Corporal'})
    return json.dumps(fig, cls=PlotlyJSONEncoder)

# Función para el gráfico de la relación entre la edad y la medida de cintura
def create_age_waist_plot(df_filtered):
    fig = px.scatter(df, x='AGE', y='NCINTURA', color='VRXSEXO',
                     title='Relación entre la Edad y la Medida de Cintura',
                     labels={'AGE': 'Edad', 'NCINTURA': 'Medida de Cintura', 'VRXSEXO': 'Sexo'})
    return json.dumps(fig, cls=PlotlyJSONEncoder)

# Función para crear un histograma de distribución de edad por enfermedad
def create_age_distribution_by_disease_plot(df):
    fig = px.histogram(df, x="AGE", color="ENFERMEDAD_VKPCODIGO",
                       title="Distribución de Edad por Enfermedad",
                       labels={'AGE': 'Edad', 'ENFERMEDAD_VKPCODIGO': 'Código de Enfermedad'},
                       barmode='overlay', opacity=0.6)
    return json.dumps(fig, cls=PlotlyJSONEncoder)

# Función para crear un diagrama de caja comparando la presión arterial por enfermedad
def create_bp_by_disease_plot(df):
    fig = px.box(df, x="ENFERMEDAD_VKPCODIGO", y="NPASS",
                 title="Comparación de la Presión Arterial Sistólica por Enfermedad",
                 labels={'ENFERMEDAD_VKPCODIGO': 'Código de Enfermedad', 'NPASS': 'Presión Arterial Sistólica'})
    return json.dumps(fig, cls=PlotlyJSONEncoder)

# Función para crear un gráfico de dispersión de IMC vs. enfermedad
def create_bmi_vs_disease_plot(df):
    fig = px.scatter(df, x="ENFERMEDAD_VKPCODIGO", y="NIMC", color="VRXSEXO",
                     title="Relación entre IMC y Enfermedad",
                     labels={'ENFERMEDAD_VKPCODIGO': 'Código de Enfermedad', 'NIMC': 'Índice de Masa Corporal'})
    return json.dumps(fig, cls=PlotlyJSONEncoder)

# Función para crear un gráfico de barras de prevalencia de tabaquismo por enfermedad
def create_smoking_prevalence_by_disease_plot(df):
    smoking_counts = df.groupby(['ENFERMEDAD_VKPCODIGO', 'TABAQUISMO']).size().reset_index(name='COUNT')
    fig = px.bar(smoking_counts, x='ENFERMEDAD_VKPCODIGO', y='COUNT', color='TABAQUISMO',
                 title="Prevalencia de Tabaquismo por Enfermedad",
                 labels={'ENFERMEDAD_VKPCODIGO': 'Código de Enfermedad', 'COUNT': 'Cantidad', 'TABAQUISMO': 'Tabaquismo'})
    return json.dumps(fig, cls=PlotlyJSONEncoder)




@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials. Please try again.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/get-plot/<plot_type>')
def get_plot(plot_type):
    gender = request.args.get('gender')
    smoking = request.args.get('smoking')
    df_filtered = filter_dataframe(gender, smoking)

    if plot_type == 'age_distribution':
        return create_age_distribution_plot(df_filtered)
    elif plot_type == 'bmi_gender':
        return create_bmi_gender_plot(df_filtered)
    elif plot_type == 'blood_pressure':
        return create_blood_pressure_plot(df_filtered)
    elif plot_type == 'smoking_prevalence':
        return create_smoking_prevalence_plot(df_filtered)
    elif plot_type == 'age_gender_distribution':
        return create_age_gender_distribution_plot(df_filtered)
    elif plot_type == 'bp_comparison':
        return create_bp_comparison_plot(df_filtered)
    elif plot_type == 'bmi_comparison':
        return create_bmi_comparison_plot(df_filtered)
    elif plot_type == 'age_waist':
        return create_age_waist_plot(df_filtered)
    elif plot_type == 'age_distribution_by_disease':
        return create_age_distribution_by_disease_plot(df_filtered)
    elif plot_type == 'bp_by_disease':
        return create_bp_by_disease_plot(df_filtered)
    elif plot_type == 'bmi_vs_disease':
        return create_bmi_vs_disease_plot(df_filtered)
    elif plot_type == 'smoking_prevalence_by_disease':
        return create_smoking_prevalence_by_disease_plot(df_filtered)
    else:
        return jsonify({'error': 'Invalid plot type'}), 400


@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
    table_html = None
    if request.method == 'POST':
        file = request.files.get('datafile')
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Convertir el DataFrame a HTML
            df = pd.read_csv(filepath)
            table_html = df.head().to_html(classes='table table-bordered', index=False)

    return render_template('alerts.html', table_html=table_html)



@app.route('/predict/<filename>')
def predict(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        data = pd.read_csv(filepath)
        # Asegúrate de aplicar el mismo preprocesamiento que usaste al entrenar los modelos
        # ...

        logistic_pred = logistic_model.predict(data)
        random_forest_pred = random_forest_model.predict(data)

        data['Logistic_Prediction'] = logistic_pred
        data['RandomForest_Prediction'] = random_forest_pred

        result_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'prediction_results.csv')
        data.to_csv(result_filepath, index=False)

        return send_file(result_filepath, as_attachment=True)
    except Exception as e:
        return f"Error processing the file: {e}"


if __name__ == '__main__':
    app.run(debug=True)
