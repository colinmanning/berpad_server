from django.contrib import admin

from .models import Role, Person
from .models import Event
from .models import Venue, VenueCategory
from .models import Club
from .models import Sport, SportClub, SportVenue, SportFacility

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    fields = ( 'name', )

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ('user', 'role', 'avatar', 'photo', 'global_id', )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'venue', 'start_time', 'end_time', )

@admin.register(VenueCategory)
class VenueCategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'code',)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    fields = ('name', 'code', 'category', 'longitude', 'latitude', 'indoor', 'outdoor', 'capacity_seating', 'capacity_standing', 'capacity_max' ,)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    fields = ('name', 'code', )

@admin.register(SportFacility)
class SportFacilityAdmin(admin.ModelAdmin):
    fields = ('name', )

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name', 'code', 'crest', )

@admin.register(SportClub)
class SportClubAdmin(admin.ModelAdmin):
    fields = ('name', 'short_name', 'code', 'crest', 'sports', )

@admin.register(SportVenue)
class SportVenueAdmin(admin.ModelAdmin):
    fields = ('name', 'code', 'category', 'longitude', 'latitude', 'indoor', 'outdoor', 'facilities', 'capacity_seating', 'capacity_standing', 'capacity_max', )
