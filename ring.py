import time
import board
import neopixel
import random

pixel_pin = board.D18

# The number of NeoPixels
numleds = 16

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER
)

minrotations = 6
maxrotations = 24

winningnumbers = [6,12]
losingnumbers = [1,2,3,4,5,7,8,9,10,11,13,14,15]

spin = 0 # spin number
winning_spins = 0 # for testing average wins printed to console

def selectwinner(spins): # function for choosing winner

    global winning_spins # for testing average wins printed to console

    winningspin = random.randint(3, 7) # randomisation of average winning spin

    if spin % winningspin == 0:
        numleds = random.sample(winningnumbers,  1)
        numleds = numleds[0]
        led_colour = [0,255,0] # winning colour B,G,R
        winning_spins += 1 # for testing average wins printed to console
    else:
        numleds = random.sample(losingnumbers,  1)
        numleds = numleds[0]
        led_colour = [0,0,255] # losing colour B,G,R


    winner = {
        "numleds":numleds,
        "led_colour":led_colour,
        "winning_spins":winning_spins # for testing average wins printed to console
    }
    return winner

# pixels= (0, 0, 0)

print('Press Ctrl-C to quit.')

try:
    while True:

        rotations = random.randint(minrotations, maxrotations) # randomised number of rotations in this spin

        numleds = 16 # reset to total number of leds after changing to chosen winner or loser

        decay = rotations * numleds # total number of leds in this spin - although more as last rotation is less

        spin += 1 # spin number going up each loop

        for rotation in range(1,rotations): # start spin - multiple rotations loop

            led_colour = ((255,255,255)) # default led colour B,G,R
            led_stop_colour  = ((255,255,255)) # reset to default colour B,G,R

            if rotation == rotations - 1: # on last rotation of spin select winning number

                winner = selectwinner(spin)
                led_stop_colour = winner.get("led_colour") # colour of winner or loser
                numleds = winner.get("numleds") # chosen winning or loser number
                winning_spins = winner.get("winning_spins") # for testing average wins printed to console

                # print("LED " + str(numleds)) # for testing print chosen led to console
                # print("Spin " + str(spin)) # for testing printed to console
                # print("Winning Spins " + str(winning_spins)) # for testing average wins printed to console


            for led in range(numleds): # start single rotation loop

                if led+1 == numleds: # if the last selected led - winner or loser
                    led_colour = led_stop_colour # changes colour based on winner or loser

                pixels[led] = (95,110,125)
                pixels[led-1] = (95/2,110/2,125/2)
                pixels[led-2] = (95/4,110/4,125/4)
                pixels[led-3] = (0,0,0)

                # pixels[led-11] = (255, 0, 0)
                # pixels[led-10] = (128, 0, 0)
                # pixels[led-9] = (64, 0, 0)
                # pixels[led-8] = (32, 0, 0)
                # pixels[led-7] = (64, 0, 0)
                # pixels[led-6] = (128, 0, 0)
                # pixels[led-5] = (255, 0, 0)

                time.sleep(rotation/decay) # creates log style increasing time delay
                decay -= 1 # increases time delay per led

                pixels.show()
                # pixels.fill((0, 0, 0))
                # pixels.show()

        time.sleep(5.0) # infinite loop pause between spins

finally:
    print("ALL LEDS OFF")
    pixels= (0, 0, 0)
    # pixels.show()
