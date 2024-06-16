from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Certification(models.Model):
    name = models.CharField(max_length=10, unique=True)


class Director(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Star(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Movie(models.Model):
    name = models.CharField(max_length=250)
    year = models.IntegerField()
    time = models.IntegerField()
    rating = models.FloatField()
    meta_score = models.FloatField(blank=True, null=True)
    gross = models.FloatField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='movies')
    certification = models.ForeignKey(Certification, on_delete=models.PROTECT, related_name='movies')
    director = models.ManyToManyField(Director, related_name='movies')
    stars = models.ManyToManyField(Star, related_name='movies')
    description = models.TextField()
