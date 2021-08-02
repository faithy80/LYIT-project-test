import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")

import django
django.setup()

import paho.mqtt.client as mqtt
from dashboard.models import TempHistory
from dashboard.models import SiteSettings

# Create the default setting if not created already
SiteSettings.load()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp/dht/temperature")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    temp_data = TempHistory(temp_data=float(msg.payload))
    temp_data.save()

client = mqtt.Client(client_id="DJANGO",
                     clean_session=True, userdata=None,
                     protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
