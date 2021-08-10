from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from .models import SiteSettings, TempHistory
from .forms import SiteSettingsForm
import paho.mqtt.client as mqtt


@login_required
def dashboard(request):
    """
    Renders the dashboard page
    """

    # Get the actual temperature data
    try:
        # Try to get the latest data from the database
        actual_temp = TempHistory.objects.latest('temp_date')
    
    # If there is no data in the database 
    except:
        # Set the variable to None
        # Dashboard template will handle displaying the missing data
        actual_temp = None
    
    # Get the actual site settings
    site_settings = SiteSettings.load()

    # Fill in the form with the actual site settings data
    form = SiteSettingsForm({
        'temp_limit': site_settings.temp_limit,
        'temp_offset': site_settings.temp_offset,
        'auto_mode': site_settings.auto_mode,
    })

    # Get the list of the historical temperature data in reversed date order
    historical_temp = TempHistory.objects.all().order_by('temp_date').reverse()

    # Gather the context
    context = {
        'actual_temp': actual_temp,
        'site_settings': site_settings,
        'form': form,
        'historical_temp': historical_temp,
    }

    # Render the dashboard view
    return render(request, 'dashboard.html', context)

def save_site_settings(request):
    """
    Store the site settings into the database and redirects to dashboard
    """

    # On POST request
    if request.method == 'POST':
        # Get the previous site settings
        old_settings = SiteSettings.load()

        # Create the new site settings
        new_settings = SiteSettings()
        new_settings.temp_limit = float(request.POST['temp_limit'])
        new_settings.temp_offset = float(request.POST['temp_offset'])
        
        if 'auto_mode' in request.POST:
            new_settings.auto_mode = True

        else:
            new_settings.auto_mode = False
        
        # Keep the relay state
        new_settings.relay_state = bool(old_settings.relay_state)
        
        # Store the new site settings
        new_settings.save()
    
    # Redirect to dashboard
    return redirect(reverse('dashboard'))

def relay_on(request):
    """
    Turns on the relay and redirects to dashboard
    """

    # On POST request
    if request.method == 'POST':
        # Get the previous site settings
        site_settings = SiteSettings.load()

        # Modify the relay state
        site_settings.relay_state = True

        # Store the relay state
        site_settings.save()

        # Call the helper function to publish the ON MQTT message
        mqtt_publish('esp/relay','ON')

    # Redirect to dashboard
    return redirect(reverse('dashboard'))

def relay_off(request):
    """
    Turns off the relay and redirects to dashboard
    """

    # On POST request
    if request.method == 'POST':
        # Get the previous site settings
        site_settings = SiteSettings.load()

        # Modify the relay state
        site_settings.relay_state = False

        # Store the relay state
        site_settings.save()

        # Call the helper function to publish the OFF MQTT message
        mqtt_publish('esp/relay','OFF')

    # Redirect to dashboard
    return redirect(reverse('dashboard'))

def delete_all_data(request):
    """
    Deletes all the historical temperature data from the database and redirects to dashboard
    """

    # On POST request
    if request.method == 'POST':
        # Gathers all the data and deletes them at once
        TempHistory.objects.all().delete()

    # Redirect to dashboard
    return redirect(reverse('dashboard'))

def mqtt_publish(topic, message):
    """
    Helper function to send MQTT messages to the given topics
    """
    
    # Intitialise the MQTT Client
    client = mqtt.Client()

    # Connect to the MQTT broker
    client.connect("localhost", 1883, 5)

    # Send the given message to the given topics
    client.publish(topic, message)
