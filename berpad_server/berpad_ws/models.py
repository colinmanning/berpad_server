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
A Venue represents a place where events happen
'''
class Sport(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True, default='',
                            help_text='sport name')
    def __str__(self):
        return self.name

'''
A Venue represents a place where events happen
'''
class Venue(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=False, default='',
                            help_text='the venue name')
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
