#to import all validation data from the .xlsx
import pandas as pd
import matplotlib.pyplot as plt

exec(open("./Data.txt").read())

TEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheetname=0)
LEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheetname=1)
HINGEDY = pd.read_excel('validation_dy_te_le_hinge.xlsx', sheetname=2)
#X,Y,Z,dY

TEDY = TEDY.values/1000
LEDY = LEDY.values/1000
HINGEDY = HINGEDY.values/1000

TEDY[:,0] = TEDY[:,0]-la/2
LEDY[:,0] = LEDY[:,0]-la/2
HINGEDY[:,0] = HINGEDY[:,0]-la/2

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