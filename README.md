# ESP-Door-Access-Control

A straightforward, PIN-based door access control system designed for small businesses or personal use. It combines a Python application for user management and authentication with an ESP32 microcontroller for physical door actuation.

## Features

* **PIN-Based Access:** Grant or deny door access using a 4-digit PIN.
* **Persistent Employee Data:** All employee PINs, names, and IDs are securely stored in an SQLite database, ensuring data persists across application restarts.
* **Physical Door Control:** An ESP32 board, connected to a relay, receives commands from the Python application to physically unlock a door or trigger any connected device.
* **Admin Panel:** A command-line interface for administrators to easily manage employee records (add, delete, view).

## How It Works

The system operates in two main parts:

1.  **Python Application (Host PC):**
    * Acts as the central management and authentication hub.
    * Provides a command-line interface for users to enter PINs and for administrators to manage employee data (stored in `door_access.db`).
    * Upon successful PIN authentication, it sends an HTTP GET request (e.g., `http://<ESP32_IP_ADDRESS>/open_door`) to the ESP32.

2.  **ESP32 Firmware (Microcontroller):**
    * Runs on an ESP32 development board, connected to your local Wi-Fi network.
    * Hosts a lightweight web server that listens for incoming commands.
    * When it receives the `/open_door` request from the Python app, it momentarily activates a connected relay module, which can be wired to an electronic door lock, gate, or other access device.

## Getting Started

To set up and run this project, you will need:

### Hardware
* ESP32 Development Board
* USB Cable for ESP32
* 1-Channel Relay Module
* Electronic Door Lock / Gate / Test LED (and appropriate power supply if using a lock)

### Software
* Python 3.x
* Arduino IDE (with ESP32 board definitions)
* `requests` Python library (`pip install requests`)

## Installation and Setup Instructions

For detailed steps on how to set up your ESP32 (wiring, firmware upload) and configure the Python application, please refer to the comprehensive `SETUP_GUIDE.md` (or similar detailed document) or follow the guided instructions provided during development.

**Key steps include:**
1.  Flashing `ESP32_Firmware.ino` to your ESP32 after configuring your Wi-Fi credentials.
2.  Wiring your relay to the specified GPIO pin on the ESP32.
3.  Updating the `ESP32_IP_ADDRESS` variable in `Access_Control_App.py` with the actual IP address of your ESP32.
4.  Running the `Access_Control_App.py` to initialize the SQLite database and start the system.

## Usage

Once running:

* **Access Door:** Enter `1` at the main menu and then your 4-digit PIN.
* **Admin Access:** Enter `2` at the main menu and use the default admin PIN (`1234`) to manage employees.

---
