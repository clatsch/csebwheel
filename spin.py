import time
import board
import neopixel
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pixel_pin = board.D18
numleds = 363
ORDER = neopixel.RGBW
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.6, auto_write=False, pixel_order=ORDER)
winningnumbers = [1,2,3,4,5,6,12]
losingnumbers = list(set(range(1, numleds+1)) - set(winningnumbers))
minrotations = 5
maxrotations = 11
spin = 0
last_winning_led = None


def selectwinner(spins):
    global last_winning_led
    numleds = 0
    if last_winning_led is not None and last_winning_led in winningnumbers:
        numleds = random.choice(losingnumbers)
    else:
        numleds = random.choice(winningnumbers)
    if numleds in winningnumbers and last_winning_led is None:
        numleds = winningnumbers[0]
    last_winning_led = numleds
    is_winning_number = numleds in winningnumbers
    winner = (numleds, is_winning_number)
    return winner


def start_spin():
    global spin
    global last_winning_led
    spin += 1

    min_rotations = 5
    max_rotations = 10
    total_rotations = random.randint(min_rotations, max_rotations)
    initial_speed = 0.01  # Adjust this value to control the initial spinning speed
    final_speed = 0.05  # Adjust this value to control the final spinning speed

    chunk_size = 5
    num_chunks = numleds // chunk_size
    if num_chunks * chunk_size < numleds:
        num_chunks += 1

    for rotation in range(1, total_rotations * num_chunks):
        winner, is_winning_number = selectwinner(spin)
        numleds = winner

        # Calculate the start and end index of the rotating chunk
        start_index = (rotation % num_chunks) * chunk_size
        end_index = min(start_index + chunk_size, numleds)

        # Set the color of the pixels in the rotating chunk
        for led in range(start_index, end_index):
            if is_winning_number:
                pixels[led] = (0, 255, 0)  # Green for winning number
            else:
                pixels[led] = (255, 0, 0)  # Red for losing number

        # Turn off the rest of the pixels
        for led in range(numleds):
            if led < start_index or led >= end_index:
                pixels[led] = (0, 0, 0)

        # Calculate the current speed based on the progress of the rotation
        progress = rotation / (total_rotations * num_chunks)
        current_speed = initial_speed * (1 - progress) + final_speed * progress

        # Wait for the specified amount of time and then show the pixels
        time.sleep(current_speed)
        pixels.show()

    # Turn off all the pixels when the spinning is complete
    pixels.fill((0, 0, 0))
    pixels.show()

