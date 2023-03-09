import time
import board
import neopixel
import random

pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 16

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=True, pixel_order=ORDER
)

while True:

    rotations = 3

    for rotation in range(rotations):

        for i in range(num_pixels):
            pixels[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            time.sleep(0.1)
            pixels[i] = (0, 0, 0)

    time.sleep(1)

