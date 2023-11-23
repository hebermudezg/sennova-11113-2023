from flask import Flask, render_template, request, redirect, url_for, flash
import plotly.express as px
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Hardcoded user credentials for simplicity
USER_CREDENTIALS = {'username': 'adminis', 'password': '123'}

# Function to create a Plotly plot
def create_iris_plot():
    # Define column names
    columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
    # Read the dataset with specified column names
    iris_df = pd.read_csv('clean_data/iris.txt', header=None, names=columns)
    # Create the plot
    fig = px.scatter(iris_df, x="sepal_width", y="sepal_length", color="species")
    return fig.to_json()


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
    plot_json = create_iris_plot()
    return render_template('dashboard.html', plot_json=plot_json)

@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
    # Placeholder for alerts functionality
    return render_template('alerts.html')

if __name__ == '__main__':
    app.run(debug=True)
