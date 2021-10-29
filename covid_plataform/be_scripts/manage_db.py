import pandas.io.sql as psql
from sqlalchemy import create_engine
engine = create_engine(r"postgresql://postgres:postgres@localhost/postgres")

def manage_db(df_cases_top,df_cases_continent,df_vacine_top_15 ):
    c = engine.connect()
    conn = c.connection
    c.execute('drop view if exists public.recomendations_europe')
    c.execute('drop view if exists public.recomendations_asia')
    c.execute('drop view if exists public.recomendations_america')
    c.execute('drop view if exists public.recomendations_africa')
    c.execute('drop view if exists public.recomendations_oceania')

    c.execute('drop view if exists public.top_15_cases_deaths')
    c.execute('drop table if exists covid_plataform.top_15_cases_deaths;')
    df_cases_top.to_sql("top_15_cases_deaths", engine,schema = 'covid_plataform')
    c.execute('''create or replace view  public.top_15_cases_deaths as
    SELECT "index" as id, "index", country, continent, population, weekly_count, rate_14_day, cumulative_count, weekly_count_deaths, rate_14_day_deaths, cumulative_count_deaths, tax_deaths FROM covid_plataform.top_15_cases_deaths;''')


    c.execute('drop view if exists public.continent_cases')
    c.execute('drop table if exists covid_plataform.continent_cases;')
    df_cases_continent.to_sql("continent_cases", engine, schema = 'covid_plataform')
    c.execute('''create or replace view  public.continent_cases as
    SELECT "index" as id, "index", continent, population, weekly_count, rate_14_day, cumulative_count FROM covid_plataform.continent_cases;''')

    c.execute('drop view if exists public.vacination')
    c.execute('drop view if exists public.danger_vacination')
    c.execute('drop view if exists public.recomendations')
    c.execute('drop table if exists covid_plataform.vacination')
    df_vacine_top_15.to_sql("vacination", engine, schema = 'covid_plataform')
    c.execute('''
    CREATE OR REPLACE VIEW public.vacination
    AS SELECT top_15_vaccinated.id,
        top_15_vaccinated.index,
        top_15_vaccinated.country,
        top_15_vaccinated.total_vaccinations,
        top_15_vaccinated.people_vaccinated,
        top_15_vaccinated.people_fully_vaccinated,
        top_15_vaccinated.daily_vaccinations_raw,
        top_15_vaccinated.daily_vaccinations,
        top_15_vaccinated.total_vaccinations_per_hundred,
        top_15_vaccinated.people_vaccinated_per_hundred,
        top_15_vaccinated.people_fully_vaccinated_per_hundred,
        top_15_vaccinated.daily_vaccinations_per_million,
        top_15_vaccinated.population,
        top_15_vaccinated.weekly_count,
        top_15_vaccinated.cumulative_count
        FROM ( SELECT row_number() OVER (ORDER BY t.people_fully_vaccinated_per_hundred DESC) AS id,
                t.index,
                t.country,
                t.total_vaccinations,
                t.people_vaccinated,
                t.people_fully_vaccinated,
                t.daily_vaccinations_raw,
                t.daily_vaccinations,
                t.total_vaccinations_per_hundred,
                t.people_vaccinated_per_hundred,
                t.people_fully_vaccinated_per_hundred,
                t.daily_vaccinations_per_million,
                t.population,
                t.weekly_count,
                t.cumulative_count
                FROM ( SELECT vacination.index,
                        vacination.country_y AS country,
                        vacination.total_vaccinations,
                        vacination.people_vaccinated,
                        vacination.people_fully_vaccinated,
                        vacination.daily_vaccinations_raw,
                        vacination.daily_vaccinations,
                        vacination.total_vaccinations_per_hundred,
                        vacination.people_vaccinated_per_hundred,
                        vacination.people_fully_vaccinated_per_hundred,
                        vacination.daily_vaccinations_per_million,
                        vacination.population,
                        vacination.weekly_count,
                        vacination.cumulative_count
                        FROM covid_plataform.vacination
                        WHERE vacination.people_fully_vaccinated_per_hundred IS NOT NULL) t) top_15_vaccinated
                        WHERE top_15_vaccinated.id <= 15; ''')

    c.execute('''
    CREATE OR REPLACE VIEW public.danger_vacination
    AS SELECT top_15_danger.id,
        top_15_danger.index,
        top_15_danger.country,
        top_15_danger.continent,
        top_15_danger.total_vaccinations,
        top_15_danger.people_vaccinated,
        top_15_danger.people_fully_vaccinated,
        top_15_danger.daily_vaccinations_raw,
        top_15_danger.daily_vaccinations,
        top_15_danger.total_vaccinations_per_hundred,
        top_15_danger.people_vaccinated_per_hundred,
        top_15_danger.people_fully_vaccinated_per_hundred,
        top_15_danger.daily_vaccinations_per_million,
        top_15_danger.population,
        top_15_danger.weekly_count,
        top_15_danger.cumulative_count,
        top_15_danger.number_days_immunity_group
        FROM ( SELECT row_number() OVER (ORDER BY t.number_days_immunity_group DESC) AS id,
                t.index,
                t.country,
                t.continent,
                t.total_vaccinations,
                t.people_vaccinated,
                t.people_fully_vaccinated,
                t.daily_vaccinations_raw,
                t.daily_vaccinations,
                t.total_vaccinations_per_hundred,
                t.people_vaccinated_per_hundred,
                t.people_fully_vaccinated_per_hundred,
                t.daily_vaccinations_per_million,
                t.population,
                t.weekly_count,
                t.cumulative_count,
                t.number_days_immunity_group
                FROM ( SELECT vacination.index,
                        vacination.country_y AS country,
                        vacination.continent,
                        vacination.total_vaccinations,
                        vacination.people_vaccinated,
                        vacination.people_fully_vaccinated,
                        vacination.daily_vaccinations_raw,
                        vacination.daily_vaccinations,
                        vacination.total_vaccinations_per_hundred,
                        vacination.people_vaccinated_per_hundred,
                        vacination.people_fully_vaccinated_per_hundred,
                        vacination.daily_vaccinations_per_million,
                        vacination.population,
                        vacination.weekly_count,
                        vacination.cumulative_count,
                        ((vacination.population * 0.7::double precision - vacination.people_fully_vaccinated) / (vacination.daily_vaccinations / 2::double precision))::integer AS number_days_immunity_group
                        FROM covid_plataform.vacination
                        WHERE ((vacination.population * 0.7::double precision - vacination.people_fully_vaccinated) / (vacination.daily_vaccinations / 2::double precision))::integer IS NOT NULL) t) top_15_danger
                        WHERE top_15_danger.id <= 15;''')
    c.execute('''
    CREATE OR REPLACE VIEW public.recomendations
    AS SELECT recomendations.id,
    recomendations.index,
    recomendations.country,
    recomendations.continent,
    recomendations.iso_code,
    recomendations.total_vaccinations,
    recomendations.people_vaccinated,
    recomendations.people_fully_vaccinated,
    recomendations.daily_vaccinations_raw,
    recomendations.daily_vaccinations,
    recomendations.total_vaccinations_per_hundred,
    recomendations.people_vaccinated_per_hundred,
    recomendations.people_fully_vaccinated_per_hundred,
    recomendations.daily_vaccinations_per_million,
    recomendations.population,
    recomendations.weekly_count,
    recomendations.cumulative_count,
    recomendations.zone
   FROM ( SELECT row_number() OVER (ORDER BY t.people_fully_vaccinated_per_hundred DESC) AS id,
            t.index,
            t.country,
            t.continent,
            t.iso_code,
            t.total_vaccinations,
            t.people_vaccinated,
            t.people_fully_vaccinated,
            t.daily_vaccinations_raw,
            t.daily_vaccinations,
            t.total_vaccinations_per_hundred,
            t.people_vaccinated_per_hundred,
            t.people_fully_vaccinated_per_hundred,
            t.daily_vaccinations_per_million,
            t.population,
            t.weekly_count,
            t.cumulative_count,
            t.zone
           FROM ( SELECT vacination.index,
                    vacination.country_y AS country,
                    vacination.continent,
                    vacination.iso_code,
                    vacination.total_vaccinations,
                    vacination.people_vaccinated,
                    vacination.people_fully_vaccinated,
                    vacination.daily_vaccinations_raw,
                    vacination.daily_vaccinations,
                    vacination.total_vaccinations_per_hundred,
                    vacination.people_vaccinated_per_hundred,
                    vacination.people_fully_vaccinated_per_hundred,
                    vacination.daily_vaccinations_per_million,
                    vacination.population,
                    vacination.weekly_count,
                    vacination.cumulative_count,
                        CASE
                            WHEN vacination.weekly_count > 100::double precision THEN 'red'::text
                            WHEN vacination.weekly_count <= 100::double precision AND vacination.people_fully_vaccinated_per_hundred >= 50::double precision OR vacination.weekly_count <= 50::double precision THEN 'green'::text
                            ELSE 'yellow'::text
                        END AS zone
                   FROM covid_plataform.vacination) t) recomendations;''')


    c.execute('''create view public.recomendations_europe as
    SELECT *
    FROM public.recomendations
    where zone = 'green' and continent = 'Europe';

    create view public.recomendations_america as
    SELECT *
    FROM public.recomendations
    where zone = 'green' and continent = 'America';

    create view public.recomendations_asia as
    SELECT *
    FROM public.recomendations
    where zone = 'green' and continent = 'Asia';

    create view public.recomendations_africa as
    SELECT *
    FROM public.recomendations
    where zone = 'green' and continent = 'Africa';

    create view public.recomendations_oceania as
    SELECT *
    FROM public.recomendations
    where zone = 'green' and continent = 'Oceania';''')
    conn.close()
