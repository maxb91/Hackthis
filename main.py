from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from data import Foods
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
    return "Purchase('{self.category}', '{self.amount}', '{self.globalWarmingPotential}', '{self.energyConsumption}', '{self.waterUsage}')"

class ReferenceValues(db.Model):
  id = db.Column('entry_id', db.Integer, primary_key = True)
  category = db.Column(db.String(100))
  globalWarmingPotential = db.Column(db.Float)
  energyConsumption = db.Column(db.Float)
  waterUsage = db.Column(db.Float)
  def __init__(self, category = None, globalWarmingPotential = None, energyConsumption = None, waterUsage = None):
    self.category = category
    self.globalWarmingPotential = globalWarmingPotential
    self.energyConsumption = energyConsumption
    self.waterUsage = waterUsage
  def __repr__(self):
    return "ReferenceValues('{self.category}', '{self.globalWarmingPotential}', '{self.energyConsumption}', '{self.waterUsage}')"

class ReferenceValuesUnits(db.Model):
  id = db.Column('entry_id', db.Integer, primary_key = True)
  globalWarmingPotential = db.Column(db.Float)
  energyConsumption = db.Column(db.Float)
  waterUsage = db.Column(db.Float)
  def __init__(self, globalWarmingPotential = None, energyConsumption = None, waterUsage = None):
    self.waterUsage = waterUsage
    self.globalWarmingPotential = globalWarmingPotential
    self.energyConsumption = energyConsumption
  def __repr__(self):
    return "ReferenceValues('{self.globalWarmingPotential}', '{self.energyConsumption}', '{self.waterUsage}')"

@app.route('/')
def index():
  Selections = EmissionData['Category'].dropna()
  return render_template('index.html', selections = Selections)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/view_list')
def view_list():
  print "Querying"
  abc = Purchases.query.all()
  print "Purchases are ", abc
  return render_template('view_list.html', purchases = abc)

@app.route('/result', methods = ['GET', 'POST'])
def result():
  amount = float(request.form['text'])
  sel_category = request.form['foodtype']
  ref_val = ReferenceValues.query.filter_by(category=sel_category).first()
  purchase = Purchases(category = sel_category, amount = amount, globalWarmingPotential = amount*ref_val.globalWarmingPotential, 
                        energyConsumption = amount*ref_val.energyConsumption, waterUsage = amount*ref_val.waterUsage)
  db.session.add(purchase)
  db.session.commit()  
  print "Added."
  return("Added item.")

if __name__ == '__main__':
	app.run(debug = True)
