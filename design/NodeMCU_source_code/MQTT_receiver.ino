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

#include <ESP8266WiFi.h>
#include <Ticker.h>
#include <AsyncMqttClient.h>

// WIFI credentials
#define WIFI_SSID "<WIFI_SSID>"
#define WIFI_PASSWORD "<WIFI_password>"

// Raspberri Pi Mosquitto MQTT Broker
#define MQTT_HOST IPAddress(192, 168, 1, 100)
#define MQTT_PORT 1883

// Relay MQTT Topics
#define MQTT_PUB_TEMP "esp/relay"

// Digital pin connected to the relay
#define PIN D6

// Setup an instance of MQTT Client
AsyncMqttClient mqttClient;
Ticker mqttReconnectTimer;

// Setup an instance of WIFI Handler
WiFiEventHandler wifiConnectHandler;
WiFiEventHandler wifiDisconnectHandler;
Ticker wifiReconnectTimer;

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
  
  // Ensure we don't reconnect to MQTT while reconnecting to Wi-Fi
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

  // Subscribe to topic
  mqttClient.subscribe(MQTT_PUB_TEMP, 2);
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

// to serve onMessage callback function
void onMqttMessage(char* topic, char* payload, AsyncMqttClientMessageProperties properties, size_t len, size_t index, size_t total) {
  // Extract message from payload
  String message="";

  for (int i=0;i<len;i++) {
    message += payload[i];
  }

  // Send feedback to Serial port
  Serial.println("Publish received.");
  Serial.print("  topic: ");
  Serial.println(topic);
  Serial.print("  qos: ");
  Serial.println(properties.qos);
  Serial.print("  dup: ");
  Serial.println(properties.dup);
  Serial.print("  retain: ");
  Serial.println(properties.retain);
  Serial.print("  len: ");
  Serial.println(len);
  Serial.print("  index: ");
  Serial.println(index);
  Serial.print("  total: ");
  Serial.println(total);
  Serial.print("  message: ");
  Serial.println(message);

  // If the received message is ON
  if (message == "ON") {
    digitalWrite(PIN, HIGH);
  }

  // If the received message is OFF
  else if (message == "OFF") {
    digitalWrite(PIN, LOW);
  }
}

// to serve onSubscribe callback function
void onMqttSubscribe(uint16_t packetId, uint8_t qos) {
  // Send feedback to Serial port
  Serial.println("Subscribe acknowledged.");
  Serial.print("  packetId: ");
  Serial.println(packetId);
  Serial.print("  qos: ");
  Serial.println(qos);
}


// Main setup
void setup() {
  // Setup Serial port
  Serial.begin(115200);
  Serial.println();

  // Setup output pin
  pinMode(PIN, OUTPUT);

  // Setup WIFI callback functions 
  wifiConnectHandler = WiFi.onStationModeGotIP(onWifiConnect);
  wifiDisconnectHandler = WiFi.onStationModeDisconnected(onWifiDisconnect);

  // Setup MQTT callback functions
  mqttClient.onConnect(onMqttConnect);
  mqttClient.onDisconnect(onMqttDisconnect);
  mqttClient.onSubscribe(onMqttSubscribe);
  mqttClient.onMessage(onMqttMessage);

  // Setup MQTT connection
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);

  // Connecting to WIFI
  connectToWifi();
}

// Main loop
void loop() {}
