import board
import neopixel
import RPi.GPIO as GPIO
import time
import random
import math

GPIO.setmode(GPIO.BCM)
pixel_pin = board.D18
num_leds = 300
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_leds, brightness=0.6, auto_write=False, pixel_order=ORDER)

min_rotations = 5
max_rotations = 11
button_pin = 17  # Use the correct GPIO pin for the button

# Setup button input
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def start_spin():
    rotations = random.randint(min_rotations, max_rotations) * num_leds
    total_steps = rotations * 2

    for i in range(total_steps):
        # Turn off all LEDs
        for j in range(num_leds):
            pixels[j] = (0, 0, 0)

        # Light up 5 LEDs
        for j in range(5):
            index = (i + j) % num_leds
            pixels[index] = (255, 0, 0)  # Set the color to red

        pixels.show()

        # Calculate the progress of the spin (0 to 1)
        progress = i / total_steps

        # Calculate delay_time to start fast and gradually slow down
        delay_time = 0.005 * (1 + 2 * (progress ** 2))
        time.sleep(delay_time)


while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:  # Change this condition
        print("Button pressed. Starting spin.")  # Debug print statement
        start_spin()
        time.sleep(0.2)  # Debounce
    time.sleep(0.1)  # Add a short delay to avoid excessive printing
