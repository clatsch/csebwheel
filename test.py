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
    print(strength)
    rotations = int(random.randint(min_rotations, max_rotations) * strength)
    total_steps = rotations * num_leds

    # Calculate initial speed based on strength and friction
    friction = 0.9
    speed = 1.5 * strength

    # Set a random starting position for the wheel
    starting_position = random.randint(0, num_leds - 1)

    # Spin the wheel
    for i in range(starting_position, starting_position + total_steps):
        # Calculate current speed based on remaining distance and friction
        remaining_steps = total_steps - (i - starting_position)
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

    # Turn off all LEDs and show them
    pixels.fill((0, 0, 0))
    pixels.show()

    # Wait for a short time before finishing
    time.sleep(0.5)


while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
