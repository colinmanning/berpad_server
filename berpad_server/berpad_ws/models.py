from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

'''
An Event represents something of interest to an audience that takes place over a time period at a Venue
'''
class Event(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False, unique=False, default='',
                            help_text='a title that will clearly identify what is happenning at the event')
    description = models.CharField(max_length=200, blank=True, null=True, unique=False, default='',
                              help_text='more information about the event')

    def __str__(self):
        return self.title