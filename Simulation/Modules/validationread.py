#to import all validation data from the .xlsx
import pandas as pd
import matplotlib.pyplot as plt

TEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheet_name='TE_DY_ALONGX')
LEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheet_name='LE_DY_ALONGX')
HINGEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheet_name='HINGE_DY_ALONGX')

TEDY = TEDY.values/1000
LEDY = LEDY.values/1000
HINGEDY = HINGEDY.values/1000

#plotting TE DY
plt.plot(TEDY[:,0],TEDY[:,3])
plt.ylabel('dY [m]')
plt.xlabel('x [m]')
plt.show()

#plotting LE DY
plt.plot(LEDY[:,0],LEDY[:,3])
plt.ylabel('dY [m]')
plt.xlabel('x [m]')
plt.show()

#plotting HINGE DY
plt.plot(HINGEDY[:,0],HINGEDY[:,3])
plt.ylabel('dY [m]')
plt.xlabel('x [m]')
plt.show()