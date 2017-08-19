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
A Role represents groupings of Persons in the system. Roles can be used to group features and permissions for individual system users.
'''
class Role(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True, default='', help_text='the role name, must be unique sysytem wide')

    def __str__(self):
        return self.name

'''
A Person represents someone who interacts with the system. A person can have different roles within the system
'''
class Person(models.Model):
    user = models.ForeignKey(User, default=-1, related_name='user', on_delete=models.PROTECT,
                             help_text='the actual database user object managing the persons password and other details')
    role = models.ManyToManyField(Role, related_name='people',
                                  help_text='A person can have a number of different roles in the system, controlling possible options available')

    global_id = models.CharField(max_length=16, null=True, blank=True, unique=False, default='', help_text='a global id for the person across systems')
    avatar = models.ImageField(help_text='small image to use in social media etc', blank='True', null=True)
    photo = models.ImageField(help_text='photo',blank='True', null=True)

    """ the person's full name, based on the first and last name stored in the related user object """
    def full_name(self):
        return ('%s %s') % (self.user.first_name, self.user.last_name, )

    def email(self):
        return self.user.email

    def username(self):
        return self.user.username

    def __str__(self):
        if self.user is not None:
            return self.user.email
        else:
            return models.Model.__str__


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
    name = models.CharField(max_length=50, blank=False, null=False, unique=True, default='',
                            help_text='sport name')
    code = models.CharField(max_length=6, blank=False, null=False, unique=True, default='',
                            help_text='unique code for the sport')
    def __str__(self):
        return self.name

'''
A VenueCategory represents a type of venue, e.g. Theathre, Pub, Restaraunt
'''
class VenueCategory(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True, default='',
                            help_text='the venue category name')
    code = models.CharField(max_length=6, blank=False, null=False, unique=True, default='',
                            help_text='unique code for the veue category')

    def __str__(self):
        return ('%s (%s)') % (self.name, self.code, )


'''
A Venue represents a place where events happen
'''
class Venue(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=False, default='',
                            help_text='the venue name')
    code = models.CharField(max_length=6, blank=False, null=False, unique=True, default='',
                            help_text='unique code for the venue')
    longitude = models.FloatField(default=0.0, null=False, unique=False, help_text='gps longitude')
    latitude = models.FloatField(default=0.0, null=False, unique=False, help_text='gps longitude')
    indoor = models.BooleanField(default = False, help_text="has indoor facilities")
    outdoor = models.BooleanField(default = False, help_text="has outdoor facilities")
    category = models.ForeignKey(VenueCategory, default=-1, related_name='category_venues', on_delete=models.PROTECT,
                             help_text='the category of venue')
    capacity_seating = models.IntegerField(default=0, null=False, unique=False, help_text='maximum seating capacity')
    capacity_standing = models.IntegerField(default=0, null=False, unique=False, help_text='maximum standing capacity')
    capacity_max = models.IntegerField(default=0, null=False, unique=False, help_text='maximum capacity (combined standing and seating)')

    def __str__(self):
        return '%s (%s)' % (self.name, self.code, )

'''
A SportVenue represents a Venue with sporting facilities
'''
class SportVenue(Venue):
    facilities = models.ManyToManyField(SportFacility, related_name='sportfacility_sportvenues',
                                  help_text='The sport facilities available at the sport venue')
    def __str__(self):
        return '%s (%s)' % (self.name, self.code,)


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
    flyer = models.FileField(help_text='A document that is a flyer advertising the event', null=True)

    venue = models.ForeignKey(Venue, default=-1, unique=False, db_constraint=False, related_name='venue_events', on_delete=models.PROTECT, )

    def __str__(self):
        return self.title

'''
A club encapsulates any type of club, and in general serves as a sub class for specific types of clubs
'''
class Club(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True, default='',
                            help_text='club name')
    code = models.CharField(max_length=6, blank=False, null=False, unique=True, default='',
                            help_text='unique code for the club')
    short_name = models.CharField(max_length=30, blank=False, null=False, unique=True, default='',
                            help_text='a short name for the club, used in fixture lists etc')
    crest = models.ImageField(help_text='club crest/logo', null=True)

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
A Festival is collection of events taking place over a period
'''
class Festival(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True, default='',
                            help_text='festival name')
    description = models.CharField(max_length=200, blank=True, null=True, unique=False, default='',
                              help_text='more information about the festival')
    start_time = models.DateTimeField(null=True, help_text='Festival starts at')
    end_time = models.DateTimeField(null=True, help_text='Festival ends at')

    def __str__(self):
        return self.name

'''
A SportTournament is a Festival with sporting events
'''
class SportTournament(Festival):
    sports = models.ManyToManyField(Sport, related_name='sport_sporttournaments',
                                  help_text='The sports involved in the tournament')
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
An SportOfficial is person responsible for organising aspects of a sports event, for example a referee
'''
class SportOfficial(Person):
    sports = models.ManyToManyField(Sport, related_name='sport_sportofficials',
                                  help_text='The sports at which the official is qualified to officiate')

'''
A SportMatch is an event that usually involves 2 teams, and may be part of a tournament, league or just standalong event
'''
class SportMatch(Event):
    sport = models.ForeignKey(Sport, default=-1, related_name='sport_matches', on_delete=models.PROTECT,
                             help_text='the sport being played in the match')

    def __str__(self):
        return self.title
