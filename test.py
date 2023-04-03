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

segments = [list(range(290, 299)), list(range(271, 289)), list(range(264, 270)), list(range(231, 264)),
            list(range(198, 231)), list(range(165, 198)), list(range(132, 165)), list(range(99, 132)),
            list(range(66, 99)), list(range(33, 66)), list(range(0, 33)), ]


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

    i = starting_position
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
    first_led_index = (i - 4) % num_leds
    for segment in segments:
        if first_led_index in segment:
            flash_segment(segment)

    # Flash all the segments smoothly for 10 seconds or until button is pressed
    start_flash_time = time.time()
    flash_duration = 10
    while time.time() < start_flash_time + flash_duration:
        flash_segments_smooth()
        if GPIO.input(button_pin) == False:
            time.sleep(0.2)
            return

    pixels.fill((0, 0, 0))
    pixels.show()


def flash_segment(segment):
    for k in range(100):
        brightness = int(abs(math.sin(k * math.pi / 100)) * 255)
        for j in segment:
            pixels[j] = (brightness, brightness, brightness)
        pixels.show()
        time.sleep(0.01)
    pixels.fill((0, 0, 0))
    pixels.show()


def flash_segments_smooth():
    for k in range(100):
        brightness = int(abs(math.sin(k * math.pi / 100)) * 255)
        for segment in segments:
            for j in segment:
                pixels[j] = (brightness, brightness, brightness)
        pixels.show()
        time.sleep(0.01)
    pixels.fill((0, 0, 0))
    pixels.show()


while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
