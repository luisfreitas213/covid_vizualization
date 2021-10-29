from django.contrib import admin

# Register your models here.
from cp_app.models import top_15_cases_deaths, full_data, continent_cases, vacination, danger_vacination,recomendations_oceania, recomendations_asia, recomendations_africa, recomendations_europe, recomendations_america, pred_1, pred_2, pred_3, pred_4, pred_5

admin.site.register(top_15_cases_deaths)
admin.site.register(continent_cases)
admin.site.register(vacination)
admin.site.register(danger_vacination)
admin.site.register(recomendations_europe)
admin.site.register(recomendations_asia)
admin.site.register(recomendations_africa)
admin.site.register(recomendations_america)
admin.site.register(recomendations_oceania)
admin.site.register(pred_1)
admin.site.register(pred_2)
admin.site.register(pred_3)
admin.site.register(pred_4)
admin.site.register(pred_5)
admin.site.register(full_data)
