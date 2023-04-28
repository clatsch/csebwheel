import time
import board
import neopixel
import RPi.GPIO as GPIO
from newSpin import start_spin
from presentation import light_up_group

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pixel_pin = board.D18
numleds = 363
ORDER = neopixel.RGBW
pixels = neopixel.NeoPixel(pixel_pin, numleds, brightness=0.8, auto_write=False, pixel_order=ORDER)

def wheel(pos):
    if pos < 0 or pos > 255:
        b = w = 0
    elif pos < 128:
        b = 255 - pos*2
        w = pos*2
    else:
        b = (pos - 128)*2
        w = 255 - (pos - 128)*2
    return (0, 0, b, w) if ORDER in (neopixel.RGBW, neopixel.RGBW) else (0, 0, b)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(numleds):
            pixel_index = (i * 256 // numleds) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def start_idle_mode(pin):
    global pixels
    rainbow_on = True
    while rainbow_on:
        rainbow_cycle(0.1)  # Increase the wait time for a slower cycle
        if GPIO.input(pin) == GPIO.LOW:
            rainbow_on = False
            pixels.fill((0, 0, 0, 0))
            pixels.show()
            while GPIO.input(pin) == GPIO.LOW:
                pass
        elif GPIO.input(17) == GPIO.LOW:
            rainbow_on = False
            pixels.fill((0, 0, 0, 0))
            pixels.show()
            start_spin()

def button_callback(pin):
    if pin == 27:
        start_idle_mode(pin)

# Setup the button as input with pull-up resistor
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Add event detection for button press
GPIO.add_event_detect(17, GPIO.FALLING, callback=lambda _: start_spin(), bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=lambda _: light_up_group(), bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("All LEDs OFF")

if any(pixels):
    pixels.fill((0, 0, 0, 0))
    pixels.show()
