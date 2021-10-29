import pandas as pd
import numpy as np
import requests
import os

def deaths(df_cases_deaths_rate, df_cases_top):
    #Filter Dataset Deaths and change name columns
    df_deaths = df_cases_deaths_rate[df_cases_deaths_rate['indicator']=='deaths']
    df_deaths = df_deaths.drop(['country_code', 'indicator', 'year_week','continent','population'], axis = 1)
    df_deaths['weekly_count_deaths']=df_deaths['weekly_count']
    df_deaths['rate_14_day_deaths']=df_deaths['rate_14_day']
    df_deaths['cumulative_count_deaths']=df_deaths['cumulative_count']
    df_deaths = df_deaths.drop(['cumulative_count', 'rate_14_day', 'weekly_count'], axis = 1)
    #merge
    df_cases_top = pd.merge(df_cases_top, df_deaths, left_on='country', right_on='country', how = 'left', indicator=False)
    #calculate tax_deaths
    df_cases_top['tax_deaths'] = round((df_cases_top['weekly_count_deaths']/df_cases_top['weekly_count'])*100,2)
    return df_deaths, df_cases_top
