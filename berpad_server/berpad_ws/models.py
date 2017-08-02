from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import traceback

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

'''
A SportFacility is a set of sports capabilities. A SportsVenue will have one or more sports facilities, such as runing track, gym, playing field etc.
'''
class SportFacility(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True, default='',
                            help_text='sport facility name')
    def __str__(self):
        return self.name

'''
A Sport encapsulates all things related to a sporting activity, including rules etc.
A Sports event will link to a Sport
'''
class Sport(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True, default='',
                            help_text='sport name')
    def __str__(self):
        return self.name

'''
A SportFacility represents a available facilities, such as football pitch, running track, gym etc.
'''
class SportFacility(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=False, default='',
                            help_text='the facility name')
    def __str__(self):
        return self.name

'''
A Venue represents a place where events happen
'''
class Venue(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=False, default='',
                            help_text='the venue name')
    longitude = models.FloatField(default=0.0, null=False, unique=False, help_text='gps longitude')
    latitude = models.FloatField(default=0.0, null=False, unique=False, help_text='gps longitude')
    indoor = models.BooleanField(default = False, help_text="has indoor facilities")
    outdoor = models.BooleanField(default = False, help_text="has outdoor facilities")

    def __str__(self):
        return self.name

'''
A SportVenue represents a Venue with sporting facilities
'''
class SportVenue(Venue):
    facilities = models.ManyToManyField(SportFacility, related_name='sportfacility_sportvenues',
                                  help_text='The sport facilities available at the sport venue')
    def __str__(self):
        return self.name

'''
An Event represents something of interest to an audience that takes place over a time period at a Venue
'''
class Event(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False, unique=False, default='',
                            help_text='a title that will clearly identify what is happenning at the event')
    description = models.CharField(max_length=200, blank=True, null=True, unique=False, default='',
                              help_text='more information about the event')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    venue = models.ForeignKey(Venue, default=-1, unique=False, db_constraint=False, related_name='venue_events', on_delete=models.PROTECT, )

    def __str__(self):
        return self.title

'''
A club encapsulates any type of club, and in general serves as a sub class for specific types of clubs
'''
class Club(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True, default='',
                            help_text='club name')
    crest = models.ImageField(help_text='club crest/logo')

    def __str__(self):
        return self.name

'''
A SportClub is a club that engages in sporting activities
'''
class SportClub(Club):
    sports = models.ManyToManyField(Sport, related_name='sport_sportclubs',
                                  help_text='The sports on offer at this sports club')
    def __str__(self):
        return self.name

'''
An SportTournament is an event where porting games take place, often over a day or weekend for example
'''
class SportTournament(Event):
    def __str__(self):
        return self.title

'''
A SportLeague is a competition over an extender period of time where teams usually play all other teams
'''
class SportLeague(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True, default='',
                            help_text='club name')
    def __str__(self):
        return self.name

'''
A Sportmatch is an event that usually involves 2 teams, and may be part of a tournament, league or just standalong event
'''
class SportMatch(Event):

    def __str__(self):
        return self.title
