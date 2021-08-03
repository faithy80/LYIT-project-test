from django.shortcuts import redirect, render, reverse
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

    form = SiteSettingsForm({
        'temp_limit': site_settings.temp_limit,
        'temp_offset': site_settings.temp_offset,
        'auto_mode': site_settings.auto_mode,
    })

    historical_temp = TempHistory.objects.all().order_by('temp_date')

    context = {
        'actual_temp': actual_temp,
        'site_settings': site_settings,
        'form': form,
        'historical_temp': historical_temp,
    }

    return render(request, 'dashboard.html', context)

def save_site_settings(request):
    if request.method == 'POST':
        old_settings = SiteSettings.load()

        new_settings = SiteSettings()
        new_settings.temp_limit = float(request.POST['temp_limit'])
        new_settings.temp_offset = float(request.POST['temp_offset'])
        new_settings.relay_state = bool(old_settings.relay_state)
        
        if 'auto_mode' in request.POST:
            new_settings.auto_mode = True

        else:
            new_settings.auto_mode = False
        
        new_settings.save()
    
    return redirect(reverse('dashboard'))

def relay_on(request):
    if request.method == 'POST':
        site_settings = SiteSettings.load()

        site_settings.relay_state = True
        site_settings.save()
    
    return redirect(reverse('dashboard'))

def relay_off(request):
    if request.method == 'POST':
        site_settings = SiteSettings.load()

        site_settings.relay_state = False
        site_settings.save()

    return redirect(reverse('dashboard'))
