from main import db
import pandas as pd
db.create_all()

from main import Purchases, ReferenceValues, ReferenceValuesUnits
purchase1 = Purchases(category = 'Almonds', amount = 1.0, globalWarmingPotential = 1.0, energyConsumption = 2.0, waterUsage = 3.0)
db.session.add(purchase1)
print('Purchases values migrated\n')

EmissionData = pd.read_excel('EmissionValues.xlsx')

for index, row in EmissionData.iterrows():

    if type(row['Energy Consumption']) == str:
        referenceValues = ReferenceValues(row['Category'], row['Global Warming Potential (GWP)'], -1, -1)
        db.session.add(referenceValues)
        db.session.commit()
        
    else:
        referenceValues = ReferenceValues(row['Category'], row['Global Warming Potential (GWP)'], row['Energy Consumption'], row['Water Usage'])
        db.session.add(referenceValues)
        db.session.commit()
        

print('Reference values migrated\n')

UnitsData = pd.read_csv('Units.csv', delimiter = ';')

for index, row in UnitsData.iterrows():
    unitsValues = ReferenceValuesUnits(row['Global Warming Potential (GWP)'], row['Energy Consumption'], row['Water Usage'])
    db.session.add(unitsValues)
    db.session.commit()

print('Units values migrated\n')