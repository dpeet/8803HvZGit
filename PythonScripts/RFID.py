import time
import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BCM)
GPIO.setup (19, GPIO.OUT)
p = GPIO.PWM(19, 100)
p.start(0)
while 1:
    for x in range(50):
        p.ChangeDutyCycle(x)
        time.sleep(0.1)
    for x in range(50):
        p.ChangeDutyCycle(50-x)
        time.sleep(0.1)
