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

    # for led in range(num_pixels): # start single rotation loop

    # pixels.fill((0, 0, 0))  # turn off all pixels
    # pixels.show()
    # time.sleep(1)
    # pixels.fill((255, 0, 0))
    # pixels.show()
    # time.sleep(1)
    # pixels.fill((0, 255, 0))
    # pixels.show()
    # time.sleep(1)

    # pixels.fill((255, 255, 0))
    # time.sleep(1)
    # pixels.fill((255, 0, 0))
    # time.sleep(1)
    # pixels.fill((0, 250, 250))
    # time.sleep(1)
    pixels[1] = (0, 0, 250)
    time.sleep(1)
    pixels[1] = (0, 0, 0)

    pixels[2] = (255, 0, 250)
    time.sleep(1)
    pixels[2] = (0, 0, 0)

    # time.sleep(1)pixels.show()
    #     # time.sleep(1)



    # pixel_index = random.randint(0, num_pixels-1)

