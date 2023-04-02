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
    rotations = random.randint(minrotations, maxrotations)
    numleds = 363
    decay = rotations * numleds
    spin += 1
    speed_factor = 10  # Increase this value to make the spinning faster

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
        for led in reversed(range(numleds)):
            if led+1 == numleds:
                led_colour = led_stop_colour
            if led == 4 or led == 13:  # check for pixels 5 and 14
                pixels[led] = (255, 255, 255)  # set color to white
            else:
                pixels[led] = led_colour
            pixels[(led+1) % numleds] = (0, 0, 0)
            time.sleep(rotation/decay)
            decay -= speed_factor  # Adjust the decrement value of decay with the speed factor
            pixels.show()
    pixels.fill((0, 0, 0))


