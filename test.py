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

button_pin = 17  # Use the correct GPIO pin for the button
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def start_spin():
    # Define the initial speed and the decay factor
    initial_speed = random.uniform(0.5, 1.0)  # Random initial speed between 50% and 100%
    decay_factor = random.uniform(0.005, 0.015)  # Random decay factor between 0.5% and 1.5% per step

    # Calculate the total number of steps and the delay time for each step
    total_steps = random.randint(10, 20) * num_leds  # Random number of total steps between 3000 and 6000
    delay_time = 0.01 / initial_speed  # Initial delay time proportional to the initial speed

    # Start the animation
    for i in range(total_steps):
        # Turn off all LEDs
        for j in range(num_leds):
            pixels[j] = (0, 0, 0)

        # Light up 5 random LEDs
        for j in range(5):
            index = random.randint(0, num_leds - 1)
            pixels[index] = (0, 0, 255)

        pixels.show()

        # Gradually increase the delay time to slow down the animation
        delay_time += delay_time * decay_factor

        # Wait for the delay time
        time.sleep(delay_time)

while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
