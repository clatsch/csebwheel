import RPi.GPIO as GPIO
import time
from spin import start_spin, spin_action
from idle import start_idle_mode
from presentation import light_up_group

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        select_spin = GPIO.input(17)
        select_idle_mode = GPIO.input(27)
        select_presentation_mode = GPIO.input(22)
        print(f"Spin: {select_spin}, Idle: {select_idle_mode}, Presentation: {select_presentation_mode}")

        if select_spin == False:
            print('Spin selected')
            first_led_index = start_spin()
            spin_action(first_led_index)
            time.sleep(0.2)
        if select_idle_mode == False:
            print('Idle Mode Selected')
            start_idle_mode()
            time.sleep(0.2)
        if select_presentation_mode == False:
            print('Presentation Mode Selected')
            light_up_group()
            time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("All LEDs OFF")

# Add this code after the while loop
if any(pixels):
    pixels.fill((0, 0, 0))
    pixels.show()

