import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")

import django
# Initialise Django before starting the MQTT thread
django.setup()

import paho.mqtt.client as mqtt
from dashboard.models import TempHistory
from dashboard.models import SiteSettings
from dashboard.views import mqtt_publish

# Create the default setting if not created already
SiteSettings.load()

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    # Subscribe to the given topics
    client.subscribe("esp/dht/temperature")

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    # Fetch the actual temperature data from the MQTT message
    temp_data = TempHistory(temp_data=float(msg.payload))

    # Store the data with a timestamp in the database
    temp_data.save()

    # Get actual site settings
    site_settings = SiteSettings.load()

    # If the automatic mode is enabled
    if site_settings.auto_mode:    
        # If the relay state is OFF and the actual temperature is below the limit
        if not site_settings.relay_state and temp_data.temp_data < site_settings.temp_limit:
            # Change the relay state
            site_settings.relay_state = True

            # Store the new relay state
            site_settings.save()

            # Call the helper function to publish the ON MQTT message
            mqtt_publish('esp/relay', 'ON')

        # If the relay state is ON and the actual temperature is above the limit + the offset
        elif site_settings.relay_state and temp_data.temp_data > site_settings.temp_limit + site_settings.temp_offset:
            # Change the relay state
            site_settings.relay_state = False

            # Store the new relay state
            site_settings.save()

            # Call the helper function to publish the OFF MQTT message
            mqtt_publish('esp/relay', 'OFF')

        # In any other cases
        else:
            # Refresh relay state (resend MQTT messages to make sure that the system is alive even if the NodeMCU board was restarted)
            if site_settings.relay_state:
                # send ON MQTT message if the relay state is true in the database
                mqtt_publish('esp/relay', 'ON')
            
            else:
                # send OFF MQTT message if the relay state is false in the database
                mqtt_publish('esp/relay', 'OFF')

# Initialise MQTT Client
client = mqtt.Client(client_id="DJANGO",
                     clean_session=True, userdata=None,
                     protocol=mqtt.MQTTv311)

# Setup the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("localhost", 1883, 60)
