import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 16)

pixels[0] = (255, 0, 0)
pixels[3] = (0, 255, 0)
pixels[4] = (0, 0, 255)
pixels[10] = (0, 56, 150)

