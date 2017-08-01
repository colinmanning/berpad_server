from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Event
from .models import Club, Venue
from .models import Sport, SportFacility, SportClub, SportVenue

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

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = Venue
        fields = ('id', 'name', 'longitude', 'latitude')

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = Club
        fields = ('id', 'name', 'crest', )

class SportVenueSerializer(VenueSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = SportVenue
        fields = ('facilities')

class SportFacility(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = SportFacility
        fields = ('id', 'name', )

class SportClub(ClubSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = SportClub
        fields = ('sports', )
