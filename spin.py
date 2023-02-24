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

counter = 0  # counter for the number of spins

while True:
    pixels.fill((0, 0, 0))  # turn off all pixels
    pixels.show()

    # choose a random pixel to light up
    pixel_index = random.randint(0, num_pixels-1)

    # choose a random number of spins
    num_spins = random.randint(3, 10)

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

        # check if three spins have been completed
        if i % num_pixels == num_pixels - 1:
            counter += 1  # increment the counter

            if counter == 3:
                # light up the last LED
                pixels.fill((255, 0, 255))
                pixels.show()
                time.sleep(3)
                break  # break out of the loop

    if counter == 3:
        # break out of the outer while loop
        break

pixels.fill((0, 0, 0))  # turn off all pixels
pixels.show()           # update the pixels to turn them off
