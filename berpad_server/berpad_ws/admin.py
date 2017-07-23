from django.contrib import admin
from .models import Event

@admin.register(Event)
class PanelAdmin(admin.ModelAdmin):
    fields = ('title', 'description',)
