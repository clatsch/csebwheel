import time
import board
import neopixel
import random

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

pixel_pin = board.D18

# The number of NeoPixels
numleds = 16

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Define the winning numbers
winningnumbers = [1,2,3,4,5,6,12]

# Generate a list of losing numbers by subtracting the winning numbers from a set of all possible numbers
losingnumbers = list(set(range(1, numleds+1)) - set(winningnumbers))

minrotations = 6
maxrotations = 10

spin = 0 # spin number
last_winning_led = None # initialize the last winning LED to None

def selectwinner(spins):
    global last_winning_led

    numleds = 0 # Initialize numleds to 0

    # Choose a random number from the list of winning numbers or losing numbers that are not in the winning numbers list
    if last_winning_led is not None and last_winning_led in winningnumbers:
        numleds = random.choice(losingnumbers)
    else:
        numleds = random.choice(winningnumbers)

    # If the current LED is a winning LED and the last winning LED is None, choose the first winning LED in the list
    if numleds in winningnumbers and last_winning_led is None:
        numleds = winningnumbers[0]
    last_winning_led = numleds

    is_winning_number = numleds in winningnumbers
    winner = (numleds, is_winning_number)
    return winner

def start_spin():
    global spin
    global last_winning_led

    input_value = GPIO.input(17)
    if input_value == False:
        print('Spin started!')

        # Select a random number of rotations for this spin
        rotations = random.randint(minrotations, maxrotations)

        # Reset the number of LEDs to the total number
        numleds = 16

        # Calculate the total number of LEDs that will be lit up in this spin
        decay = rotations * numleds

        # Increment the spin number
        spin += 1

        print(rotations)

        # Loop through all the rotations in this spin
        for rotation in range(1,rotations):

            # Set the default LED color to white
            led_colour = (0, 0, 255)

            # Reset the LED stop color to white
            print('....')
            led_stop_colour = (0, 0, 255)

            # If this is the last rotation, select a winning or losing number
            if rotation == rotations - 1:
                winner, is_winning_number = selectwinner(spin)
                numleds = winner
                if is_winning_number:
                    led_stop_colour = (0, 255, 0) # set to green if winning number
                else:
                    led_stop_colour = (255, 0, 0) # set to red if losing number not in winningnumbers array
                print("LED " + str(numleds))
                print("Spin " + str(spin))

            # Loop through all the LEDs in this rotation
            for led in range(numleds):

                # If this is the last LED in the rotation, change its color to the stop color
                if led+1 == numleds:
                    led_colour = led_stop_colour

                # Turn on the current LED and turn off the previous LED
                pixels[led] = led_colour
                pixels[led-1] = (0, 0, 0)

                # Sleep for a fraction of a second to create a logarithmic decay effect
                time.sleep(rotation/decay)

                # Decrement the decay variable to increase the sleep time for each subsequent LED
                decay -= 1

                # Update the LEDs
                pixels.show()

        # Wait for the button to be released before starting the next spin
        while input_value == False:
            input_value = GPIO.input(17)


print('Press Ctrl-C to quit.')

try:
    while True:
        input_value = GPIO.input(17)
        if input_value == False:
            start_spin()

finally:
    # Turn off all the LEDs
    pixels.fill((0, 0, 0))
    print("ALL LEDS OFF")
