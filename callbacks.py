import RPi.GPIO as GPIO
import time

def button_callback(channel):
    print("Button pressed!")
    time.sleep(0.2) # Wait for 200ms to debounce
