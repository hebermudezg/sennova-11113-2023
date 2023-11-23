from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import json
from plotly.utils import PlotlyJSONEncoder  # Import PlotlyJSONEncoder directly


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Load the cleaned data
    cleaned_data = pd.read_csv('clean_data/cleaned_data.csv')

    # Create a histogram of the BMI (NIMC) distribution
    fig = px.histogram(cleaned_data, x='NIMC', nbins=50, title='Distribution of BMI')

    # Convert the figure to JSON using the directly imported PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)

    return render_template('dashboard.html', plot=graphJSON)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            data = pd.read_csv(uploaded_file)
            # Here you can add code to process the data and make predictions
            # predictions = model.predict(data)
            # Then, you might want to return the predictions or render another template
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
