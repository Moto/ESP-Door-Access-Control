ESP32 Door Access Control System - Setup Instructions
This guide provides step-by-step instructions to deploy your door access control system, using the code you've saved in your GitHub repository.
System Components
 * ESP32 Firmware (Arduino C++): Runs on the ESP32, connects to Wi-Fi, hosts a web server, and controls the relay. (Your ESP32_Firmware.ino file).
 * Python Application (on your computer): Handles PIN-based employee authentication, manages employee data in an SQLite database, and sends commands to the ESP32 via HTTP. (Your Access_Control_App.py file).
Part 1: ESP32 Hardware & Software Setup
This section covers setting up your Arduino IDE and uploading the firmware to your ESP32.
Step 1: Set Up Arduino IDE for ESP32
If you haven't already, configure your Arduino IDE to work with ESP32 boards:
 * Download Arduino IDE: If you don't have it, download and install the latest version from arduino.cc.
 * Add ESP32 Board Manager URL:
   * Open Arduino IDE.
   * Go to File > Preferences (or Arduino > Preferences on macOS).
   * In the "Additional Boards Manager URLs:" field, add the following URL:
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

   * If you have other URLs, separate them with a comma.
   * Click "OK."
 * Install ESP32 Boards:
   * Go to Tools > Board > Boards Manager...
   * In the Boards Manager, search for "esp32".
   * Select "esp32 by Espressif Systems" and click "Install."
 * Select Your ESP32 Board:
   * Go to Tools > Board > ESP32 Arduino.
   * Select your specific ESP32 board model (e.g., "ESP32 Dev Module").
 * Select the COM Port:
   * Connect your ESP32 board to your computer via USB.
   * Go to Tools > Port.
   * Select the COM port that corresponds to your ESP32 (e.g., COM3 on Windows, /dev/ttyUSB0 or /dev/tty.usbserial-XXXX on macOS/Linux).
Step 2: Prepare ESP32 Firmware
 * Open ESP32_Firmware.ino: Locate and open the ESP32_Firmware.ino file from your GitHub repository in the Arduino IDE.
 * Customize Wi-Fi Credentials:
   * In the code, find the lines:
     const char* ssid = "YOUR_WIFI_SSID";         // REPLACE with your Wi-Fi network name
const char* password = "YOUR_WIFI_PASSWORD"; // REPLACE with your Wi-Fi password

   * REPLACE "YOUR_WIFI_SSID" and "YOUR_WIFI_PASSWORD" with your actual Wi-Fi network name and password.
 * Confirm RELAY_PIN:
   * Check this line: const int RELAY_PIN = 2;
   * Ensure that 2 (or whatever number is there) matches the GPIO pin on your ESP32 to which you will connect your relay module's signal pin.
Step 3: Wire the Relay
Before uploading, ensure your relay is properly wired to the ESP32:
 * Relay VCC: Connect to ESP32's 5V pin (or 3.3V, depending on your relay module's voltage requirement – check your relay's datasheet).
 * Relay GND: Connect to ESP32's GND pin.
 * Relay IN (or Signal): Connect to the ESP32's RELAY_PIN (e.g., GPIO 2, as defined in your code).
 * Door Lock/Mechanism: Wire the relay's COM (Common), NO (Normally Open), and NC (Normally Closed) terminals to your door locking mechanism.
   * For a typical "fail-secure" magnetic lock (locks when power is removed, unlocks when power applied), you'd usually connect the lock's power wire to NO and the power supply to COM.
   * Always be careful when wiring mains voltage. For testing, consider using a low-voltage LED or buzzer instead of a real lock.
Step 4: Upload ESP32 Firmware and Note IP Address
 * Upload the Code: With your ESP32 connected and the correct board/port selected in Arduino IDE, click the "Upload" button (the right arrow icon).
   * Troubleshooting: If the upload fails (e.g., "Failed to connect"), try pressing and holding the "BOOT" button on your ESP32 when the Arduino IDE starts uploading, then release it once you see "Connecting...".
 * Note IP Address: After a successful upload, open the "Serial Monitor" (Tools > Serial Monitor or Ctrl+Shift+M) and set the baud rate to 115200. Your ESP32 will connect to Wi-Fi and print its assigned IP Address. Write this IP address down! You will need it for the Python application.
Part 2: Python Application Setup & Execution
This section covers preparing and running your Python access control application.
Step 1: Install Python Libraries
 * Install requests: If you haven't already, open your terminal or command prompt (e.g., Command Prompt on Windows, Terminal on macOS/Linux) and run:
   pip install requests

 * sqlite3 is built-in: You don't need to install anything for SQLite as it comes with Python.
Step 2: Prepare Python Application
 * Locate Access_Control_App.py: Navigate to the folder where you have cloned your GitHub repository and find the Access_Control_App.py file.
 * Edit ESP32_IP_ADDRESS: Open Access_Control_App.py in a text editor (like VS Code, Sublime Text, Notepad++, or even a basic text editor).
   * Find the line:
     ESP32_IP_ADDRESS = "YOUR_ESP32_IP_ADDRESS" # e.g., "192.168.1.105"

   * CRUCIALLY, REPLACE "YOUR_ESP32_IP_ADDRESS" with the actual IP address you noted from your ESP32's serial monitor. For example:
     ESP32_IP_ADDRESS = "192.168.1.105"

   * Save the file after making this change.
Step 3: Run the Python Application
 * Open Terminal/Command Prompt: Navigate to the directory where your Access_Control_App.py file is located.
 * Run the application: Execute the script using Python:
   python Access_Control_App.py

Step 4: Test the Complete System
 * Initial Run: When you run the Python app for the first time, it will initialize the SQLite database. A file named door_access.db will be created in the same directory as your Python script. It will also add a default admin user (PIN: 1234) to the database if it doesn't already exist.
 * Test Access:
   * From the main menu, choose option 1 (Enter PIN).
   * Enter the admin PIN 1234.
   * You should see "Access granted!" in the terminal, and your ESP32's relay should activate briefly. If you have the Arduino IDE Serial Monitor open, you'll also see "Door opening..." and "Door closed." messages.
   * Try entering an invalid PIN to confirm "Access denied."
 * Test Admin Features (for persistence):
   * From the main menu, choose option 2 (Admin Options).
   * Enter the admin PIN 1234.
   * Choose 1 (Add New Employee) to add new employees with unique 4-digit PINs, names, and IDs.
   * Choose 3 (View Employees) to see all registered employees (including the ones you just added).
   * Choose 2 (Delete Employee) to remove an employee by their PIN.
 * Verify Data Persistence:
   * Close the Python application.
   * Run the Python application again.
   * Try using the PINs of the employees you added previously. You'll find that they are still there because the data is now saved in the door_access.db file.
You now have your complete ESP32-based door access control system up and running with persistent data!
