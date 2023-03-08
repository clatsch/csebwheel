import time
import board
import neopixel
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

pixel_pin = board.D18
numleds = 16
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER)

minrotations = 6
maxrotations = 24

winningnumbers = [6,12]
losingnumbers = [1,2,3,4,5,7,8,9,10,11,13,14,15]

spin = 0
winning_spins = 0

def selectwinner(spins):
    global winning_spins
    winningspin = random.randint(3, 7)
    if spin % winningspin == 0:
        numleds = random.sample(winningnumbers,  1)
        numleds = numleds[0]
        led_colour = [0,255,0]
        is_winner = True
        winning_spins += 1
    else:
        numleds = random.sample(losingnumbers,  1)
        numleds = numleds[0]
        led_colour = [0,0,255]
        is_winner = False
    winner = {
        "numleds":numleds,
        "led_colour":led_colour,
        "winning_spins":winning_spins,
        "is_winner": is_winner
    }
    return winner

print('Press Ctrl-C to quit.')

try:
    while True:
        input_value = GPIO.input(17)
        if input_value == False:
            print('Who pressed my button!')
            rotations = random.randint(minrotations, maxrotations)
            numleds = 16
            decay = rotations * numleds
            spin += 1
            for rotation in range(1,rotations):
                led_colour = ((255,255,255))
                led_stop_colour  = ((255,255,255))
                if rotation == rotations - 1:
                    winner = selectwinner(spin)
                    led_stop_colour = winner.get("led_colour")
                    numleds = winner.get("numleds")
                    winning_spins = winner.get("winning_spins")
                    is_winner = winner.get("is_winner")
                for led in range(numleds):
                    if led+1 == numleds:
                        led_colour = led_stop_colour
                    if led+1 == numleds and led_colour == [0,255,0]:
                        pixels[led] = (0,255,0)
                    elif led+1 == numleds and led_colour == [0,0,255]:
                        pixels[led] = (255,0,0)
                    else:
                        pixels[led] = (95,110,255)
                    pixels[led-1] = (40,50,60)
                    pixels[led-2] = (20,25,30)
                    pixels[led-3] = (0,0,0)
                    time.sleep(rotation/decay)
                    decay -= 1
                    pixels.show()
            while input_value == False:
                input_value = GPIO.input(17)

finally:
    print("ALL LEDS OFF")
    pixels= (0, 0, 0)
