from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Event
from .models import Venue
from .models import Sport

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = User
        fields = ('password', )

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = Event
        fields = ('id', 'title', 'description', 'venue', 'start_time', 'end_time', )

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = Venue
        fields = ('id', 'name', )

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = Sport
        fields = ('id', 'name', )
