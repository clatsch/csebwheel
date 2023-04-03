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
    initial_strength = random.uniform(0.5, 1.0)
    rotations = int(random.randint(min_rotations, max_rotations) * num_leds * initial_strength)
    total_steps = rotations * 2
    decay = rotations

    for i in range(total_steps):
        # Calculate the progress of the spin (0 to 1)
        progress = i / total_steps

        # Calculate delay_time to start fast and gradually slow down
        if progress < 0.5:
            delay_time = (1 - 2 * progress) * 0.005 / initial_strength + 0.001
        else:
            delay_time = (2 * progress - 1) ** 2 / initial_strength + 0.001

        # Light up 5 LEDs
        for j in range(5):
            prev_index = (i - 5 + j) % num_leds
            pixels[prev_index] = (0, 0, 0)

            index = (i + j) % num_leds
            pixels[index] = (0, 0, 255)

        pixels.show()

        time.sleep(delay_time)

    # Slow down the spin as it approaches the end
    for i in range(total_steps, total_steps + decay):
        # Calculate the progress of the spin (0 to 1)
        progress = (i - total_steps) / decay

        # Calculate delay_time to gradually slow down
        delay_time = (1 - progress) ** 2 / initial_strength + 0.001

        # Light up 5 LEDs
        for j in range(5):
            prev_index = (i - 5 + j) % num_leds
            pixels[prev_index] = (0, 0, 0)

            index = (i + j) % num_leds
            pixels[index] = (0, 0, 255)

        pixels.show()

        time.sleep(delay_time)

while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
