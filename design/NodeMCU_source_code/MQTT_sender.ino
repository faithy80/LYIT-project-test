/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp8266-nodemcu-mqtt-publish-dht11-dht22-arduino/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  This program was modified by Krisztian Buza to create the Smart Home System project.
  Date: 03 August 2021

  Original source: https://github.com/marvinroger/async-mqtt-client
*/

#include <DHTesp.h>
#include <ESP8266WiFi.h>
#include <Ticker.h>
#include <AsyncMqttClient.h>

// WIFI credentials
#define WIFI_SSID "<WIFI_SSID>"
#define WIFI_PASSWORD "<WIFI_password>"

// Raspberri Pi Mosquitto MQTT Broker
#define MQTT_HOST IPAddress(192, 168, 1, 100)
#define MQTT_PORT 1883

// Temperature MQTT Topics
#define MQTT_PUB_TEMP "esp/dht/temperature"

// Digital pin connected to the DHT sensor
#define DHTPIN D5

// Setup an instance of DHTesp sensor
DHTesp dht;

// Variables to hold sensor readings
float temp;

// Setup an instance of MQTT Client
AsyncMqttClient mqttClient;
Ticker mqttReconnectTimer;

// Setup an instance of WIFI Handler
WiFiEventHandler wifiConnectHandler;
WiFiEventHandler wifiDisconnectHandler;
Ticker wifiReconnectTimer;

/* Stores last time temperature was published &
 * defines interval at which to publish sensor readings */
unsigned long previousMillis = 0;
const long interval = 60000;

// Function for connecting to WIFI
void connectToWifi() {
  // Send feedback to Serial port
  Serial.println("Connecting to Wi-Fi...");

  // Initialise WIFI setup
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

// To serve wifiConnectHandler callback function
void onWifiConnect(const WiFiEventStationModeGotIP& event) {
  // Send feedback to Serial port
  Serial.println("Connected to Wi-Fi.");

  // Call MQTT connect function
  connectToMqtt();
}

// To serve wifiDisconnectHandler callback function
void onWifiDisconnect(const WiFiEventStationModeDisconnected& event) {
  // Send feedback to Serial port
  Serial.println("Disconnected from Wi-Fi.");
  
  // Ensure we don't reconnect to MQTT while reconnecting to WiFi
  mqttReconnectTimer.detach();
  wifiReconnectTimer.once(2, connectToWifi);
}

// Function for connecting to MQTT broker
void connectToMqtt() {
  // Send feedback to Serial port
  Serial.println("Connecting to MQTT...");

  // Connect to MQTT broker
  mqttClient.connect();
}

// To serve onConnect callback function
void onMqttConnect(bool sessionPresent) {
  // Send feedback to Serial port
  Serial.println("Connected to MQTT.");
  Serial.print("Session present: ");
  Serial.println(sessionPresent);
}

// To serve onDisconnect callback function
void onMqttDisconnect(AsyncMqttClientDisconnectReason reason) {
  // Send feedback to Serial port
  Serial.println("Disconnected from MQTT.");

  // Reconnect to MQTT broker after WIFI is reconnected
  if (WiFi.isConnected()) {
    mqttReconnectTimer.once(2, connectToMqtt);
  }
}

// To serve onPublish callback function
void onMqttPublish(uint16_t packetId) {
  // Send feedback to Serial port
  Serial.print("Publish acknowledged.");
  Serial.print("  packetId: ");
  Serial.println(packetId);
}

// Main setup
void setup() {
  // Setup Serial port
  Serial.begin(115200);
  Serial.println();

  // Setup the DHT sensor
  dht.setup(DHTPIN, DHTesp::DHT11);
  delay(250);

  // Setup WIFI callback functions 
  wifiConnectHandler = WiFi.onStationModeGotIP(onWifiConnect);
  wifiDisconnectHandler = WiFi.onStationModeDisconnected(onWifiDisconnect);

  // Setup MQTT callback functions
  mqttClient.onConnect(onMqttConnect);
  mqttClient.onDisconnect(onMqttDisconnect);
  mqttClient.onPublish(onMqttPublish);
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);

  // Connecting to WIFI
  connectToWifi();
}

// Main loop
void loop() {
  unsigned long currentMillis = millis();
  
  // Every X number of seconds (interval = 60 seconds) 
  // it publishes a new MQTT message
  if (currentMillis - previousMillis >= interval) {
    // Save the last time a new reading was published
    previousMillis = currentMillis;
    
    // New DHT sensor readings
    // Read temperature as Celsius (the default)
    temp = dht.getTemperature();
    
    // Publish an MQTT message on topic esp/dht/temperature
    uint16_t packetIdPub1 = mqttClient.publish(MQTT_PUB_TEMP, 1, true, String(temp).c_str());                            
    Serial.printf("Publishing on topic %s at QoS 1, packetId: %i ", MQTT_PUB_TEMP, packetIdPub1);
    Serial.printf("Message: %.2f \n", temp);
  }
}
