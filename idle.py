import time
import board
import neopixel
import RPi.GPIO as GPIO
from newSpin import start_spin

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

def start_idle_mode():
    global pixels
    rainbow_on = [True]  # Use a list to store the value of rainbow_on
    # Define the button_pin variable for the button on pin 27
    button_pin = 27
    # Save the current state of the GPIO
    gpio_state = {pin: GPIO.gpio_function(pin) for pin in (button_pin, 17, 22)}
    gpio_pull_state = {pin: GPIO.input(pin) for pin in (button_pin, 17, 22)}
    # Setup the button as input with pull-up resistor
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Add event detection for button press using interrupts
    GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=lambda _: rainbow_on.__setitem__(0, False), bouncetime=300)
    while rainbow_on[0]:
        rainbow_cycle(0.1)  # Increase the wait time for a slower cycle
        if GPIO.input(17) == GPIO.LOW:
            rainbow_on[0] = False
            pixels.fill((0, 0, 0, 0))
            pixels.show()
            start_spin()
    # Cleanup the GPIO and remove the event detection for the button on pin 27
    GPIO.remove_event_detect(button_pin)
    GPIO.cleanup(button_pin)
    # Restore the state of the GPIO
    for pin, function in gpio_state.items():
        GPIO.setup(pin, function)
    for pin, pull_state in gpio_pull_state.items():
        GPIO.input(pin, pull_state)



