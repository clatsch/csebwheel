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
    strength = random.uniform(0.4, 1.0)
    rotations = int(random.randint(min_rotations, max_rotations) * strength * num_leds)
    total_steps = rotations * 2

    # Calculate initial speed based on strength and friction
    friction = 0.95
    speed = 10 * strength

    # Spin the wheel
    for i in range(total_steps):
        # Calculate current speed based on remaining distance and friction
        remaining_steps = total_steps - i
        current_speed = speed * remaining_steps / total_steps * friction

        # Update LED colors and show them
        for j in range(5):
            prev_index = (i - 5 + j) % num_leds
            pixels[prev_index] = (0, 0, 0)

        for j in range(5):
            index = (i + j) % num_leds
            pixels[index] = (0, 0, 255)

        pixels.show()

        # Wait for a short time based on current speed
        delay_time = 0.001 / current_speed
        time.sleep(delay_time)

    # Determine stopping point based on strength
    stop_index = (rotations * strength * num_leds) % num_leds

    # Turn off all LEDs and show them
    pixels.fill((0, 0, 0))
    pixels.show()

    # Light up the stopping point in yellow and wait for a short time before finishing
    for i in range(10):
        if i % 2 == 0:
            pixels[stop_index] = (255, 255, 0)
        else:
            pixels[stop_index] = (0, 0, 0)
        pixels.show()
        time.sleep(0.1)

while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
