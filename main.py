import RPi.GPIO as GPIO
import time
from spin import start_spin
from idle import start_idle_mode
from presentation import light_up_group

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DEBOUNCE_TIME = 0.3  # Set the debounce time to 300ms

last_spin_time = 0
last_idle_time = 0
last_presentation_time = 0

try:
    while True:
        current_time = time.time()

        if GPIO.input(17) == False and current_time - last_spin_time > DEBOUNCE_TIME:
            print('Spin selected')
            start_spin()
            last_spin_time = current_time

        if GPIO.input(27) == False and current_time - last_idle_time > DEBOUNCE_TIME:
            print('Idle Mode Selected')
            start_idle_mode()
            last_idle_time = current_time

        if GPIO.input(22) == False and current_time - last_presentation_time > DEBOUNCE_TIME:
            print('Presentation Mode Selected')
            light_up_group()
            last_presentation_time = current_time

except KeyboardInterrupt:
    GPIO.cleanup()
    print("All LEDs OFF")

if any(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()
