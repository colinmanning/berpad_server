from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Role, Person
from .models import Event
from .models import Club, Venue
from .models import Sport, SportFacility, SportClub, SportVenue, SportTournament, SportLeague, SportMatch

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berlin_ws'
        model = Role
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')

class PersonSerializer(UserSerializer):
   class Meta:
        app_label = 'berlin_ws'
        model = Person
        fields = ('user', 'username', 'role', 'full_name', 'avatar', 'photo', 'global_id')


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

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = Sport
        fields = ('id', 'name', 'code', )

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = Club
        fields = ('id', 'name', 'code', 'short_name', 'crest', )

class VenueCategorySerializer(serializers.ModelSerializer):
    fields = ('name', 'code', )


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = Venue
        fields = ('id', 'name', 'code', 'category', 'longitude', 'latitude', 'indoor', 'outdoor', 'capacity_seating', 'capacity_standing', 'capacity_max', )

class SportVenueSerializer(VenueSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = SportVenue
        fields = ('id', 'name', 'code', 'category', 'longitude', 'latitude', 'indoor', 'outdoor', 'facilities', )

class SportFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = SportFacility
        fields = ('id', 'name', )

class SportClubSerializer(ClubSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = SportClub
        fields = ('id', 'name', 'code', 'short_name', 'crest', 'sports', )

class SportTournamentSerializer(EventSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = SportTournament
        fields = ('id', 'sports', )

class SportMatchSerializer(EventSerializer):
    class Meta:
        app_label = 'berpad_ws'
        model = SportMatch
        fields = ('id', 'sport', )
