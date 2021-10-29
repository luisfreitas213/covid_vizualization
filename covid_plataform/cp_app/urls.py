from django.conf.urls import url
from django.urls import path
from cp_app import views

urlpatterns = [url(r'^$', views.index, name = 'index'),
               url(r'^$', views.mode, name = 'mode'),
               path('history/', views.HistoryView.as_view()),
               path('select/history/', views.SelectionView.as_view()),]
