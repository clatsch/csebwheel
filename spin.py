import time
import board
import neopixel
import random
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BCM)
pixel_pin = board.D18
numleds = 363
ORDER = neopixel.RGBW
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.6, auto_write=False, pixel_order=ORDER)
winningnumbers = [1,2,3,4,5,6,12]
losingnumbers = list(set(range(1, numleds+1)) - set(winningnumbers))
minrotations = 5
maxrotations = 10
spin = 0
last_winning_led = None

def selectwinner(spins):
    global last_winning_led
    numleds = 0
    if last_winning_led is not None and last_winning_led in winningnumbers:
        numleds = random.choice(losingnumbers)
    else:
        numleds = random.choice(winningnumbers)
    if numleds in winningnumbers and last_winning_led is None:
        numleds = winningnumbers[0]
    last_winning_led = numleds
    is_winning_number = numleds in winningnumbers
    winner = (numleds, is_winning_number)
    return winner

def start_spin():
    global spin
    global last_winning_led
    global numleds
    spin += 1

    min_rotations = 5
    max_rotations = 10
    total_rotations = random.randint(min_rotations, max_rotations) * numleds
    initial_speed = 0.001  # Adjust this value to control the initial spinning speed
    decay_factor = 1.0005  # Adjust this value to control how quickly the spinning slows down

    current_speed = initial_speed

    for rotation in range(1, total_rotations):
        led_colour = (0, 0, 255)
        led_stop_colour = (0, 0, 255)

        winner, is_winning_number = selectwinner(spin)
        numleds = winner
        if is_winning_number:
            led_stop_colour = (0, 255, 0)
        else:
            led_stop_colour = (255, 0, 0)

        for led in reversed(range(numleds)):
            if led + 1 == numleds:
                led_colour = led_stop_colour
            else:
                pixels[led] = led_colour
            pixels[(led + 1) % numleds] = (0, 0, 0)

            time.sleep(current_speed)
            pixels.show()

        # Update the speed for the next rotation
        current_speed *= decay_factor

    pixels.fill((0, 0, 0))
