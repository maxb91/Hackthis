from main import db
# db.create_all()

from main import Purchases, ReferenceValues, ReferenceValuesUnits
purchase1 = Purchases(category = 'Almonds', amount = 1.0, globalWarmingPotential = 1.0, energyConsumption = 2.0, waterUsage = 3.0)
# db.add(purchase1)

import pandas as pd

EmissionData = pd.read_excel('EmissionValues.xlsx')

for index, row in EmissionData.iterrows():
    if type(row['Energy Consumption']) == str:
        referenceValues = ReferenceValues(row['Category'], row['Global Warming Potential (GWP)'], -1, -1)
        db.add(referenceValues)
        db.commit()
    else:
        referenceValues = ReferenceValues(row['Category'], row['Global Warming Potential (GWP)'], row['Energy Consumption'], row['Water Usage'])
        db.add(referenceValues)
        db.commit()
