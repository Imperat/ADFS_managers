from django.db import models
from datetime import datetime
# Create your models here.

class Player (models.Model):
    firstName = models.CharField(max_length=70)
    lastName = models.CharField(max_length=70)
    birth = models.DateField()
    vkLink = models.CharField(max_length=30)
    # G - goalkeeper, H - defender, F - nap
    basePosition = models.CharField(max_length=1)
    image = models.ImageField(upload_to="media")
    history = models.ManyToManyField('Team', through='RecOfTeam')

    def __unicode__(self):
        return unicode(self.firstName + " " + self.lastName)

class Team(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    foundation = models.IntegerField()
    image = models.ImageField(upload_to="media")
    players = models.ManyToManyField('Player', through='RecOfTeam')
    vkLink = models.CharField(max_length=30, default="null")
    captain = models.OneToOneField('Player', related_name='+', default=Player())
    # And list of players!

    def __unicode__(self):
        return unicode(self.name)

class RecOfTeam(models.Model):
    beginDate = models.DateField(default=datetime.now())
    endDate = models.DateField(default=datetime.now())
    team = models.ForeignKey('Team')
    player = models.ForeignKey('Player')

    def __unicode__(self):
        return self.player.__unicode__() + " (" + self.team.__unicode__() + ")"

    def get_end_date(self):
        if self.endDate.year > datetime.now().year:
            return u"At our time"
        else:
            return self.endDate

