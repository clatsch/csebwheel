import board
import neopixel
import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)
pixel_pin = board.D18
num_leds = 300
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_leds, brightness=0.6, auto_write=False, pixel_order=ORDER)

min_rotations = 3
max_rotations = 5
button_pin = 17

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def start_spin():
    # Generate a random strength between 40% and 100%
    strength = random.uniform(0.4, 1.0)
    # Calculate the number of rotations based on the strength and the min/max rotations
    rotations = int(random.randint(min_rotations, max_rotations) * num_leds * strength)
    # Calculate the total number of steps
    total_steps = rotations * num_leds
    # Calculate the initial delay time (faster initial speed)
    delay_time = 0.0005 / strength

    # Loop through all the steps
    for i in range(total_steps):
        # Calculate the index of the first LED to light up
        start_index = i % num_leds
        # Light up the next 5 LEDs
        for j in range(5):
            index = (start_index + j) % num_leds
            pixels[index] = (0, 0, 255)
        # Turn off the LEDs that were lit up in the previous iteration
        for j in range(5):
            index = (start_index - 5 + j) % num_leds
            pixels[index] = (0, 0, 0)
        # Show the updated LED colors
        pixels.show()
        # Gradually increase the delay time to simulate friction and slowing down
        delay_time += 0.0000001 * (total_steps - i) / total_steps
        # Wait for the calculated delay time
        time.sleep(delay_time)

    # Turn off all the LEDs
    pixels.fill((0, 0, 0))
    pixels.show()

while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
