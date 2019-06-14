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

## 0.- WHICH ONES ARE COB ACAPULCO?                             ## QUESTION 1
print('Extracting COB 237')
print('Before Removing: ',df.shape[0])
yesterdayCOB = datetime.datetime.now()+td(days=-1)
yesterdayCOB = datetime.datetime.strftime(yesterdayCOB,'%Y%m%d')

path_cob_acapulco = '//NVO01WINAP0023A/Procesos SQL/Rentabilidad/files/'
path_cob_acapulco = path_cob_acapulco+yesterdayCOB+' - ToursRevenueNal.csv'
df_cob = pd.read_csv(path_cob_acapulco)[['Contrato','Locacion']]
df_cob.rename(columns = {'Contrato':'ContractNumber'}, inplace = True)
df_cob = df_cob[(df_cob['Locacion'] == 237) & (pd.notnull(df_cob['ContractNumber']))] #<:::: ANSWER 1
print(len(np.unique(df_cob['ContractNumber'])),df_cob.shape[0])

df = df.merge(df_cob, how = 'left', on = ['ContractNumber'])
df = df[df['Locacion'] != 237]
df = df.drop(columns = ['Locacion'])

print('After Removing: ',df.shape[0])
print(yesterday)

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
