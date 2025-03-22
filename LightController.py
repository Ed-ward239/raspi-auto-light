import os
import time
from datetime import datetime

# Function to toggle USB power
def toggle_usb_power(state):
    if state == "off":
        os.system("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind")
        print(f"[{datetime.now()}] USB ports turned OFF")
    elif state == "on":
        os.system("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind")
        print(f"[{datetime.now()}] USB ports turned ON")
    else:
        print(f"[{datetime.now()}] Invalid state: {state}")

# Function to determine if USB power should be off
def should_turn_off(hour):
    # Actual Time Logic: Turn off between 9-18 and 21-6
    if (9 <= hour < 18) or (21 <= hour or hour < 6):
        return True
    return False

# Test Mode
def test_mode():
    print(f"[{datetime.now()}] Running in TEST MODE")
    for hour in range(0, 24):
        if should_turn_off(hour):
            print(f"[{datetime.now().replace(hour=hour)}] Turning USB OFF")
        else:
            print(f"[{datetime.now().replace(hour=hour)}] Turning USB ON")

# Main Control Loop
def run_control():
    while True:
        now = datetime.now()
        hour = now.hour

        if should_turn_off(hour):
            toggle_usb_power("off")
        else:
            toggle_usb_power("on")

        # Sleep for 1 minute before re-checking
        time.sleep(60)

# Run Test Mode or Actual Control
if __name__ == "__main__":
    mode = input("Enter 'test' for test mode or 'run' for actual mode: ").strip().lower()
    if mode == "test":
        test_mode()
    elif mode == "run":
        run_control()
    else:
        print("Invalid input. Please enter 'test' or 'run'.")
