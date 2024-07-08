from django.db import models

class PopulationData(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    total_population = models.IntegerField()
    population_0_4 = models.FloatField()
    population_5_17 = models.FloatField()
    population_18_24 = models.FloatField()
    population_25_44 = models.FloatField()
    population_45_64 = models.FloatField()
    population_65_plus = models.FloatField()
    population_under_18 = models.FloatField()
    population_18_54 = models.FloatField()
    population_55_plus = models.FloatField()
    male_population = models.FloatField()
    female_population = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.year}"

class ElectionResult(models.Model):
    state = models.CharField(max_length=255)
    year = models.IntegerField()
    republican = models.FloatField()
    democratic = models.FloatField()
    others = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"{self.state} - {self.year}"