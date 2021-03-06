import pandas as pd
import numpy as np
import os
import datetime
from datetime import date as dt
from datetime import timedelta as td

print('\n\nTours...\n\n')

pd.set_option('display.max_columns',500)

## I.- EXTRACTING FILE
date = dt.today()+td(days = -1)
date = dt.strftime(date,'%Y%m%d')
print(date)

path = '//NVO01WINAP0023A/Procesos SQL/Rentabilidad/files/'
files = [f for f in os.listdir(path) if 'ToursRevenueNal' in f and date in f][0]
print(files)

ls_columns = ['Clave','EmpresaNombre','Fecha','SistemaVenta']
df = pd.read_csv(path+files)
df = df[df['Locacion'] != 237][ls_columns]
df['Fecha'] = pd.to_datetime(df['Fecha'], format = '%d/%m/%Y')

### FECHA
df_dates = pd.read_excel('//NVO01WINAP0023A/Procesos Sense/Catalogos/Catalog Fecha.xlsx')
df_dates = df_dates[['Fecha','Semana_Myn','Año-Sem Mayan','Año_Myn']]
df_dates.rename(columns = {'Año-Sem Mayan':'Año_Semana'}, inplace = True)
df_dates['Año_Semana'] = [str(year) + ' - ' + str(week) if int(week) >9 else\
                          str(year) + ' - 0' + str(week) \
                          for year,week in zip(df_dates['Año_Myn'],df_dates['Semana_Myn'])]

print(df.shape)
df = df.merge(df_dates, how = 'left', on = ['Fecha'])
print(str(df.shape)+' dates')

df_cat = pd.read_excel('catalogoPlaza.xlsx', sheet_name = 'Tours')
df = df.merge(df_cat, how = 'left', on = ['EmpresaNombre'])
print(str(df.shape)+' plaza')

df = df[df['Año_Myn'] >= 2016]
print(str(df.shape)+' >=2016\n\n')
df.rename(columns = {'SistemaVenta':'Sistema'}, inplace = True)

## print(np.unique(df['Sistema']))

df = df.groupby(['PlazaBuena',
                 'Sistema',
                 'Año_Semana'], as_index = True)[['Clave']].nunique()
df = pd.DataFrame(df.to_records())
df.rename(columns = {'Clave':'Tours'}, inplace = True)
#### EXCEPTION 1 - 02 APRIL 2019: REMOVED 'PLAN DE DESCANSO'
df = df[df['PlazaBuena'] != 'PLAN DE DESCANSO']

def frame():
    return(df)