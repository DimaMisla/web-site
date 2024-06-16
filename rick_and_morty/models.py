from django.db import models
from django_extensions.db.fields import AutoSlugField


class Character(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    status = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    image = models.TextField()
    url = models.TextField()


class Episode(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    air_date = models.DateField()
    episode = models.CharField(max_length=15)
    url = models.URLField()
    characters = models.ManyToManyField(Character, related_name='episodes')
