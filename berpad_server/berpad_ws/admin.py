from django.contrib import admin
from .models import Event
from .models import Venue
from .models import Sport

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'venue', 'start_time', 'end_time', )

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    fields = ('name', )

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    fields = ('name', )
