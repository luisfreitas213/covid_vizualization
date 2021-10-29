from django.db import models

# Create your models here.
class top_15_cases_deaths(models.Model):
    id = models.IntegerField(primary_key=True)
    index = models.IntegerField()
    country = models.CharField(max_length=200)
    continent = models.CharField(max_length=200)
    population = models.IntegerField()
    weekly_count = models.IntegerField()
    rate_14_day = models.FloatField()
    cumulative_count = models.IntegerField()
    weekly_count_deaths = models.IntegerField()
    rate_14_day_deaths = models.FloatField()
    cumulative_count_deaths = models.IntegerField()
    tax_deaths = models.FloatField()

    def __str__(self):
        return self.country #choose representative

    class Meta:
        managed = False # Thi
        db_table = 'top_15_cases_deaths'

# Create your models here.
class continent_cases(models.Model):
    id = models.IntegerField(primary_key=True)
    index = models.IntegerField()
    continent = models.CharField(max_length=200)
    population = models.IntegerField()
    weekly_count = models.IntegerField()
    rate_14_day = models.FloatField()
    cumulative_count = models.IntegerField()

    def __str__(self):
        return self.continent #choose representative

    class Meta:
        managed = False # Thi
        db_table = 'continent_cases'

# create model vacination
class vacination(models.Model):
        id = models.IntegerField(primary_key=True)
        index = models.IntegerField()
        country = models.CharField(max_length=200)
        total_vaccinations = models.IntegerField()
        people_vaccinated = models.IntegerField()
        people_fully_vaccinated = models.IntegerField()
        daily_vaccinations_raw = models.IntegerField()
        daily_vaccinations = models.IntegerField()
        total_vaccinations_per_hundred = models.FloatField()
        people_vaccinated_per_hundred = models.FloatField()
        people_fully_vaccinated_per_hundred = models.FloatField()
        daily_vaccinations_per_million = models.IntegerField()
        population = models.IntegerField()
        weekly_count = models.IntegerField()
        cumulative_count = models.IntegerField()

        def __str__(self):
            return self.country #choose representative

        class Meta:
            managed = False # Thi
            db_table = 'vacination'



# create model danger_vacination
class danger_vacination(models.Model):
        id = models.IntegerField(primary_key=True)
        index = models.IntegerField()
        country = models.CharField(max_length=200)
        continent = models.CharField(max_length=200)
        total_vaccinations = models.IntegerField()
        people_vaccinated = models.IntegerField()
        people_fully_vaccinated = models.IntegerField()
        daily_vaccinations_raw = models.IntegerField()
        daily_vaccinations = models.IntegerField()
        total_vaccinations_per_hundred = models.FloatField()
        people_vaccinated_per_hundred = models.FloatField()
        people_fully_vaccinated_per_hundred = models.FloatField()
        daily_vaccinations_per_million = models.IntegerField()
        population = models.IntegerField()
        weekly_count = models.IntegerField()
        cumulative_count = models.IntegerField()
        number_days_immunity_group = models.IntegerField()

        def __str__(self):
            return self.country #choose representative

        class Meta:
            managed = False # Thi
            db_table = 'danger_vacination'

# create model recomendations
class recomendations_europe(models.Model):
        id = models.IntegerField(primary_key=True)
        index = models.IntegerField()
        country = models.CharField(max_length=200)
        continent = models.CharField(max_length=200)
        iso_code = models.CharField(max_length=200)
        total_vaccinations = models.IntegerField()
        people_vaccinated = models.IntegerField()
        people_fully_vaccinated = models.IntegerField()
        daily_vaccinations_raw = models.IntegerField()
        daily_vaccinations = models.IntegerField()
        total_vaccinations_per_hundred = models.FloatField()
        people_vaccinated_per_hundred = models.FloatField()
        people_fully_vaccinated_per_hundred = models.FloatField()
        daily_vaccinations_per_million = models.IntegerField()
        population = models.IntegerField()
        weekly_count = models.IntegerField()
        cumulative_count = models.IntegerField()
        zone = models.CharField(max_length=200)

        def __str__(self):
            return self.country #choose representative

        class Meta:
            managed = False # Thi
            db_table = 'recomendations_europe'

class recomendations_america(models.Model):
        id = models.IntegerField(primary_key=True)
        index = models.IntegerField()
        country = models.CharField(max_length=200)
        continent = models.CharField(max_length=200)
        iso_code = models.CharField(max_length=200)
        total_vaccinations = models.IntegerField()
        people_vaccinated = models.IntegerField()
        people_fully_vaccinated = models.IntegerField()
        daily_vaccinations_raw = models.IntegerField()
        daily_vaccinations = models.IntegerField()
        total_vaccinations_per_hundred = models.FloatField()
        people_vaccinated_per_hundred = models.FloatField()
        people_fully_vaccinated_per_hundred = models.FloatField()
        daily_vaccinations_per_million = models.IntegerField()
        population = models.IntegerField()
        weekly_count = models.IntegerField()
        cumulative_count = models.IntegerField()
        zone = models.CharField(max_length=200)

        def __str__(self):
            return self.country #choose representative

        class Meta:
            managed = False # Thi
            db_table = 'recomendations_america'

