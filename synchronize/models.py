from django.db import models


# Create your models here.

class MatchData(models.Model):
    characteristics = models.CharField(max_length=100)


class Stadium(models.Model):
    slug = models.SlugField(max_length=200)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Championship(models.Model):
    slug = models.SlugField(max_length=200)
    name = models.CharField(max_length=100)


class Referee(models.Model):
    name = models.CharField(max_length=100)


class State(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)


class Match(models.Model):
    slug = models.SlugField(max_length=200)
    championship = models.ForeignKey(Championship, on_delete=models.SET_NULL, null=True)
    referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, null=True)
    match_date = models.DateTimeField()
    duration = models.TimeField()
    period = models.CharField(max_length=50)
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    data = models.ManyToManyField(MatchData)


class Action(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    icon = models.FileField(upload_to='action')
    url = models.URLField()


class Team(models.Model):
    slug = models.SlugField(max_length=200)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=80)
    image = models.FileField(upload_to='team')


class Score(models.Model):
    local = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='local')
    away = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='away')
    local_goals = models.IntegerField()
    local_penalty = models.IntegerField()
    away_goals = models.IntegerField()
    away_penalty = models.IntegerField()
    scorer = models.CharField(max_length=50)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
