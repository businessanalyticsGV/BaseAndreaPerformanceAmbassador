import pandas as pd
import numpy as np
import os
import datetime
from datetime import timedelta as td
pd.set_option('display.max_columns',500)

print('\n\nVentas Offsite...\n\n')

## I.- EXTRACTING FILE

path = '//NVO01WINAP0023A/Procesos Sense/Respaldos Ventas Off Site/'


yesterday = datetime.datetime.now()+td(days=-1)
yesterday = datetime.datetime.strftime(yesterday,'%Y-%m-%d')

df = pd.read_csv(path+'Ventas Off Site_'+yesterday+'.csv')

print(yesterday)

#ls = os.listdir(path)
#ls = [(f,f[-14:][:10]) for f in ls]
#df = pd.DataFrame(ls,columns=['name','txtdate'])
#df['date'] = [((d[:4]),(d[5:7]),(d[-2:])) for d in df['txtdate']]
#df['true'] = ['S' in d[0] for d in df['date']]
#df = df[df['true'] == False]
#df['date'] = [datetime.datetime(int(d[0]),int(d[1]),int(d[2])) for d in df['date']]
#df = df[df['date'] == max(df['date'])].iloc[0,0]






#print(df.head())
## II.- LOADING FRAME AND MERGING WITH DATE CATALOGUE
df_dates = pd.read_excel('//NVO01WINAP0023A/Procesos Sense/Catalogos/Catalog Fecha.xlsx')
df_dates = df_dates[['Fecha','Semana_Myn','Año-Sem Mayan','Año_Myn']]
df_dates.rename(columns = {'Año-Sem Mayan':'Año_Semana'}, inplace = True)
df_dates['Año_Semana'] = [str(year) + ' - ' + str(week) if int(week) >9 else\
                          str(year) + ' - 0' + str(week) \
                          for year,week in zip(df_dates['Año_Myn'],df_dates['Semana_Myn'])]

df_dates.rename(columns = {'Fecha':'Fecha finiquito estadística'}, inplace = True)

date = 'Fecha finiquito estadística'
df[date] = pd.to_datetime(df[date],format='%d/%m/%Y')
print(df.shape)
df = df.merge(df_dates, how = 'left', on = ['Fecha finiquito estadística'])
print(str(df.shape)+' dates')

df_cat = pd.read_excel('catalogoPlaza.xlsx')
df = df.merge(df_cat, how = 'left', on = ['PLAZA AJUSTE'])
print(str(df.shape)+' plaza')

df_cat = pd.read_excel('catalogoPlaza.xlsx', sheet_name = 'Sistema')
df = df.merge(df_cat, how = 'left', on = ['SISTEMA On (f) Agrup Rentas'])
print(str(df.shape)+' sistema')

df = df[df['Año_Myn'] >= 2016]
print(str(df.shape)+' >=2016\n\n')

print(np.unique(df['SISTEMA On (f) Agrup Rentas']))
## print(np.unique(df['Sistema']))

df = df.groupby(['PlazaBuena',
                 'Sistema',
                 'Año_Semana'], as_index = True)[['ContractNumber']].nunique()
df = pd.DataFrame(df.to_records())
df.rename(columns = {'ContractNumber':'Ventas'}, inplace = True)

def frame():
    return(df)
