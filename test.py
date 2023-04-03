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
    max_steps = random.randint(min_rotations, max_rotations) * num_leds * strength
    current_step = 0
    speed = 0.005 / strength
    deceleration = 0.01 * (1 - strength)

    while current_step < max_steps:
        for j in range(5):
            index = (current_step + j) % num_leds
            pixels[index] = (0, 0, 255)

        pixels.show()
        current_step += 1
        time.sleep(speed)
        speed += deceleration

    pixels.fill((0, 0, 0))
    pixels.show()

while True:
    input_state = GPIO.input(button_pin)
    if input_state == False:
        print("Button pressed. Starting spin.")
        start_spin()
        time.sleep(0.2)
    time.sleep(0.1)
