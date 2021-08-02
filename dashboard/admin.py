from django.contrib import admin
from .models import TempHistory


class TempHistortyAdmin(admin.ModelAdmin):
    readonly_fields = ('temp_date',)

admin.site.register(TempHistory, TempHistortyAdmin)
