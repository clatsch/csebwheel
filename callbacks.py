import RPi.GPIO as GPIO
import time

def button_callback(channel):
    print("Button pressed")
    start_spin(18)

