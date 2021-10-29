import pandas as pd
import numpy as np
import requests
import os

def vacination(df_vacine, df_cases):
    df_vacine['ID'] = df_vacine['location']+df_vacine['date']
    #Group by
    df_vacine_last_date = df_vacine.groupby('location',as_index=False)['ID'].max()
    df_vacine = pd.merge(df_vacine_last_date, df_vacine, left_on='ID', right_on='ID', how = 'left', indicator=False)
    df_vacine['country'] = df_vacine['location_x']
    df_vacine = df_vacine.drop(['location_x', 'location_y', 'ID', 'date'], axis = 1)
    df_vacine = pd.merge(df_vacine, df_cases, left_on = 'iso_code', right_on = 'country_code', how = 'left', indicator = False)
    df_vacine = df_vacine[df_vacine['country_y'].notna()]
    df_vacine_top_15 = df_vacine.sort_values('people_fully_vaccinated_per_hundred', ascending=False).head(201).reset_index()
    return df_vacine_top_15, df_vacine
