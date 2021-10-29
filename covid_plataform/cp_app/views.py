from django.shortcuts import render
from cp_app.models import full_data, top_15_cases_deaths, continent_cases, vacination, danger_vacination,recomendations_oceania, recomendations_asia, recomendations_africa, recomendations_europe, recomendations_america,pred_1, pred_2, pred_3, pred_4, pred_5
# Create your views here.

def index(request):
    #Top 15 countries with more cases
    top_15_cases_deaths_list = top_15_cases_deaths.objects.order_by('index')
    labels_1 = []
    data_1 = []
    for i in top_15_cases_deaths_list:
        labels_1.append(i.country)
        data_1.append(i.weekly_count)

    continent_cases_list = continent_cases.objects.order_by('weekly_count')
    labels_2 = []
    data_2 = []
    for j in continent_cases_list:
        labels_2.append(j.continent)
        data_2.append(j.weekly_count)

    vacination_list = vacination.objects.order_by('people_fully_vaccinated_per_hundred').reverse()
    labels_3 = []
    data_3 = []
    data_31 = []
    for k in vacination_list:
        labels_3.append(k.country)
        data_3.append(k.people_fully_vaccinated_per_hundred)
        data_31.append(k.weekly_count)

    danger_vacination_list = danger_vacination.objects.order_by('number_days_immunity_group').reverse()
    labels_4 = []
    data_4 = []
    data_41 = []
    for k in danger_vacination_list:
        labels_4.append(k.country)
        data_4.append(k.number_days_immunity_group)
        data_41.append(k.weekly_count)

    recomendation_europe_list = recomendations_europe.objects.order_by('weekly_count')
    recomendation_america_list = recomendations_america.objects.order_by('weekly_count')
    recomendation_africa_list = recomendations_africa.objects.order_by('weekly_count')
    recomendation_asia_list = recomendations_asia.objects.order_by('weekly_count')
    recomendation_oceania_list = recomendations_oceania.objects.order_by('weekly_count')

    return render(request, 'cp_app/index.html', {'index_id':top_15_cases_deaths_list, 'labels_1':labels_1, 'data_1':data_1, 'labels_2':labels_2, 'data_2':data_2 , 'labels_3':labels_3, 'data_3':data_3, 'data_31':data_31, 'labels_4':labels_4, 'data_4':data_4, 'data_41':data_41,'recomendation_europe':recomendation_europe_list,'recomendation_america':recomendation_america_list,'recomendation_africa':recomendation_africa_list,'recomendation_oceania':recomendation_oceania_list,'recomendation_asia':recomendation_asia_list})


# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from url_filter.filtersets import ModelFilterSet

import pandas as pd
import numpy as np
import json


class MyFilterSet(ModelFilterSet):
    class Meta(object):
        model = full_data
class HistoryView(
    APIView
):

    def get(self,request, **kwargs):
        data = dict(request.GET) #.GET("content")
        if 'daterange' in data:
            start_date = pd.to_datetime(data['daterange'][0][0:10], format="%m/%d/%Y")
            end_date = pd.to_datetime(data['daterange'][0][13:23], format="%m/%d/%Y")
        def get_queryset(self):
            queryset = full_data.objects.all()
            return queryset
        queryset = get_queryset(self)
        data_final = pd.DataFrame(list(queryset.values()))

        # get data and country values for filtering
        country_list = data_final['country'].unique()
        right_date = data_final['year_week'].unique()
        data_list = data_final['year_week'].astype(str).unique()
        data_list = pd.to_datetime(data_list)
        first_date = right_date[0]
        first_date = pd.to_datetime(first_date)
        last_date =right_date[-1]
        last_date = pd.to_datetime(last_date)

        # filter information for html
        data_final = data_final[data_final['country'].isin(data['country_selection'])]
        data_table = data_final
        if 'daterange' in data:
            data_final = data_final[data_final['year_week'] >= start_date]
        if 'daterange' in data:
            data_final = data_final[data_final['year_week'] <= end_date]
        country_graph_list = data_final['country'].unique()
        data_graph_list = data_final['year_week'].astype(str).unique()
        # determine pallete
        PALETTE = ['#fb906c', '#e2e7e7', '#94bebf', '##6d97a7', '##617e98' ]

        #create context who will save all charts
        #context['charts'] = []
        #example chart
        #city_payment_radar = Chart('radar', chart_id='city_payment_radar', palette=PALETTE)
        #city_payment_radar.from_df(df, values='total', stacks=['payment'], labels=['city'])
        #context['charts'].append(city_payment_radar.get_presentation())

        # get data for initial table
        table_dic = {}
        dictListas = {}
        dictListas_vac = {}
        for i in country_graph_list:
            data_teste = data_table[data_table['country'] == i]
            casos = data_teste['weekly_count'].mean()
            mortes = data_teste['weekly_count_deaths'].mean()
            taxa_morte = data_teste['tax_deaths'].mean()
            vac_completa = data_teste['people_fully_vaccinated_per_hundred'].max()
            vac_meia = data_teste['people_vaccinated_per_hundred'].max()
            table_dic[i] = {'casos': casos, 'mortes': mortes, 'taxa_morte': taxa_morte, 'vac_completa': vac_completa, 'vac_meia': vac_meia}

            # começar a tirar dados para a lista de listas
            lista = []
            aux = data_final[data_final['country']==i]
            lista = aux['weekly_count'].to_list()
            dictListas[i] = lista # cases
            # começar a tirar dados para a lista de listas das vacinas
            lista_vac = []
            aux_vac = data_final[data_final['country']==i]
            lista_vac = aux_vac['people_fully_vaccinated_per_hundred'].to_list()
            dictListas_vac[i] = lista_vac # cases
        firstdate_str = str(first_date)[0:10]
        lastdate_str = str(last_date)[0:10]
        labels_aux = data_final['year_week'].unique()
        labels_serie = []
        for x in labels_aux:
            y = str(x)[0:10]
            labels_serie.append(y)
        print(dictListas_vac)
        return render(request, 'cp_app/history.html', {'table_dic': table_dic, 'country_graph_list' : country_graph_list, 'date_graph_list' : data_graph_list, 'country_list' : country_list, 'date_list' : data_list, 'first_date' : first_date, 'last_date' : last_date, 'firstdate_str': firstdate_str, 'lastdate_str': lastdate_str, 'labels_serie':labels_serie, 'dictListas' : dictListas, 'dictListas_vac': dictListas_vac })

