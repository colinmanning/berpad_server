from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'nectar_admin'
        model = Event
        fields = ('id', 'title', 'description', 'street_2', )
