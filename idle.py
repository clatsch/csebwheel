import time
import datetime
import board
import neopixel
import RPi.GPIO as GPIO
from newSpin import start_spin

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DEBOUNCE_TIME = 0.3

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
    global pixels
    rainbow_on = True
    rainbow_wait = 0.1
    rainbow_steps = 255
    rainbow_step_time = rainbow_wait / rainbow_steps
    rainbow_pos = 0

    while rainbow_on:
        # Intersperse with button press checks
        for i in range(10):
            if GPIO.input(27) == GPIO.LOW:
                rainbow_on = False
                pixels.fill((0, 0, 0, 0))
                pixels.show()
                light_up_group()
                break
            elif GPIO.input(17) == GPIO.LOW:
                rainbow_on = False
                pixels.fill((0, 0, 0, 0))
                pixels.show()
                start_spin()
                break
            time.sleep(0.01)

        # Continue with rainbow cycle
        for j in range(rainbow_steps):
            for i in range(numleds):
                pixel_index = (i * 256 // numleds) + rainbow_pos
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(rainbow_step_time)
            rainbow_pos += 1
            if rainbow_pos >= 256:
                rainbow_pos = 0
