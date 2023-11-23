from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    cleaned_data = pd.read_csv('clean_data/cleaned_data.csv')
    fig = px.histogram(cleaned_data, x='NIMC', nbins=50, title='Distribution of BMI')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', plot=graphJSON)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            data = pd.read_csv(uploaded_file)
            # Process and predict here
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
