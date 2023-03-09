import time
import RPi.GPIO as GPIO
from spin import start_spin
from idle import start_idle_mode
from presentation import start_presentation_mode

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)

try:
    while True:
        select_spin = GPIO.input(17)
        select_idle_mode = GPIO.input(27)
        select_presentation_mode = GPIO.input(22)
        if select_spin == False:
            print('Spin selected')
            start_spin()
        if select_idle_mode == False:
            print('Idle Mode Selected')
            start_idle_mode()
        if select_presentation_mode == False:
            print('Presentation Mode Selected')
            start_presentation_mode()
            time.sleep(0.2) # wait for button debounce

finally:
    GPIO.cleanup()
    print("All LEDs OFF")
