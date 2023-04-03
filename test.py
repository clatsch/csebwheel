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

def start_spin():
    initial_strength = random.uniform(0.5, 1.0)
    rotations = int(random.randint(min_rotations, max_rotations) * num_leds * initial_strength)
    total_steps = rotations * 2

    for i in range(total_steps):
        for j in range(5):
            prev_index = (i - 5 + j) % num_leds
            pixels[prev_index] = (0, 0, 0)

        for j in range(5):
            index = (i + j) % num_leds
            pixels[index] = (0, 0, 255)

        pixels.show()

        progress = i / total_steps
        delay_time = -0.005 * math.log(1 - progress) * initial_strength
        time.sleep(delay_time)

while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
