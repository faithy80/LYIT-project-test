import paho.mqtt.client as mqtt
from datetime import datetime

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("esp/dht/temperature")
    client.subscribe("esp/dht/humidity")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    messages = open('messages.txt', 'a')
    messages.writelines(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") +" "+ msg.topic + " " + str(msg.payload) + "\n")
    messages.close()

client = mqtt.Client(client_id="DJANGO",
                     clean_session=True, userdata=None,
                     protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
