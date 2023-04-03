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

min_rotations = 5
max_rotations = 11
button_pin = 21  # Assuming you have the button connected to GPIO21

# Setup button input
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function to light up 5 LEDs
def light_up(current_led):
    for i in range(5):
        index = (current_led + i) % num_leds
        pixels[index] = (255, 0, 0)  # Set the color to red

# Function to turn off all LEDs
def clear_leds():
    for i in range(num_leds):
        pixels[i] = (0, 0, 0)
    pixels.show()

def start_spin():
    rotations = random.randint(min_rotations, max_rotations) * num_leds
    for i in range(rotations):
        clear_leds()
        light_up(i % num_leds)
        pixels.show()

        # Slow down the spin as it approaches the end
        slowdown_factor = 1 + (i / rotations)
        delay_time = 0.01 * math.sqrt(slowdown_factor)
        time.sleep(delay_time)

while True:
    input_state = GPIO.input(button_pin)
    print(f"Button state: {input_state}")  # Debug print statement
    if input_state == True:  # Change this condition
        print("Button pressed. Starting spin.")  # Debug print statement
        start_spin()
        time.sleep(0.2)  # Debounce
    time.sleep(0.1)  # Add a short delay to avoid excessive printing


