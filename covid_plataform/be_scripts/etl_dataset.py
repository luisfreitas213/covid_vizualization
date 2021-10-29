import pandas as pd
import numpy as np
import requests
import os

def create_dataset():
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
    #Delete Columns
    df_cases_deaths_rate = df_cases_deaths_rate.drop(['source'], axis=1)
    #Filter Dataset Cases
    df_cases = df_cases_deaths_rate[df_cases_deaths_rate['indicator']=='cases']
    #Filter Dataset Deaths
    df_deaths = df_cases_deaths_rate[df_cases_deaths_rate['indicator']=='deaths']

    df_join = df_deaths
    df_join['ID'] = df_join['country']+df_join['year_week']
    df_join = df_join.drop(['year_week','country','indicator','country_code','continent'
                        ,'population','rate_14_day'], axis=1)

    df_join = df_join.rename(columns={'weekly_count': 'week_deaths'
                                  ,'cumulative_count':'cumulative_deaths'})
    df_model = df_cases

    df_model['ID'] = df_model['country']+df_model['year_week']
    df_model = pd.merge(df_model,df_join, left_on='ID', right_on = 'ID', how='left', indicator=False)
    df_model = df_model.drop(['ID'], axis=1)
    return df_model
