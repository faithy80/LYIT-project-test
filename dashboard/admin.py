from django.contrib import admin
from .models import TempHistory
from .models import SiteSettings


class TempHistortyAdmin(admin.ModelAdmin):
    readonly_fields = ('temp_date',)

# Register models in the admin dashboard
admin.site.register(TempHistory, TempHistortyAdmin)
admin.site.register(SiteSettings)
