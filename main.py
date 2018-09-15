from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import datetime

EmissionData = pd.read_excel('EmissionValues.xlsx')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purchases.sqlite3'
db = SQLAlchemy(app)

class Purchases(db.Model):

	id = db.Column('entry_id', db.Integer, primary_key = True)
	category = db.Column(db.String(100))
	amount = db.Column(db.Float)
	globalWarmingPotential = db.Column(db.Float)
	energyConsumption = db.Column(db.Float)
	waterUsage = db.Column(db.Float)
	dateAdded = db.Column(db.DateTime, nullable = False, default = datetime.datetime.utcnow)

	def __init__(self, category = None, amount = None, globalWarmingPotential = None, energyConsumption = None, waterUsage = None):
		self.category = category
		self.amount = amount
		self.globalWarmingPotential = globalWarmingPotential
		self.energyConsumption = energyConsumption
		self.waterUsage = waterUsage

	def __repr__(self):
		return f"Purchase('{self.category}', '{self.amount}', '{self.globalWarmingPotential}', '{self.energyConsumption}', '{self.waterUsage}')"

class ReferenceValues(db.Model):

	id = db.Column('entry_id', db.Integer, primary_key = True)
	category = db.Column(db.String(100))
	globalWarmingPotential = db.Column(db.Float)
	energyConsumption = db.Column(db.Float)
	waterUsage = db.Column(db.Float)

	def __init__(self, )

	def __repr__(self):
		return f"ReferenceValues('{self.category}', '{self.globalWarmingPotential}', '{self.energyConsumption}', '{self.waterUsage}')"

class ReferenceValuesUnits(db.Model):

	id = db.Column('entry_id', db.Integer, primary_key = True)
	globalWarmingPotential = db.Column(db.Float)
	energyConsumption = db.Column(db.Float)
	waterUsage = db.Column(db.Float)

	def __repr__(self):
		return f"ReferenceValues('{self.globalWarmingPotential}', '{self.energyConsumption}', '{self.waterUsage}')"



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