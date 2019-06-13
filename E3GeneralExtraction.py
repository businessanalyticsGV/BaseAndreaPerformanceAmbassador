import pandas as pd
import numpy as np
import E1VentasOffSite_Extraction as offsite
import E2Tours_Extraction as tours

llave = ['PlazaBuena','Sistema','Año_Semana']

df = offsite.frame().merge(tours.frame(), on = llave, how = 'outer')
df = df[(df['Sistema'] == 'IN-HOUSE') | (df['Sistema'] == 'STREET')]

df.to_excel('base.xlsx', index = False)
#df.to_csv('base.csv', index = False)
print(df.shape)
print(df.head())

### TO AUTOMATE WITH POWER SHELL
# E:\"Procesos Sense"\"Modelos BA"\"SaulExtracciones"\"01. 28Mar2019 - Performance Ambassador" ;; py .\E3GeneralExtraction.py
