from flask import Flask, render_template, request
import pandas as pd
from data import Foods
import requests

Foods = Foods()
EmissonData = pd.read_excel('EmissionValues.xlsx')

app = Flask(__name__)

@app.route('/')
def index():
	Selections = EmissonData['Category']
	return render_template('index.html', selections = Selections)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/view_list')
def view_list():
  return render_template('view_list.html', foods = Foods)

@app.route('/result', methods = ['POST'])
def result():
	print ("printing results")
	test = request.form['javascript_data']
	return test

@app.route('/receivedata', methods = ['POST'])
def receive_data():
	#data = request.json['data']
	for k in request.form.keys():
		print(k + request.form[k])
	return "data"

if __name__ == '__main__':
	app.run(debug = True)