#include <WiFi.h>
#include <WebServer.h>

// --- Wi-Fi Credentials ---
const char* ssid = "YOUR_WIFI_SSID";         // Replace with your Wi-Fi network name
const char* password = "YOUR_WIFI_PASSWORD"; // Replace with your Wi-Fi password

// --- Relay Pin Configuration ---
const int RELAY_PIN = 2; // Connect your relay signal pin to ESP32's GPIO 2.
                         // Ensure your relay module is properly powered and wired.

// --- Web Server Setup ---
WebServer server(80); // Create a web server object on port 80 (standard HTTP)

// --- Function to handle root URL "/" ---
void handleRoot() {
  server.send(200, "text/plain", "ESP32 Door Access Control - Ready to open door.");
}

// --- Function to handle "/open_door" URL ---
void handleOpenDoor() {
  // Activate the relay to open the door (assuming active-LOW relay, adjust if needed)
  // Most common relay modules are active-LOW, meaning LOW signal turns them ON.
  digitalWrite(RELAY_PIN, LOW); // Turn relay ON

  Serial.println("Door opening...");
  server.send(200, "text/plain", "Door command sent!");

  // Keep the door open for a short duration (e.g., 2 seconds), then close
  delay(2000); // Wait 2 seconds (2000 milliseconds)

  // Deactivate the relay to close the door
  digitalWrite(RELAY_PIN, HIGH); // Turn relay OFF
  Serial.println("Door closed.");
}

// --- Function to handle 404 Not Found errors ---
void handleNotFound() {
  server.send(404, "text/plain", "Not Found");
}

void setup() {
  Serial.begin(115200); // Initialize serial communication for debugging

  // --- Configure Relay Pin ---
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // Ensure relay is OFF by default (assuming active-LOW)

  // --- Connect to Wi-Fi ---
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // --- Configure Web Server Routes ---
  server.on("/", handleRoot);            // Handle requests to the root URL
  server.on("/open_door", handleOpenDoor); // Handle requests to /open_door
  server.onNotFound(handleNotFound);     // Handle any other undefined URLs

  // --- Start Web Server ---
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  // --- Handle incoming web requests ---
  server.handleClient();
  // Add other tasks here if needed, but keep loop short for responsiveness
}
