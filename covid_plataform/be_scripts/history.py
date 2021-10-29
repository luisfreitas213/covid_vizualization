import pandas as pd
import numpy as np
import requests
import os

def history():
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

    def safe_div(x,y):
        if y == 0:
            return 0
        return x / y

    # Export dataset Cases|Deads|Rate weekly
    df_cases_deaths_rate = get_data("https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/csv")
    df_vacine = get_data("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
    #Delete Columns
    df_cases_deaths_rate = df_cases_deaths_rate.drop(['source'], axis=1)
    #Filter Dataset Cases
    df_cases = df_cases_deaths_rate[df_cases_deaths_rate['indicator']=='cases']
    # create continentes
    df_cases_continent = df_cases[df_cases['country_code'].isna()]
    df_cases_continent = df_cases_continent[df_cases_continent['country']!='EU/EEA (total)']
    #remove continentes
    df_cases = df_cases[df_cases['country_code'].notna()]
    #Filter Dataset Deaths and change name columns
    df_deaths = df_cases_deaths_rate[df_cases_deaths_rate['indicator']=='deaths']
    df_deaths = df_deaths.drop(['indicator','continent','population'], axis = 1)
    df_deaths['weekly_count_deaths']=df_deaths['weekly_count']
    df_deaths['rate_14_day_deaths']=df_deaths['rate_14_day']
    df_deaths['cumulative_count_deaths']=df_deaths['cumulative_count']
    df_deaths = df_deaths.drop(['cumulative_count', 'rate_14_day', 'weekly_count'], axis = 1)

    df_deaths['concat'] = df_deaths['year_week'] + df_deaths['country_code']
    df_cases['concat'] = df_cases['year_week'] + df_cases['country_code']
    #merge
    df_final = pd.merge(df_cases, df_deaths, left_on='concat', right_on='concat', how = 'left', indicator=False)
    df_final['year_week'] = df_final['year_week_y']
    #calculate tax_deaths
    df_final['tax_deaths'] = round((df_final['weekly_count_deaths']/df_final['weekly_count'])*100,2)
    df_final['tax_deaths'] = df_final['tax_deaths'].fillna(0)


    # vaccination
    from datetime import datetime, timedelta
    #dts = pd.to_datetime(df_vacine['date'], format='%Y-%m-%d')
    #df_vacine['weekly_date'] = dts


    df_vacine['weekly_date'] = df_vacine['date']
    def transform_date(date):
        string = str(date)
        dt = datetime.strptime(string, '%Y-%m-%d')
        return dt - timedelta(days=dt.weekday())
    count = 0
    for i in df_vacine['weekly_date']:
        df_vacine.loc[count,'weekly_date'] = transform_date(i)
        count +=1
    df_vacine["weekly_date"] = pd.to_datetime(df_vacine["weekly_date"], format = "%Y-%m-%d")
    df_vacine = df_vacine.groupby(['weekly_date', 'location'], as_index=False).max()

    # add full data columns
    full_Date = df_final['year_week'].to_string(index = False, dtype="string").split('\n')
    del(full_Date[-1])
    df_final['year_week'] = full_Date
    df_final['year_week'] = df_final['year_week'] + '-1'
    df_final['year_week'] = df_final['year_week'].str.lstrip()
    df_final['year_week'] = pd.to_datetime(df_final['year_week'], format = '%Y-%W-%w')


    # merge
    df_vacine['concat'] = df_vacine["weekly_date"].astype(str) + df_vacine["iso_code"]
    df_final['concat'] = df_final['year_week'].astype(str) + df_final['country_code_x']
    df_final2 = pd.merge(df_final, df_vacine, left_on = 'concat', right_on = 'concat', how = 'left', indicator = False)
    df_final2 = df_final2[df_final2['continent'].notna()]
    #df_final2 = df_final2[df_vacine['country_y'].notna()]
    df_final2.drop(['country_code_x','weekly_date','country_code_y','indicator', 'concat'], axis = 1)
    df_final = df_final2
    #


    import pandas.io.sql as psql
    from sqlalchemy import create_engine
    engine = create_engine(r"postgresql://postgres:postgres@localhost/postgres")
    full_dataset = df_final
    c = engine.connect()
    conn = c.connection
    c.execute('drop view if exists public.full_dataset')
    c.execute('drop table if exists covid_plataform.full_dataset')
    c.execute('drop table if exists covid_plataform.df_final')
    c.execute('drop view if exists public.df_final')
    full_dataset.to_sql("df_final", engine, schema='covid_plataform')
    c.execute('''create or replace view  public.full_dataset as
    SELECT "index" as id, "index", year_week, country_x as country, continent, population, weekly_count, rate_14_day, cumulative_count, weekly_count_deaths, rate_14_day_deaths, cumulative_count_deaths, tax_deaths, total_vaccinations, people_vaccinated,
           people_fully_vaccinated, daily_vaccinations_raw,
           daily_vaccinations, total_vaccinations_per_hundred,
           people_vaccinated_per_hundred, people_fully_vaccinated_per_hundred,
           daily_vaccinations_per_million FROM covid_plataform.df_final;''')
    conn.close()
