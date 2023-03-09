import time
import board
import neopixel
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)

pixel_pin = board.D18
numleds = 16
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER)
winningnumbers = [1,2,3,4,5,6,12]
losingnumbers = list(set(range(1, numleds+1)) - set(winningnumbers))
minrotations = 6
maxrotations = 10
spin = 0
last_winning_led = None
rainbow_on = False

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
    numleds = 16
    decay = rotations * numleds
    spin += 1
    for rotation in range(1,rotations):
        led_colour = (0, 0, 255)
        led_stop_colour = (0, 0, 255)
        if rotation == rotations - 1:
            winner, is_winning_number = selectwinner(spin)
            numleds = winner
            if is_winning_number:
                led_stop_colour = (0, 255, 0)
            else:
                led_stop_colour = (255, 0, 0)
        for led in range(numleds):
            if led+1 == numleds:
                led_colour = led_stop_colour
            pixels[led] = led_colour
            pixels[led-1] = (0, 0, 0)
            time.sleep(rotation/decay)
            decay -= 1
            pixels.show()
    pixels.fill((0, 0, 0))

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

try:
    rainbow_on = False
    while True:
        select_spin = GPIO.input(17)
        select_presentation = GPIO.input(27)
        if select_spin == False:
            print('Spin selected')
            start_spin()
        if select_presentation == False:
            print('Presentation selected')
            rainbow_on = True
            while rainbow_on:
                rainbow_cycle(0.001)
                select_presentation = GPIO.input(27)
                if select_presentation == False:
                    rainbow_on = False
                    pixels.fill((0, 0, 0))
                    pixels.show()
                    while select_presentation == False:
                        select_presentation = GPIO.input(27)

finally:
    pixels.fill((0, 0, 0))
    pixels.show()
    print("All LEDs OFF")
