import pandas as pd
import numpy as np
import requests
import os

def cases(df_cases_deaths_rate):
    #Delete Columns
    df_cases_deaths_rate = df_cases_deaths_rate.drop(['source'], axis=1)
    #more recent week
    week = max(df_cases_deaths_rate['year_week'])

    df_cases_deaths_rate = df_cases_deaths_rate[df_cases_deaths_rate['year_week'] == week]
    #Filter Dataset Cases
    df_cases = df_cases_deaths_rate[df_cases_deaths_rate['indicator']=='cases']
    # create continentes
    df_cases_continent = df_cases[df_cases['country_code'].isna()]
    df_cases_continent = df_cases_continent[df_cases_continent['country']!='EU/EEA (total)']
    #remove continentes
    df_cases = df_cases[df_cases['country_code'].notna()]
    #group_by cases
    df_cases_top = df_cases.drop(['country_code', 'indicator', 'year_week'], axis = 1)
    df_cases_top = df_cases_top.sort_values('weekly_count', ascending=False).head(15).reset_index()
    df_cases_top = df_cases_top.drop(['index'], axis = 1)
    return df_cases_top, df_cases_deaths_rate, df_cases, df_cases_continent
