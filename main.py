import time
import RPi.GPIO as GPIO
from spin import start_spin
from idle import start_idle_mode

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)

try:
    while True:
        select_spin = GPIO.input(17)
        select_idle_mode = GPIO.input(27)
        if select_spin == False:
            print('Spin selected')
            start_spin()
        if select_idle_mode == False:
            print('Presentation selected')
            start_idle_mode()


finally:
    GPIO.cleanup()
    print("All LEDs OFF")
