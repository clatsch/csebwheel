import time
import board
import neopixel
import RPi.GPIO as GPIO
from newSpin import start_spin

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pixel_pin = board.D18
numleds = 363
ORDER = neopixel.RGBW
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.8, auto_write=False, pixel_order=ORDER)

def wheel(pos):
    if pos < 0 or pos > 255:
        b = w = 0
    elif pos < 128:
        b = 255 - pos*2
        w = pos*2
    else:
        b = (pos - 128)*2
        w = 255 - (pos - 128)*2
    return (0, 0, b, w) if ORDER in (neopixel.RGBW, neopixel.RGBW) else (0, 0, b)




def rainbow_cycle(wait):
    for j in range(255):
        for i in range(numleds):
            pixel_index = (i * 256 // numleds) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def start_idle_mode():
    # Define the button_pin variable for the button on pin 27
    button_pin = 27
    # Setup the button as input with pull-up resistor
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Wait for the button on pin 27 to be pressed
    while GPIO.input(button_pin) == GPIO.HIGH:
        time.sleep(0.1)
    # Cleanup the GPIO and return to main.py
    GPIO.cleanup(button_pin)




