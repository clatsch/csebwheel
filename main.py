import RPi.GPIO as GPIO
import time
from spin import start_spin, spin_action
from idle import start_idle_mode
from presentation import light_up_group

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spin_mode = False

try:
    while True:
        select_spin = GPIO.input(17)
        select_idle_mode = GPIO.input(27)
        select_presentation_mode = GPIO.input(22)
        print(f"Spin: {select_spin}, Idle: {select_idle_mode}, Presentation: {select_presentation_mode}")

        if select_spin == False and not spin_mode:
            print('Spin selected')
            start_spin()
            spin_mode = True
            time.sleep(0.2)
        elif spin_mode:
            spin_action()

        if select_idle_mode == False:
            print('Idle Mode Selected')
            spin_mode = False
            start_idle_mode()
            time.sleep(0.2)

        if select_presentation_mode == False:
            print('Presentation Mode Selected')
            spin_mode = False
            light_up_group()
            time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("All LEDs OFF")
