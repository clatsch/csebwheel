import time
import board
import neopixel
import RPi.GPIO as GPIO

from idle import start_idle_mode
from spin import start_spin

# Pin definitions
BUTTON_PIN = 22
pixel_pin = board.D18
numleds = 16
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER)

# Define groups of pixels
groups = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]

# Define function to light up a group of pixels
def light_up_group(group):
    # Turn off all pixels first
    pixels.fill((0, 0, 0))
    # Set the color of the pixels in the group to white
    for i in group:
        pixels[i] = (255, 255, 255)
    pixels.show()

# Define a callback function to handle button presses
# Define a callback function to handle button presses
def button_callback(channel):
    global current_group
    # Increment current_group to move to the next group
    current_group = (current_group + 1) % len(groups)
    light_up_group(groups[current_group])

    # Check if spin button is pressed
    if GPIO.input(17) == False:
        print('Spin selected')
        start_spin()
    # Check if idle mode button is pressed
    elif GPIO.input(27) == False:
        print('Idle Mode Selected')
        start_idle_mode()


# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Add event detection for button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

# Main loop
current_group = 0
light_up_group(groups[current_group])
while True:
    pass  # Main loop does nothing
