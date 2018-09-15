from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

EmissionData = pd.read_excel('EmissionValues.xlsx')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purchases.sqlite3'
db = SQLAlchemy(app)

@app.route('/')
def index():
  Selections = EmissionData['Category'].dropna()
  return render_template('basic.html', selections = Selections)

@app.route('/test', methods = ['GET', 'POST'])
def result():
  print ("printing results")
  return(request.form['colours'] + ' | ' + request.form['text'])

if __name__ == '__main__':
  app.run(debug = True)
