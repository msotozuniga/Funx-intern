from django.db import models


# Create your models here.

class Team(models.Model):
    slug = models.SlugField(max_length=200)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=80)
    image = models.FileField(upload_to='team')

    def __str__(self):
        return self.name


class Stadium(models.Model):
    slug = models.SlugField(max_length=200)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Championship(models.Model):
    slug = models.SlugField(max_length=200)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Referee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    slug = models.SlugField(max_length=200)
    championship = models.ForeignKey(Championship, on_delete=models.SET_NULL, null=True)
    referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, null=True)
    match_date = models.DateTimeField()
    duration = models.FloatField()
    period = models.CharField(max_length=50)
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.slug


class MatchData(models.Model):
    characteristics = models.CharField(max_length=100)
    status = models.CharField(max_length=50, null=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.match.slug + ' - Data'


class State(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.match.slug + ' - State'


class Action(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100)
    icon = models.FileField(upload_to='action')
    url = models.URLField()

    def __str__(self):
        return self.match.slug + ' - Action ' + str(self.pk)


class Score(models.Model):
    local = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='local')
    away = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='away')
    local_goals = models.IntegerField()
    local_penalty = models.IntegerField()
    away_goals = models.IntegerField()
    away_penalty = models.IntegerField()
    score_s = models.CharField(max_length=50)
    match = models.OneToOneField(Match, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.match.slug + ' - Score'
