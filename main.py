from flask import Flask, render_template, request
import pandas as pd

EmissonData = pd.read_excel('EmissionValues.xlsx')

app = Flask(__name__)

@app.route('/')
def index():
	Selections = EmissonData['Category']
	return render_template('basic.html', selections = Selections)

@app.route('/test', methods = ['GET', 'POST'])
def result():
	print ("printing results")
	return(request.form['colours'] + ' | ' + request.form['text'])

if __name__ == '__main__':
	app.run(debug = True)