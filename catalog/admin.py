from django.contrib import admin
from .models import DoorSpec


@admin.register(DoorSpec)
class DoorSpecAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
