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
button_pin = 17

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

segments = [
    list(range(290, 299)),
    list(range(271, 289)),
    list(range(264, 270)),
    list(range(231, 264)),
    list(range(198, 231)),
    list(range(165, 198)),
    list(range(132, 165)),
    list(range(99, 132)),
    list(range(66, 99)),
    list(range(33, 66)),
    list(range(0, 33)),
]

def start_spin():
    strength = random.uniform(0.4, 1.0)

    distance = strength * num_leds * 2 * math.pi

    circumference = num_leds * 2 * math.pi
    rotations = int(distance / circumference)

    rotations += random.randint(0, 2)

    total_steps = rotations * num_leds

    friction = 0.9
    speed = 1.5 * strength

    starting_position = random.randint(0, num_leds - 1)

    i = starting_position # set default value for i
    for i in range(starting_position, starting_position + total_steps):
        remaining_steps = total_steps - (i - starting_position)
        current_speed = speed * remaining_steps / total_steps * friction

        for j in range(5):
            prev_index = (i - 5 + j) % num_leds
            pixels[prev_index] = (0, 0, 0)

        for j in range(5):
            index = (i + j) % num_leds
            pixels[index] = (0, 0, 255)

        pixels.show()

        delay_time = 0.001 / current_speed
        time.sleep(delay_time)

    # Find the segment where the spin stopped and light it up
    stop_position = (i - 4) % num_leds
    for segment in segments:
        if stop_position in segment:
            lit_segment(segment)
            break

    # Wait for a short time before finishing
    time.sleep(0.5)


def lit_segment(segment):
    for i in range(10):
        for j in segment:
            pixels[j] = (255, 0, 0)
        pixels.show()
        time.sleep(0.1)

        for j in segment:
            pixels[j] = (0, 0, 0)
        pixels.show()
        time.sleep(0.1)

while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
