import pandas as pd
import numpy as np
import os
import datetime
pd.set_option('display.max_columns',500)

## I.- EXTRACTING FILE

path = '//NVO01WINAP0023A/Procesos Sense/Respaldos Ventas Off Site/'
ls = os.listdir(path)
ls = [(f,f[-14:][:10]) for f in ls]
df = pd.DataFrame(ls,columns=['name','txtdate'])
df['date'] = [((d[:4]),(d[5:7]),(d[-2:])) for d in df['txtdate']]
df['true'] = ['S' in d[0] for d in df['date']]
df = df[df['true'] == False]
df['date'] = [datetime.datetime(int(d[0]),int(d[1]),int(d[2])) for d in df['date']]
df = df[df['date'] == max(df['date'])].iloc[0,0]

## II.- LOADING FRAME AND MERGING WITH DATE CATALOGUE
df_dates = pd.read_excel('//NVO01WINAP0023A/Procesos Sense/Catalogos/Catalog Fecha.xlsx')
df_dates = df_dates[['Fecha','Semana_Myn','Año_Semana']]
df_dates.rename(columns = {'Fecha':'Fecha finiquito estadística'}, inplace = True)

df = pd.read_csv(path+df)
date = 'Fecha finiquito estadística'
df[date] = pd.to_datetime(df[date],format='%d/%m/%Y')
print(df.shape)
df = df.merge(df_dates, how = 'left', on = ['Fecha finiquito estadística'])
print(df.shape)

df_cat = pd.read_excel('catalogoPlaza.xlsx')
df = df.merge(df_cat, how = 'left', on = ['PLAZA AJUSTE'])
print(df.shape)

df = df.groupby(['PlazaBuena',
                 'SISTEMA On (f) Agrup Rentas',
                 'Año_Semana'], as_index = True)[['ContractNumber']].nunique()

def frame():
    return(df)
