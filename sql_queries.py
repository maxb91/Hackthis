from main import db
from datatypes import Purchases, ReferenceValues, ReferenceValuesUnits

ReferenceValues.query.filter_by(category='beef').all()
Purchases.query.filter_by(category='Almonds').all()