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
        r = g = b = w = 0
    elif pos < 128:
        r = 0
        g = 0
        b = pos * 2
        w = 0
    else:
        r = 0
        g = 0
        b = 0
        w = (pos - 128) * 2
    return (r, g, b, w) if ORDER in (neopixel.RGBW, neopixel.RGBW) else (r, g, b)


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
    while rainbow_on:
        rainbow_cycle(0.01)  # Increase the wait time for a slower cycle
        if GPIO.input(27) == GPIO.LOW:
            rainbow_on = False
            pixels.fill((0, 0, 0, 0))
            pixels.show()
            while GPIO.input(27) == GPIO.LOW:
                pass
        elif GPIO.input(17) == GPIO.LOW:
            rainbow_on = False
            pixels.fill((0, 0, 0, 0))
            pixels.show()
            start_spin()
