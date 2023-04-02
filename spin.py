import time
import board
import neopixel
import random
import RPi.GPIO as GPIO
import math

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
    rotations = random.randint(minrotations, maxrotations)
    global numleds
    decay = rotations * numleds * 100
    spin += 1
    chunk_size = 5  # Increase this value to update more LEDs per iteration
    for rotation in range(1, rotations):
        led_colour = (0, 0, 255)
        led_stop_colour = (0, 0, 255)
        if rotation == rotations - 1:
            winner, is_winning_number = selectwinner(spin)
            numleds = winner
            if is_winning_number:
                led_stop_colour = (0, 255, 0)
            else:
                led_stop_colour = (255, 0, 0)
        for i in reversed(range(0, numleds, chunk_size)):  # Update LEDs in chunks instead of every LED
            chunk = min(chunk_size, numleds - i)
            pixels[i:i+chunk] = [led_stop_colour] + [led_colour]*(chunk-1)
            pixels[(i+chunk) % numleds] = (0, 0, 0)
            for j in range(i+chunk, i+chunk+chunk_size):
                pixels[j % numleds] = (0, 0, 0)  # Turn off LEDs after the chunk being updated
            progress = rotation / (rotations - 1)  # Calculate progress of spin
            current_speed = (1 - math.log(progress + 1, 2)) / 50  # Use logarithmic function to reduce speed
            time.sleep(current_speed)
            pixels.show()
            decay -= chunk
        if rotation == rotations - 1:
            pixels.fill(led_stop_colour)
            time.sleep(0.5)
            pixels.fill((0, 0, 0))
        else:
            pixels.fill((0, 0, 0))
            time.sleep(0.2)








