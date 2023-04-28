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

DEBOUNCE_TIME = 0.3  # Set the debounce time to 300ms

def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGBW, neopixel.RGBW) else (r, g, b, w)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(numleds):
            pixel_index = (i * 256 // numleds) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def start_idle_mode():
    global pixels
    rainbow_on = True
    last_button_time = 0  # initialize variable for last button press time
    while rainbow_on:
        rainbow_cycle(0.001)
        current_time = time.time()  # get current time
        if GPIO.input(27) == GPIO.LOW:
            # check if debounce time has passed since last button press
            if current_time - last_button_time > DEBOUNCE_TIME:
                rainbow_on = False
                pixels.fill((0, 0, 0))
                pixels.show()
                while GPIO.input(27) == GPIO.LOW:
                    pass
                last_button_time = current_time  # update last button press time
        elif GPIO.input(17) == GPIO.LOW:
            # check if debounce time has passed since last button press
            if current_time - last_button_time > DEBOUNCE_TIME:
                rainbow_on = False
                pixels.fill((0, 0, 0))
                pixels.show()
                start_spin()
                last_button_time = current_time  # update last button press time
