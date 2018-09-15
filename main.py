from flask import Flask, render_template, request
import pandas as pd
from data import Foods

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

@app.route('/result', methods = ['GET', 'POST'])
def result():
	print ("printing results")
	return(request.form['foodtype'] + ' | ' + request.form['text'])

if __name__ == '__main__':
	app.run(debug = True)