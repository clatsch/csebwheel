import time
import board
import neopixel
import RPi.GPIO as GPIO

# Pin definitions
BUTTON_PIN = 22
pixel_pin = board.D18
numleds = 16
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER)

# Define groups of pixels
groups = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]

# # Initialize button
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON_PIN, GPIO.IN)

# Define function to light up a group of pixels
def light_up_group(group):
    global current_group
    for i in range(numleds):
        if i in group:
            pixels[i] = (255, 255, 255)  # Set color of pixels in the current group to white
        else:
            pixels[i] = (0, 0, 0)  # Set color of pixels in other groups to off
    current_group = group
    pixels.show()

# Main loop
current_group = 0

def start_presentation_mode():
    global current_group
    while True:
        if GPIO.input(BUTTON_PIN) == False:
            light_up_group(groups[current_group]) # Light up the current group
            current_group = (current_group + 1) % len(groups) # Move to the next group
            while GPIO.input(BUTTON_PIN) == False:
                pass # Wait for button to be released
