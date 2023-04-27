import board
import neopixel
import RPi.GPIO as GPIO
import time
import random
import math

GPIO.setmode(GPIO.BCM)
pixel_pin = board.D18
num_leds = 363
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_leds, brightness=0.6, auto_write=False, pixel_order=ORDER)

min_rotations = 3
max_rotations = 5
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

spin_completed = False # Flag variable to track if the first spin has been completed

def spin_action(first_led_index):
    flash_finished = False
    for segment in segments:
        if first_led_index in segment:
            flash_duration = 3
            flash_segment_pulse(segment, flash_duration, 3)
            flash_finished = True
            break

    if not flash_finished:
        pixels.fill((0, 0, 0))
        pixels.show()
    time.sleep(0.2)

    if any(pixels):
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.5)

    time.sleep(0.1)

def start_spin():
    global spin_completed # Use the global flag variable
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
            pixels[prev_index] = (0, 0, 0)

        for j in range(5):
            index = (i - j) % num_leds
            pixels[index] = (0, 0, 255)

        pixels.show()

        delay_time = 0.001 / current_speed
        time.sleep(delay_time)

    first_led_index = i % num_leds
    spin_action(first_led_index) # call spin_action with the first_led_index as argument
    spin_completed = True # Set the flag variable to True when the first spin is completed

def flash_segment_pulse(segment, flash_duration, num_pulses):
    start_flash_time = time.time()
    flash_interval = flash_duration / num_pulses
    while time.time() < start_flash_time + flash_duration:
        elapsed_time = time.time() - start_flash_time
        if elapsed_time < flash_interval * 0.7:
            brightness = 255
        else:
            brightness = int(abs(math.sin((elapsed_time - flash_interval * 0.7) * math.pi / (flash_interval * 0.3))) * 255)
        for j in range(num_leds):
            if j in segment:
                pixels[j] = (brightness, brightness, brightness)
            else:
                pixels[j] = (0, 0, 0)
        pixels.show()
        time.sleep(0.01)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)

# Define a callback function for the button press
def button_callback(channel):
    global spin_completed # Use the global flag variable
    if spin_completed:
        first_led_index = start_spin()
        spin_completed = False # Reset the flag variable
    print("Button pressed")

# Add a button interrupt to listen for button presses
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
    GPIO.cleanup()




