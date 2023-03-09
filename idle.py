import time
import board
import neopixel
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pixel_pin = board.D18
numleds = 16
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER)

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
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

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
        rainbow_cycle(0.001)
        if GPIO.input(27) == GPIO.LOW:
            rainbow_on = False
            pixels.fill((0, 0, 0))
            pixels.show()
            while GPIO.input(27) == GPIO.LOW:
                pass
