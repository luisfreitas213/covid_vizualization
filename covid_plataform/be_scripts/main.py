import pandas as pd
import numpy as np
import requests
import os
import cases
import deaths
import vacination
import manage_db
import db_predicton
import history


'''
***
1.Back-End - Situação Atual
***
'''
# Function to import data sets (with url)
def get_data(url):
    csv_url = url
    req = requests.get(csv_url)
    url_content = req.content
    csv_file = open('downloaded.csv', 'wb')
    csv_file.write(url_content)
    csv_file.close()
    df = pd.read_csv('downloaded.csv')
    os.remove("downloaded.csv")
    return df

df_cases_deaths_rate = get_data("https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/csv")

df_vacine = get_data("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")

df_cases_top, df_cases_deaths_rate, df_cases, df_cases_continent = cases.cases(df_cases_deaths_rate)

df_deaths, df_cases_top = deaths.deaths(df_cases_deaths_rate, df_cases_top)

df_vacine_top_15, df_vacine = vacination.vacination(df_vacine, df_cases)

manage_db.manage_db(df_cases_top,df_cases_continent,df_vacine_top_15 )

'''
***
2.Back-End - History
***
'''
history.history()
'''
***
3.Back-End - Previsões
***
'''

#Country 1
#Parameters
country = 'India'
n_steps = 5
units = 100
layers = 3
drop = 0.2
epochs = 200
batch_size = 5
optimizer = 'adam'
dim_test = 5

db_predicton.db_predicton('pred_1', country, n_steps, units, layers, drop, epochs, batch_size, optimizer, dim_test)

#Country 2
#Parameters
country = 'Brazil'
n_steps = 5
units = 100
layers = 3
drop = 0.2
epochs = 200
batch_size = 5
optimizer = 'adam'
dim_test = 5

db_predicton.db_predicton('pred_2', country, n_steps, units, layers, drop, epochs, batch_size, optimizer, dim_test)

#Country 3
#Parameters
country = 'Colombia'
n_steps = 5
units = 100
layers = 3
drop = 0.2
epochs = 200
batch_size = 5
optimizer = 'adam'
dim_test = 5

db_predicton.db_predicton('pred_3', country, n_steps, units, layers, drop, epochs, batch_size, optimizer, dim_test)

#Country 4
#Parameters
country = 'Argentina'
n_steps = 5
units = 100
layers = 3
drop = 0.2
epochs = 200
batch_size = 5
optimizer = 'adam'
dim_test = 5

db_predicton.db_predicton('pred_4', country, n_steps, units, layers, drop, epochs, batch_size, optimizer, dim_test)

#Country 5
#Parameters
country = 'United States Of America'
n_steps = 5
units = 100
layers = 3
drop = 0.2
epochs = 200
batch_size = 5
optimizer = 'adam'
dim_test = 5

db_predicton.db_predicton('pred_5', country, n_steps, units, layers, drop, epochs, batch_size, optimizer, dim_test)