class SelectionView(
    APIView
):

    def get(self,request):

        def get_queryset(self):
            queryset = full_data.objects.all()
            return queryset
        queryset = get_queryset(self)
        data_final = pd.DataFrame(list(queryset.values()))
        country_list = data_final['country'].unique()
        right_date = data_final['year_week'].unique()
        data_list = data_final['year_week'].astype(str).unique()
        data_list = pd.to_datetime(data_list)
        first_date = right_date[0]#.astype(str)
        first_date = pd.to_datetime(first_date)
        last_date =right_date[-1]#.astype(str)
        last_date = pd.to_datetime(last_date)
        return render(request, 'cp_app/history_selection.html', {'country_list' : country_list, 'date_list' : data_list, 'first_date' : first_date, 'last_date' : last_date } )


#def mode(request):
#    return render(request, 'cp_app/mode.html')





def mode(request):
    pred1_list = pred_1.objects.order_by('id')
    pred2_list = pred_2.objects.order_by('id')
    pred3_list = pred_3.objects.order_by('id')
    pred4_list = pred_4.objects.order_by('id')
    pred5_list = pred_5.objects.order_by('id')
    for k in pred1_list:
        p1 = k.country
    for k in pred2_list:
        p2 = k.country
    for k in pred3_list:
        p3 = k.country
    for k in pred4_list:
        p4 = k.country
    for k in pred5_list:
        p5 = k.country

    def create_labels(pred_list):
        labels = []
        datar = []
        datat = []
        datap = []
        for k in pred_list:
            if k.year_week != None:
                labels.append(k.year_week)
            else:
                labels.append(".")
            if k.weekly_count != None:
                datar.append(k.weekly_count)
            else:
                datar.append(".")
            if k.train_predictons != None:
                datat.append(k.train_predictons)
            else:
                datat.append(".")
            if k.predictons != None:
                datap.append(k.predictons)
            else:
                datap.append(".")
        return labels, datar, datat, datap


    labels_p1, datar_p1, datat_p1, datap_p1 = create_labels(pred1_list)
    labels_p2, datar_p2, datat_p2, datap_p2 = create_labels(pred2_list)
    labels_p3, datar_p3, datat_p3, datap_p3 = create_labels(pred3_list)
    labels_p4, datar_p4, datat_p4, datap_p4 = create_labels(pred4_list)
    labels_p5, datar_p5, datat_p5, datap_p5 = create_labels(pred5_list)

    return render(request, 'cp_app/mode.html', {'pred1':pred1_list, 'pred2':pred2_list, 'pred3':pred3_list, 'pred4':pred4_list, 'pred5':pred5_list,
    'p1':p1, 'p2':p2, 'p3':p3, 'p4':p4, 'p5':p5,
    'labels_p1':labels_p1, 'datar_p1':datar_p1, 'datat_p1':datat_p1, 'datap_p1':datap_p1,
    'labels_p2':labels_p2, 'datar_p2':datar_p2, 'datat_p2':datat_p2, 'datap_p2':datap_p2,
    'labels_p3':labels_p3, 'datar_p3':datar_p3, 'datat_p3':datat_p3, 'datap_p3':datap_p3,
    'labels_p4':labels_p4, 'datar_p4':datar_p4, 'datat_p4':datat_p4, 'datap_p4':datap_p4,
    'labels_p5':labels_p5, 'datar_p5':datar_p5, 'datat_p5':datat_p5, 'datap_p5':datap_p5,
    })
