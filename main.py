from flask import Flask, render_template
import pandas as pd

EmissonData = pd.read_excel('EmissionValues.xlsx')

app = Flask(__name__)

@app.route('/')
def index():
	Selections = EmissonData['Category']
	return render_template('basic.html', selections = Selections)

if __name__ == '__main__':
	app.run(debug = True)