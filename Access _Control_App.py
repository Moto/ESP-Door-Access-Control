import requests
import time
import sqlite3 # Import the SQLite library

# --- Configuration for ESP32 (remains the same) ---
# IMPORTANT: Replace with the actual IP address of your ESP32!
ESP32_IP_ADDRESS = "YOUR_ESP32_IP_ADDRESS" # e.g., "192.168.1.105"
DOOR_OPEN_URL = f"http://{ESP32_IP_ADDRESS}/open_door"

# --- Database Configuration ---
DB_NAME = 'door_access.db' # The name of your SQLite database file

# --- Admin PIN (for accessing admin menu) ---
# This is hardcoded for simplicity. In a real system, admin users would have their own login.
ADMIN_PIN = "1234"

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def initialize_database():
    """
    Connects to the database and creates the 'employees' table if it doesn't exist.
    Inserts a default admin employee if the table is empty.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            pin TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL
        )
    ''')

    # Check if the admin PIN exists, if not, add it
    cursor.execute("SELECT COUNT(*) FROM employees WHERE pin = ?", (ADMIN_PIN,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO employees (pin, name, employee_id) VALUES (?, ?, ?)",
                       (ADMIN_PIN, "Admin User", "AD001"))
        print(f"Default admin user (PIN: {ADMIN_PIN}) added to the database.")

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized successfully.")

# --- ESP32 Communication (remains the same) ---
def open_door_via_esp32():
    """
    Sends an HTTP GET request to the ESP32 to trigger the door opening.
    """
    print(f"Attempting to open door via ESP32 at: {DOOR_OPEN_URL}")
    try:
        response = requests.get(DOOR_OPEN_URL, timeout=5) # 5-second timeout
        if response.status_code == 200:
            print("Successfully sent 'open door' command to ESP32.")
            print(f"ESP32 response: {response.text}")
            print("Door should now be opening for a few seconds.")
        else:
            print(f"Error sending command to ESP32. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to ESP32 at {ESP32_IP_ADDRESS}. Is it on and connected to Wi-Fi?")
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Employee Database Operations (New/Modified) ---

def authenticate_pin(pin):
    """
    Authenticates an employee based on a 4-digit PIN from the database.

    Args:
        pin (str): The 4-digit PIN to check.

    Returns:
        dict or None: Dictionary containing employee details if authentication is successful,
                      None otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pin, name, employee_id FROM employees WHERE pin = ?", (pin,))
    employee = cursor.fetchone() # Fetch one row
    conn.close()

    if employee:
        return {"pin": employee['pin'], "name": employee['name'], "id": employee['employee_id']}
    return None

def add_employee(pin, name, employee_id):
    """
    Adds a new employee record to the database.

    Returns:
        bool: True if successful, False otherwise (e.g., PIN or ID already exists).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO employees (pin, name, employee_id) VALUES (?, ?, ?)",
                       (pin, name, employee_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        # This error occurs if PIN (PRIMARY KEY) or employee_id (UNIQUE) already exists
        print(f"Database error: {e}. PIN or Employee ID might already exist.")
        return False
    finally:
        conn.close()

def delete_employee_from_db(pin):
    """
    Deletes an employee record from the database by PIN.

    Returns:
        bool: True if successful, False if PIN not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE pin = ?", (pin,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def get_all_employees():
    """
    Retrieves all employee records from the database.

    Returns:
        list of dict: A list of dictionaries, each representing an employee.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pin, name, employee_id FROM employees")
    employees = []
    for row in cursor.fetchall():
        employees.append({"pin": row['pin'], "name": row['name'], "id": row['employee_id']})
    conn.close()
    return employees

# --- Admin Menu Implementations (Modified to use DB functions) ---

def admin_add_employee():
    """
    Allows an admin to add a new employee, with database persistence.
    """
    print("\n--- Add New Employee ---")
    while True:
        new_pin = input("Enter 4-digit PIN for new employee: ").strip()
        if len(new_pin) == 4 and new_pin.isdigit():
            # Check if PIN exists in DB before asking for other details
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees WHERE pin = ?", (new_pin,))
            if cursor.fetchone()[0] > 0:
                print(f"PIN '{new_pin}' already exists. Please choose a different PIN.")
                conn.close()
            else:
                conn.close()
                break # Valid and unique PIN
        else:
            print("Invalid PIN. Please enter exactly 4 digits.")

    new_name = input("Enter employee name: ").strip()
    new_id = input("Enter employee ID: ").strip()

    if add_employee(new_pin, new_name, new_id):
        print(f"Employee '{new_name}' (ID: {new_id}, PIN: {new_pin}) added successfully to database!")
    else:
        print("Failed to add employee. PIN or Employee ID might already be in use.")


def admin_delete_employee():
    """
    Allows an admin to delete an employee by PIN, with database persistence.
    """
    print("\n--- Delete Employee ---")
    pin_to_delete = input("Enter PIN of employee to delete: ").strip()
    if pin_to_delete == ADMIN_PIN: # Prevent deleting the admin PIN
        print("Cannot delete the default admin PIN.")
        return

    if delete_employee_from_db(pin_to_delete):
        print(f"Employee with PIN '{pin_to_delete}' deleted successfully from database.")
    else:
        print(f"PIN '{pin_to_delete}' not found in database.")


def admin_view_employees():
    """
    Allows an admin to view existing registered employees from the database.
    """
    print("\n--- Registered Employees ---")
    employees = get_all_employees()
    if not employees:
        print("No employees registered.")
        return
    for emp in employees:
        print(f"PIN: {emp['pin']}, Name: {emp['name']}, ID: {emp['id']}")


# --- Main Menu Functions (unchanged logic, just calls new functions) ---
def main_menu():
    print("\n--- Door Access Control System ---")
    print("1. Enter PIN (Open Door)")
    print("2. Admin Options")
    print("3. Exit")

def admin_menu():
    print("\n--- Admin Menu ---")
    print("1. Add New Employee")
    print("2. Delete Employee")
    print("3. View Employees")
    print("4. Back to Main Menu")

# --- Main Application Loop ---
if __name__ == "__main__":
    initialize_database() # Call this once at the start to set up the DB

    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            pin = input("Enter 4-digit PIN: ").strip()
            employee_data = authenticate_pin(pin)

            if employee_data:
                print(f"Access granted for {employee_data['name']} (ID: {employee_data['id']})!")
                open_door_via_esp32()
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Access granted for {employee_data['name']} (ID: {employee_data['id']}) via PIN {pin}.")
            else:
                print("Access denied. Invalid PIN.")
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Access denied for PIN {pin}.")
            time.sleep(1)

        elif choice == '2':
            admin_pin_input = input("Enter admin PIN: ").strip()
            if admin_pin_input == ADMIN_PIN:
                while True:
                    admin_menu()
                    admin_choice = input("Enter your admin choice: ").strip()
                    if admin_choice == '1':
                        admin_add_employee()
                    elif admin_choice == '2':
                        admin_delete_employee()
                    elif admin_choice == '3':
                        admin_view_employees()
                    elif admin_choice == '4':
                        break
                    else:
                        print("Invalid admin choice. Please try again.")
            else:
                print("Incorrect admin PIN.")
            time.sleep(1)

        elif choice == '3':
            print("Exiting Door Access Control System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        time.sleep(1)
