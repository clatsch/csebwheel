# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 16

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


# def wheel(pos):
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 0 or pos > 255:
#         r = g = b = 0
#     elif pos < 85:
#         r = int(pos * 3)
#         g = int(255 - pos * 3)
#         b = 0
#     elif pos < 170:
#         pos -= 85
#         r = int(255 - pos * 3)
#         g = 0
#         b = int(pos * 3)
#     else:
#         pos -= 170
#         r = 0
#         g = int(pos * 3)
#         b = int(255 - pos * 3)
#     return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
#
#
# def rainbow_cycle(wait):
#     for j in range(255):
#         for i in range(num_pixels):
#             pixel_index = (i * 256 // num_pixels) + j
#             pixels[i] = wheel(pixel_index & 255)
#         pixels.show()
#         time.sleep(wait)


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

finally:
    pixels.fill((0, 0, 0))
