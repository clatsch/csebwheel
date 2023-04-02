import time
import board
import neopixel
import RPi.GPIO as GPIO

from idle import start_idle_mode
from spin import start_spin

GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)

# Pin definitions
BUTTON_PIN = 22
pixel_pin = board.D18
numleds = 363
ORDER = neopixel.RGBW
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.5, auto_write=False, pixel_order=ORDER)

# Define groups of pixels
groups = [
    list(range(0, 33)),
    list(range(33, 66)),
    list(range(66, 99)),
    list(range(99, 132)),
    list(range(132, 165)),
    list(range(165, 198)),
    list(range(198, 231)),
    list(range(231, 264)),
    list(range(264, 297)),
    list(range(297, 330)),
    list(range(330, 361))
]

# Define function to light up a group of pixels
def light_up_group(group):
    # Turn off all pixels first
    pixels.fill((0, 0, 0, 0))
    # Set the color of the pixels in the group to white
    for i in group:
        pixels[i] = (255, 255, 255, 255)
    pixels.show()
    # Return the current group
    return groups.index(group)

# Define a callback function to handle button presses
def button_callback(channel):
    global current_group
    # Increment current_group to move to the next group
    current_group = (current_group + 1) % len(groups)
    current_group_index = light_up_group(groups[current_group])

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
current_group_index = light_up_group(groups[current_group])
while True:
    select_spin = GPIO.input(17)
    select_idle_mode = GPIO.input(27)
    if select_spin == False:
        print('Spin selected')
        start_spin()
    if select_idle_mode == False:
        print('Idle Mode Selected')
        start_idle_mode()

    time.sleep(0.1)
