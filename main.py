from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from data import Foods
import datetime, json


isDebug = True

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

@app.route('/home')
def index():
  Selections = [keys.category for keys in ReferenceValues.query.all()]
  return render_template('index.html', selections = Selections)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/view_list')
def view_list():
  purch = Purchases.query.all()
  ref_val_unit = ReferenceValuesUnits.query.first()
  units = [ref_val_unit.globalWarmingPotential, ref_val_unit.energyConsumption, ref_val_unit.waterUsage]
  return render_template('view_list.html', purchases = purch, ref_units = units)

@app.route('/results', methods = ['POST'])
def result():
  # Looping through the received object and adding all the elements to the array newData
  newData = []
  # Getting the response and converting it to an object
  postData = json.loads(request.form['purchases'])
  # Looping through the dict and adding the values to the newData list
  for key in postData:
    ref_val = ReferenceValues.query.filter_by(category=key).first()
    # Making sure to not multiply by 'NaN'
    if ref_val.energyConsumption == None:
      ref_val.energyConsumption = 0
      ref_val.waterUsage = 0
    newData.append(Purchases(category = key, amount = postData[key], globalWarmingPotential = round(postData[key]*ref_val.globalWarmingPotential,2), 
                        energyConsumption = round(postData[key]*ref_val.energyConsumption,2), waterUsage = round(postData[key]*ref_val.waterUsage,2)))
  
  db.session.bulk_save_objects(newData)
  db.session.commit()
  return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/piechart')
def piechart():
  purch = Purchases.query.all()
  return render_template('piechart.html', purchases = purch)

@app.route('/barchart')
def barchart():
  purch = Purchases.query.all()
  return render_template('barchart.html', purchases = purch)

@app.route('/overview')
def overview():
  purch = Purchases.query.all()
  ref_val_unit = ReferenceValuesUnits.query.first()
  units = [ref_val_unit.globalWarmingPotential, ref_val_unit.energyConsumption, ref_val_unit.waterUsage]
  return render_template('overview.html', purchases = purch, ref_units = units)  

@app.route('/testData', methods=['GET'])
def provideList():
  purch = Purchases.query.all()
  groupedResponse = {}
  databaseCategories = ['category', 'amount', 'globalWarmingPotential', 'energyConsumption', 'waterUsage']
  # Looping through the dict and grouping to dicts based on the parameter sent
  if request.args.get('option') == 'weekly':
    for lines in purch:
      current = datetime.datetime.isocalendar(lines.dateAdded)[1]
      singleEntry = {}
      for keys in databaseCategories:
        singleEntry[keys] = getattr(lines, keys)
      singleEntry['dateAdded'] = lines.dateAdded.strftime("%Y-%m-%d")
      if current in groupedResponse:
        groupedResponse[current].append(singleEntry)
      else:
        groupedResponse[current] = [singleEntry]
    return json.dumps([{keys: groupedResponse[keys]} for keys in groupedResponse])
  elif request.args.get('option') == 'daily':
    for lines in purch:
      current = datetime.datetime.isocalendar(lines.dateAdded)[-1]
      singleEntry = {}
      for keys in databaseCategories:
        singleEntry[keys] = getattr(lines, keys)
      singleEntry['dateAdded'] = lines.dateAdded.strftime("%Y-%m-%d")
      if current in groupedResponse:
        groupedResponse[current].append(singleEntry)
      else:
        groupedResponse[current] = [singleEntry]
    return json.dumps([{keys: groupedResponse[keys]} for keys in groupedResponse])
  elif request.args.get('option') == 'yearly':
    for lines in purch:
      current = datetime.datetime.isocalendar(lines.dateAdded)[0]
      singleEntry = {}
      for keys in databaseCategories:
        singleEntry[keys] = getattr(lines, keys)
      singleEntry['dateAdded'] = lines.dateAdded.strftime("%Y-%m-%d")
      if current in groupedResponse:
        groupedResponse[current].append(singleEntry)
      else:
        groupedResponse[current] = [singleEntry]
    return json.dumps([{keys: groupedResponse[keys]} for keys in groupedResponse])
  else:
    return abort(400)
if __name__ == '__main__':
  if isDebug == True:
    app.run(debug = True, host='0.0.0.0')
  else:
    app.run(host='0.0.0.0')