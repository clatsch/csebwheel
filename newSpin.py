import board
import neopixel
import RPi.GPIO as GPIO
import time
import random
import math

GPIO.setmode(GPIO.BCM)
pixel_pin = board.D18
num_leds = 363
ORDER = neopixel.RGBW
pixels = neopixel.NeoPixel(pixel_pin, num_leds, brightness=0.8, auto_write=False, pixel_order=ORDER)

# min_rotations = 3
# max_rotations = 5
button_pin = 17

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

segments = [
    list(range(330, 362)),
    list(range(297, 330)),
    list(range(264, 297)),
    list(range(231, 264)),
    list(range(198, 231)),
    list(range(165, 198)),
    list(range(132, 165)),
    list(range(99, 132)),
    list(range(66, 99)),
    list(range(33, 66)),
    list(range(0, 33)),
]

def spin_action(first_led_index):
    flash_finished = False
    for segment in segments:
        if first_led_index in segment:
            flash_duration = 4
            flash_segment_pulse(segment, flash_duration, 3)
            flash_finished = True
            break
        else:
            continue

    if not flash_finished:
        pixels.fill((0, 0, 0, 0))
        pixels.show()
    time.sleep(0.1)

    if any(pixels):
        pixels.fill((0, 0, 0, 0))
        pixels.show()
        time.sleep(0.1)

    time.sleep(0.1)
    flash_finished = False  # add this line to reset the variable
    return


def start_spin():
    print("Starting spin")
    strength = random.uniform(0.6, 1.0)

    distance = strength * num_leds * 2 * math.pi

    circumference = num_leds * 2 * math.pi
    rotations = int(distance / circumference)

    rotations += random.randint(0, 2)

    total_steps = rotations * num_leds

    friction = 0.7
    speed = 1.6 * strength

    starting_position = random.randint(0, num_leds - 1)

    i = starting_position
    for i in range(starting_position, starting_position - total_steps, -1):
        remaining_steps = total_steps - (starting_position - i)
        current_speed = speed * remaining_steps / total_steps * friction

        for j in range(5):
            prev_index = (i + 5 - j) % num_leds
            pixels[prev_index] = (0, 0, 0, 0)

        for j in range(5):
            index = (i - j) % num_leds
            pixels[index] = (0, 0, 255, 70)

        pixels.show()

        delay_time = 0.001 / current_speed
        time.sleep(delay_time)

    first_led_index = i % num_leds
    spin_action(first_led_index) # call spin_action with the first_led_index as argument
    return

def flash_segment_pulse(segment, flash_duration, num_pulses):
    start_flash_time = time.time()
    flash_interval = flash_duration / num_pulses
    while time.time() < start_flash_time + flash_duration:
        elapsed_time = time.time() - start_flash_time
        if elapsed_time < flash_interval * 0.9:
            brightness = 255
        else:
            brightness = int(abs(math.sin((elapsed_time - flash_interval * 0.9) * math.pi / (flash_interval * 0.3))) * 255)
        for j in range(num_leds):
            if j in segment:
                pixels[j] = (brightness, brightness, brightness, brightness)
            else:
                pixels[j] = (0, 0, 0, 0)
        pixels.show()
        time.sleep(0.01)
    pixels.fill((0, 0, 0, 0))
    pixels.show()
    time.sleep(0.1)