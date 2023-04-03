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

min_rotations = 3
max_rotations = 5
button_pin = 17  # Use the correct GPIO pin for the button

# Setup button input
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def start_spin():
    rotations = random.randint(min_rotations, max_rotations) * num_leds
    total_steps = rotations * 2
    decay = rotations

    for i in range(total_steps):
        # Turn off the previous 5 LEDs
        for j in range(5):
            prev_index = (i - 5 + j) % num_leds
            pixels[prev_index] = (0, 0, 0)

        # Light up 5 LEDs
        for j in range(5):
            index = (i + j) % num_leds
            pixels[index] = (0, 0, 255)  # Set the color to blue

        pixels.show()

        # Calculate delay_time to start fast and gradually slow down
        delay_time = (i / decay) / 20  # Divide by 10 to make the initial speed 10 times faster
        time.sleep(delay_time)




while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:  # Change this condition
        print("Button pressed. Starting spin.")  # Debug print statement
        start_spin()
        time.sleep(0.2)  # Debounce
    time.sleep(0.1)  # Add a short delay to avoid excessive printing
