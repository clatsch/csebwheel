import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)

try:
    while True:
        select_spin = GPIO.input(17)
        select_idle_mode = GPIO.input(27)
        select_presentation_mode = GPIO.input(22)
        print(f"Spin: {select_spin}, Idle: {select_idle_mode}, Presentation: {select_presentation_mode}")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO cleanup complete.")
