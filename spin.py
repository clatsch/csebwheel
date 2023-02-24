import time
import board
import neopixel
import random

pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 16

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

while True:
    pixels.fill((0, 0, 0))  # turn off all pixels
    pixels.show()

    # choose a random pixel to light up
    pixel_index = random.randint(0, num_pixels-1)

    # choose a random number of spins
    num_spins = 2
    # num_spins = random.randint(3, 10)

    # light up the chosen pixel
    for i in range(num_spins * num_pixels):
        # turn off all pixels
        pixels.fill((0, 0, 0))

        # calculate the pixel to light up based on the current spin
        spin_position = i % num_pixels
        current_pixel_index = (pixel_index + spin_position) % num_pixels

        # set the color of the current pixel to a random color
        pixels[current_pixel_index] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # show the updated pixel colors
        pixels.show()

        # delay between updates
        time.sleep(0.1)

pixels.fill((0, 0, 0))  # turn off all pixels
pixels.show()           # update the pixels to turn them off
