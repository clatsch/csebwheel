import time
import board
import neopixel
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)

pixel_pin = board.D18

# The number of NeoPixels
numleds = 16

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# Define the winning numbers
winningnumbers = [1, 2, 3, 4, 5, 6, 12]

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
for rotation in range(1, rotations):

    # Set the default LED color to white
    led_colour = (0, 0, 255)

    # Reset the LED stop color to white
    led_stop_colour = (0, 0, 255)

    # If this is the last rotation, select a winning or losing number
    if rotation == rotations - 1:
        winner, is_winning_number = selectwinner(spin)
        numleds = winner
        if is_winning_number:
            led_stop_colour = (0, 255, 0)  # set to green if winning number
        else:
            led_stop_colour = (255, 0, 0)  # set to red if losing number not in winningnumbers array

    # Loop through all the LEDs in this rotation
    for led in range(numleds):

        # If this is the last LED in the rotation, change its color to the stop color
        if led + 1 == numleds:
            led_colour = led_stop_colour

        # Turn on the current LED and turn off the previous LED
        pixels[led] = led_colour
        if led > 0:
            pixels[led - 1] = (0, 0, 0)
        else:
            pixels[numleds - 1] = (0, 0, 0)

        # Sleep for a fraction of a second to create a logarithmic decay effect
        time.sleep(rotation / decay)

        # Decrement the decay variable to increase the sleep time for each subsequent LED
        decay -= 1

        # Update the LEDs
        pixels.show()

    # Wait for a short period of time before starting the next LED sequence
    time.sleep(0.1)

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
    global rainbow_active
    rainbow_active = True

    while rainbow_active:
        for j in range(255):
            for i in range(numleds):
                pixel_index = (i * 256 // numleds) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

    # Turn off all the LEDs
    pixels.fill((0, 0, 0))
    print("ALL LEDS OFF")

print('Press Ctrl-C to quit.')

try:
    while True:
        select_spin = GPIO.input(17)
        select_presentation = GPIO.input(27)
        if select_spin == False:
            print('spin selected')
            start_spin()
        if select_presentation == False:
            print('presentation selected')
            rainbow_cycle(0.001)
            while select_presentation == False:
                select_presentation = GPIO.input(27)
                # Switch off rainbow with button on GPIO 27
                if select_spin == False:
                    pixels.fill((0, 0, 0))
                    pixels.show()
                    break

finally:
    # Turn off all the LEDs
    pixels.fill((0, 0, 0))
    print("ALL LEDS OFF")
