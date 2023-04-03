import board
import neopixel
import RPi.GPIO as GPIO
import random
import time

GPIO.setmode(GPIO.BCM)
pixel_pin = board.D18
numleds = 300
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.6, auto_write=False, pixel_order=ORDER)

# Set up the button
button_pin = 17
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define the minimum and maximum number of rotations
min_rotations = 5
max_rotations = 11

# Define the number of LEDs to light up at once
num_lights = 5

# Define the delay between LED updates
delay = 0.02

# Define the colors for the LEDs
colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)]

# Define a function to spin the wheel
def spin_wheel():
    # Choose a random number of rotations
    num_rotations = random.randint(min_rotations, max_rotations)

    # Choose a random initial speed
    speed = random.uniform(0.05, 0.1)

    # Set up the initial LED positions
    positions = list(range(numleds))
    random.shuffle(positions)
    lights = positions[:num_lights]

    # Spin the wheel
    for i in range(num_rotations):
        for j in range(num_lights):
            # Set the color for the current LED
            color = colors[j % num_lights]
            # Light up the current LED
            pixels[lights[j]] = color
        # Update the LED positions
        lights = [(x + 1) % numleds for x in lights]
        # Delay for a short time to slow down the wheel
        time.sleep(speed)
        # Reduce the speed
        speed += 0.001
    # Light up the final set of LEDs
    for j in range(num_lights):
        color = colors[j % num_lights]
        pixels[lights[j]] = color
    # Update the LEDs
    pixels.show()

# Define a function to handle button presses
def button_pressed(channel):
    # Spin the wheel
    spin_wheel()

# Set up the button event handler
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_pressed, bouncetime=300)

# Main loop
while True:
    # Update the LEDs
    pixels.show()
    # Delay for a short time
    time.sleep(delay)
