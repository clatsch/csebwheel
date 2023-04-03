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

    first_led_index = i % num_leds
    return first_led_index

def flash_segment_smooth(segment, num_flashes):
    for i in range(num_flashes):
        brightness = 255
        for j in range(4):
            for k in segment:
                pixels[k] = (brightness, brightness, brightness)
            pixels.show()
            time.sleep(0.05)
            brightness = int(brightness * 0.5)
        pixels.fill((0, 0, 0))
        pixels.show()
        if GPIO.input(button_pin) == False:
            time.sleep(0.2)
            return


while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        first_led_index = start_spin()
        flash_finished = False
        for segment in segments:
            if first_led_index in segment:
                start_flash_time = time.time()
                flash_duration = 3
                while time.time() < start_flash_time + flash_duration:
                    flash_segment_smooth(segment)
                    if GPIO.input(button_pin) == False:
                        time.sleep(0.2)
                        break
                else:
                    flash_finished = True
                break
        if not flash_finished:
            pixels.fill((0, 0, 0))
            pixels.show()
        time.sleep(0.2)

    elif any(pixels):
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.5)

    time.sleep(0.1)
