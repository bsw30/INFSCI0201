from flask import Flask, render_template, request
import requests
from datetime import datetime
from apod_model import fetch_apod_data

app = Flask(__name__)

API_KEY = "gMzEXxheSX3XwHvBkCDK9qRYG6d4XMVcRhi31N8K"
API_URL = "https://api.nasa.gov/planetary/apod"

@app.route('/')
def index():
    return render_template('landing_page.html')

@app.route('/history', methods=['GET', 'POST'])
def history():
    apod_data = {}
    if request.method == 'POST':
        selected_date = request.form['date']
        apod_data = fetch_apod_data(selected_date)
    return render_template('history.html', apod_data=apod_data)


if __name__ == '__main__':
    app.run(debug=True)