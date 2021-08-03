from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SiteSettings, TempHistory
from .forms import SiteSettingsForm

@login_required
def dashboard(request):
    """
    Renders the dashboard page
    """

    actual_temp = TempHistory.objects.latest('temp_date')

    site_settings = SiteSettings.load()

    form = SiteSettingsForm()

    historical_temp = TempHistory.objects.all().order_by('temp_date')

    context = {
        'actual_temp': actual_temp,
        'site_settings': site_settings,
        'form': form,
        'historical_temp': historical_temp,
    }

    return render(request, 'dashboard.html', context)
