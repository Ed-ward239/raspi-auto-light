import RPi.GPIO as GPIO
import time
from datetime import datetime

# GPIO pin configuration
relay_pin = 17  # Use GPIO pin 17

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

# Function to turn on the power
def power_on():
    GPIO.output(relay_pin, GPIO.HIGH)
    print(f"[{datetime.now()}] Power ON")

# Function to turn off the power
def power_off():
    GPIO.output(relay_pin, GPIO.LOW)
    print(f"[{datetime.now()}] Power OFF")

# Function to determine if power should be ON
def should_turn_on(hour):
    # Lights ON between 9:00 to 18:00 and 21:00 to 6:00
    if (9 <= hour < 18) or (21 <= hour or hour < 6):
        return True
    return False

# Test Mode: Interactive on/off control
def test_mode():
    print(f"[{datetime.now()}] Running in TEST MODE")
    try:
        while True:
            command = input("Type 'on' to turn on, 'off' to turn off, or 'exit' to quit: ").strip().lower()
            if command == "on":
                power_on()
            elif command == "off":
                power_off()
            elif command == "exit":
                print(f"[{datetime.now()}] Exiting TEST MODE")
                break
            else:
                print(f"[{datetime.now()}] Invalid command. Please type 'on', 'off', or 'exit'.")
    finally:
        GPIO.cleanup()

# Run Mode: Automated control based on time
def run_mode():
    print(f"[{datetime.now()}] Running in RUN MODE")
    try:
        while True:
            now = datetime.now()
            hour = now.hour

            # Determine if the lights should be ON or OFF
            if should_turn_on(hour):
                power_on()
            else:
                power_off()

            # Sleep for 1 minute before checking again
            time.sleep(60)
    finally:
        GPIO.cleanup()

# Main Function
if __name__ == "__main__":
    mode = input("Enter 'test' for test mode or 'run' for automated mode: ").strip().lower()
    if mode == "test":
        test_mode()
    elif mode == "run":
        run_mode()
    else:
        print(f"[{datetime.now()}] Invalid input. Please enter 'test' or 'run'.")