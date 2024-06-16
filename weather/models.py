from django.db import models

from accounts.models import CustomUser
from weather.validators import validate_city


class City(models.Model):
    city = models.CharField(max_length=100, validators=[validate_city])
    info = models.TextField()
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.city


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ManyToManyField(CustomUser,
                                  related_name='weather')

    def __str__(self):
        return f'{self.user} - {self.city}'

