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
is_winner = False  # Define is_winner as a global variable

def selectwinner(spins):
    global winning_spins, is_winner  # Access the global variable is_winner
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
            decay = rotations * numleds
            spin += 1
            stop_led = random.randint(0, numleds-1)  # Generate a random stopping point
            for rotation in range(1,rotations):
                led_colour = ((255,255,255))
                led_stop_colour  = ((255,255,255))
                if rotation == rotations - 1:
                    winner = selectwinner(spin)
                    numleds = winner.get("numleds")
                    led_stop_colour = winner.get("led_colour")
                    winning_spins = winner.get("winning_spins")
                    is_winner = winner.get("is_winner")
                for led in range(numleds):
                    if led == stop_led:  # Stop on the random stopping point
                        if is_winner:
                            pixels[led] = (0,255,0)
                            for i in range(5):
                                pixels[led] = (0,0,0)
                                pixels.show()
                                time.sleep(0.1)
                                pixels[led] = (0,255,0)
                                pixels.show()
                                time.sleep(0.1)
                        else:
                            pixels[led] = (255,0,0)
                            for i in range(5):
                                pixels[led] = (0,0,0)
                                pixels.show()
                                time.sleep(0.1)
                                pixels[led] = (255,0,0)
                                pixels.show()
                                time.sleep(0.1)
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
