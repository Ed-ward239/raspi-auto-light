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

# Function to determine if USB power should be ON
def should_turn_on(hour):
    # Lights ON between 9:00 to 18:00 and 21:00 to 6:00
    if (9 <= hour < 18) or (21 <= hour or hour < 6):
        return True
    return False

# Test Mode: Interactive on/off control
def test_mode():
    print(f"[{datetime.now()}] Running in TEST MODE")
    while True:
        command = input("Type 'on' to turn on, 'off' to turn off, or 'exit' to quit: ").strip().lower()
        if command == "on":
            toggle_usb_power("on")
        elif command == "off":
            toggle_usb_power("off")
        elif command == "exit":
            print(f"[{datetime.now()}] Exiting TEST MODE")
            break
        else:
            print(f"[{datetime.now()}] Invalid command. Please type 'on', 'off', or 'exit'.")

# Run Mode: Automated control based on time
def run_mode():
    print(f"[{datetime.now()}] Running in RUN MODE")
    while True:
        now = datetime.now()
        hour = now.hour

        # Determine if the lights should be ON or OFF
        if should_turn_on(hour):
            toggle_usb_power("on")
        else:
            toggle_usb_power("off")

        # Sleep for 1 minute before checking again
        time.sleep(60)

# Main Function
if __name__ == "__main__":
    mode = input("Enter 'test' for test mode or 'run' for automated mode: ").strip().lower()
    if mode == "test":
        test_mode()
    elif mode == "run":
        run_mode()
    else:
        print(f"[{datetime.now()}] Invalid input. Please enter 'test' or 'run'.")