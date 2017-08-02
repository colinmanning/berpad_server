from django.contrib import admin
from .models import Event
from .models import Venue
from .models import Sport, SportClub, SportVenue, SportFacility

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'venue', 'start_time', 'end_time', )

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    fields = ('name', )

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    fields = ('name', )

@admin.register(SportFacility)
class SportFacilityAdmin(admin.ModelAdmin):
    fields = ('name', )

@admin.register(SportClub)
class SportClubAdmin(admin.ModelAdmin):
    fields = ('name', )

@admin.register(SportVenue)
class SportVenueAdmin(admin.ModelAdmin):
    fields = ('name', )
