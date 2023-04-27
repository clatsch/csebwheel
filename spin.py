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
pixels = neopixel.NeoPixel(pixel_pin, num_leds, brightness=0.6, auto_write=False, pixel_order=ORDER)

button_pin = 17
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

segments = [
    list(range(330, 361)),
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
    for segment in segments:
        if first_led_index in segment:
            for index in segment:
                pixels[index] = (255, 0, 0, 0) # Set the color of the pixel to red
            pixels.show()
            time.sleep(1) # Wait for 1 second
            for index in segment:
                pixels[index] = (0, 0, 0, 0) # Reset the color of the pixel to black
            pixels.show()
            break

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
    for i in range(starting_position, starting_position - total_steps, -1):
        remaining_steps = total_steps - (starting_position - i)
        current_speed = speed * remaining_steps / total_steps * friction

        for j in range(5):
            prev_index = (i + 5 - j) % num_leds
            pixels[prev_index] = (0, 0, 0, 0)

        for j in range(5):
            index = (i - j) % num_leds
            pixels[index] = (0, 0, 255, 0)

        pixels.show()

        delay_time = 0.001 / current_speed
        time.sleep(delay_time)

    first_led_index = i % num_leds
    spin_action(first_led_index) # call spin_action with the first_led_index as argument

while True:
    if GPIO.input(button_pin) == False:
        print('Button pressed')
        pixels.fill((0, 0, 0, 0)) # Reset the LED state
        start_spin()

    time.sleep(0.1) # Wait for 0.1 seconds before checking the button again