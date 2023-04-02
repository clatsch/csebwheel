import time
import board
import neopixel
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pixel_pin = board.D18
numleds = 363
ORDER = neopixel.RGBW
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.6, auto_write=False, pixel_order=ORDER)
winningnumbers = [1,2,3,4,5,6,12]
losingnumbers = list(set(range(1, numleds+1)) - set(winningnumbers))
minrotations = 5
maxrotations = 11
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

    total_rotations = random.randint(minrotations, maxrotations) * numleds
    min_speed = 0.001  # Adjust this value to control the minimum spinning speed
    max_speed = 0.04  # Adjust this value to control the maximum spinning speed

    for rotation in range(1, total_rotations):
        winner, is_winning_number = selectwinner(spin)
        numleds = winner
        if is_winning_number:
            led_stop_colour = (0, 255, 0)
        else:
            led_stop_colour = (255, 0, 0)

        current_led = numleds - (rotation % numleds) - 1
        if current_led + 1 == numleds:
            pixels[current_led] = led_stop_colour
        else:
            pixels[current_led] = (0, 0, 255)
        pixels[(current_led + 1) % numleds] = (0, 0, 0)

        progress = rotation / total_rotations
        current_speed = min_speed + (max_speed - min_speed) * progress**2
        time.sleep(current_speed)

        pixels.show()
    pixels.fill((0, 0, 0))
