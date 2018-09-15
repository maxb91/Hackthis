# Hackthis

# Dependencies to install for the database usage
pip install flask-sqlalchemy
pip install flask-migrate

# Setting up the db
from main import db
db.create_all()
from main import Purchases, ReferenceValues, ReferenceValuesUnits
purchase1 = Purchases(category = 'Almonds', amount = 1.0, globalWarmingPotential = 1.0, energyConsumption = 2.0, waterUsage = 3.0)

eval('referenceValues'+str(index)+'=ReferenceValues('+row['category']+','+row['Global Warming Potential (GWP)']+','+row['Energy Consumption']+','+row['Water Usage']+'))

db.add(purchase1)
db.add(units)
db.add(referenceValues)