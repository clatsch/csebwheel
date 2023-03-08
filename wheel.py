import time
import board
import neopixel
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

pixel_pin = board.D18
numleds = 16
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.2, auto_write=False, pixel_order=ORDER)

# Define the winning pixels as an array
winning_pixels = [3, 6, 9, 12]

# Define the acceleration of the LED ring
acceleration = 1.05  # higher values mean faster acceleration

# Function to spin the LED ring
def spin():
    # Generate a random spin range between 6 and 15 pixels
    spin_range = random.randint(6, 15)
    speed = 0.05  # reset the speed
    for i in range(16):
        pixels[i] = (255, 255, 255)  # set all pixels to white
    pixels.show()
    time.sleep(0.5)  # pause for a moment
    for i in range(spin_range):
        pixels[i] = (0, 0, 0)  # turn off all pixels
        pixels[i-1] = (255, 255, 255)  # move the "active" pixel
        pixels.show()
        time.sleep(speed)
        speed *= acceleration  # speed up the rotation
    pixels.fill((0, 0, 0))  # turn off all pixels
    pixels.show()
    time.sleep(1)  # pause for a moment

# Main loop
while True:
    input_value = GPIO.input(17)
    if input_value == False:
        print('Button pressed!')
        spin()
        if pixels[winning_pixels[-1]] == (255, 255, 255):
            # if the last pixel is a winning pixel, flash green
            pixels.fill((0, 255, 0))
            pixels.show()
            time.sleep(2)  # pause for a moment
        else:
            # if the last pixel is not a winning pixel, flash red
            pixels.fill((255, 0, 0))
            pixels.show()
            time.sleep(2)  # pause for a moment
        pixels.fill((0, 0, 0))  # turn off all pixels
        pixels.show()
