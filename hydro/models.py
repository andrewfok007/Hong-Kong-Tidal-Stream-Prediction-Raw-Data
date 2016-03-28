from django.db import models

# Hydro database model for sstoring tidal data

class Hydro(models.Model):
    mode = models.TextField()
    date = models.DateTimeField()
    prediction_interval = models.IntegerField()
    knots = models.FloatField()
    degree = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
