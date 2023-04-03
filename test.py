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

segments = [    list(range(290, 299)),    list(range(271, 289)),    list(range(264, 270)),    list(range(231, 264)),    list(range(198, 231)),    list(range(165, 198)),    list(range(132, 165)),    list(range(99, 132)),    list(range(66, 99)),    list(range(33, 66)),    list(range(0, 33)),]

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

    lit_segments = []

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

        for segment in segments:
            if i % num_leds in segment and segment not in lit_segments:
                for k in range(100):
                    brightness = int(abs(math.sin(k * math.pi / 100)) * 255)
                    for j in segment:
                        pixels[j] = (brightness, brightness, brightness)
                    pixels.show()
                    time.sleep(0.01)

                pixels.fill((0, 0, 0))
                pixels.show()

                lit_segments.append(segment)

        if time.monotonic() - start_time > 20:
            break

        delay_time = 0.001 / current_speed
        time.sleep(delay_time)

    pixels.fill((0, 0, 0))
    pixels.show()

def flash_segment(segment):
    for i in range(100):
        brightness = int(abs(math.sin(i * math.pi / 100)) * 255)
        for j in segment:
            pixels[j] = (brightness, brightness, brightness)
        pixels.show()
        time.sleep(0.01)

    pixels.fill((0, 0, 0))
    pixels.show()

start_time = time.monotonic()

while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        start_spin()
        lit_segments = []
        start_time = time.monotonic()
        time.sleep(0.2)
    time.sleep(0.1)
