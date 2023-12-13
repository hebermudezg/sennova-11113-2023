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
    fig = px.histogram(df_filtered, x="AGE", title="Distribución de Edades")
    return json.dumps(fig, cls=PlotlyJSONEncoder)

def create_bmi_gender_plot(df_filtered):
    fig = px.bar(df_filtered, x="VRXSEXO", y="NIMC", title="Índice de Masa Corporal por Género")
    return json.dumps(fig, cls=PlotlyJSONEncoder)

def create_blood_pressure_plot(df_filtered):
    fig = px.scatter(df_filtered, x="NPASS", y="NPADS", title="Presión Arterial Sistólica vs. Diastólica")
    return json.dumps(fig, cls=PlotlyJSONEncoder)

def create_smoking_prevalence_plot(df_filtered):
    smoking_counts = df_filtered['TABAQUISMO'].value_counts()
    fig = px.bar(smoking_counts, x=smoking_counts.index, y=smoking_counts.values, title="Prevalencia de Tabaquismo")
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
    else:
        return jsonify({'error': 'Invalid plot type'}), 400




@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('predict', filename=filename))
        else:
            flash('Invalid file type or no file selected.')
    return render_template('alerts.html')


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
