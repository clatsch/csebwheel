import RPi.GPIO as GPIO
import time
from spin import start_spin

def button_callback(channel):
    print("Button pressed")
    start_spin(18)