class recomendations_asia(models.Model):
        id = models.IntegerField(primary_key=True)
        index = models.IntegerField()
        country = models.CharField(max_length=200)
        continent = models.CharField(max_length=200)
        iso_code = models.CharField(max_length=200)
        total_vaccinations = models.IntegerField()
        people_vaccinated = models.IntegerField()
        people_fully_vaccinated = models.IntegerField()
        daily_vaccinations_raw = models.IntegerField()
        daily_vaccinations = models.IntegerField()
        total_vaccinations_per_hundred = models.FloatField()
        people_vaccinated_per_hundred = models.FloatField()
        people_fully_vaccinated_per_hundred = models.FloatField()
        daily_vaccinations_per_million = models.IntegerField()
        population = models.IntegerField()
        weekly_count = models.IntegerField()
        cumulative_count = models.IntegerField()
        zone = models.CharField(max_length=200)

        def __str__(self):
            return self.country #choose representative

        class Meta:
            managed = False # Thi
            db_table = 'recomendations_asia'

class recomendations_africa(models.Model):
        id = models.IntegerField(primary_key=True)
        index = models.IntegerField()
        country = models.CharField(max_length=200)
        continent = models.CharField(max_length=200)
        iso_code = models.CharField(max_length=200)
        total_vaccinations = models.IntegerField()
        people_vaccinated = models.IntegerField()
        people_fully_vaccinated = models.IntegerField()
        daily_vaccinations_raw = models.IntegerField()
        daily_vaccinations = models.IntegerField()
        total_vaccinations_per_hundred = models.FloatField()
        people_vaccinated_per_hundred = models.FloatField()
        people_fully_vaccinated_per_hundred = models.FloatField()
        daily_vaccinations_per_million = models.IntegerField()
        population = models.IntegerField()
        weekly_count = models.IntegerField()
        cumulative_count = models.IntegerField()
        zone = models.CharField(max_length=200)

        def __str__(self):
            return self.country #choose representative

        class Meta:
            managed = False # Thi
            db_table = 'recomendations_africa'

class recomendations_oceania(models.Model):
        id = models.IntegerField(primary_key=True)
        index = models.IntegerField()
        country = models.CharField(max_length=200)
        continent = models.CharField(max_length=200)
        iso_code = models.CharField(max_length=200)
        total_vaccinations = models.IntegerField()
        people_vaccinated = models.IntegerField()
        people_fully_vaccinated = models.IntegerField()
        daily_vaccinations_raw = models.IntegerField()
        daily_vaccinations = models.IntegerField()
        total_vaccinations_per_hundred = models.FloatField()
        people_vaccinated_per_hundred = models.FloatField()
        people_fully_vaccinated_per_hundred = models.FloatField()
        daily_vaccinations_per_million = models.IntegerField()
        population = models.IntegerField()
        weekly_count = models.IntegerField()
        cumulative_count = models.IntegerField()
        zone = models.CharField(max_length=200)

        def __str__(self):
            return self.country #choose representative

        class Meta:
            managed = False # Thi
            db_table = 'recomendations_oceania'

class pred_1(models.Model):
    id = models.IntegerField(primary_key=True)
    year_week = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    weekly_count = models.IntegerField()
    train_predictons = models.IntegerField()
    predictons = models.IntegerField()
    def __str__(self):
        return self.year_week #choose representative

    class Meta:
        managed = False # Thi
        db_table = 'pred_1'

class pred_2(models.Model):
    id = models.IntegerField(primary_key=True)
    year_week = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    weekly_count = models.IntegerField()
    train_predictons = models.IntegerField()
    predictons = models.IntegerField()
    def __str__(self):
        return self.year_week #choose representative

    class Meta:
        managed = False # Thi
        db_table = 'pred_2'

class pred_3(models.Model):
    id = models.IntegerField(primary_key=True)
    year_week = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    weekly_count = models.IntegerField()
    train_predictons = models.IntegerField()
    predictons = models.IntegerField()
    def __str__(self):
        return self.year_week #choose representative

    class Meta:
        managed = False # Thi
        db_table = 'pred_3'

class pred_4(models.Model):
    id = models.IntegerField(primary_key=True)
    year_week = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    weekly_count = models.IntegerField()
    train_predictons = models.IntegerField()
    predictons = models.IntegerField()
    def __str__(self):
        return self.year_week #choose representative

    class Meta:
        managed = False # Thi
        db_table = 'pred_4'


class pred_5(models.Model):
    id = models.IntegerField(primary_key=True)
    year_week = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    weekly_count = models.IntegerField()
    train_predictons = models.IntegerField()
    predictons = models.IntegerField()
    def __str__(self):
        return self.year_week #choose representative

    class Meta:
        managed = False # Thi
        db_table = 'pred_5'



class full_data(models.Model):
    id = models.IntegerField(primary_key=True)
    index = models.IntegerField()
    year_week = models.DateField(max_length=200)
    country = models.CharField(max_length=200)
    continent = models.CharField(max_length=200)
    population = models.IntegerField()
    weekly_count = models.IntegerField()
    rate_14_day = models.FloatField()
    cumulative_count = models.IntegerField()
    weekly_count_deaths = models.IntegerField()
    rate_14_day_deaths = models.IntegerField()
    cumulative_count_deaths = models.IntegerField()
    tax_deaths = models.FloatField()
    total_vaccinations = models.IntegerField()
    people_vaccinated = models.IntegerField()
    people_fully_vaccinated = models.IntegerField()
    daily_vaccinations_raw = models.IntegerField()
    daily_vaccinations = models.IntegerField()
    total_vaccinations_per_hundred = models.FloatField()
    people_vaccinated_per_hundred = models.FloatField()
    people_fully_vaccinated_per_hundred = models.FloatField()
    daily_vaccinations_per_million = models.FloatField()


    class Meta:
        managed = False # Thi
        db_table = 'full_dataset'
    def __str__(self):
        return self.id
