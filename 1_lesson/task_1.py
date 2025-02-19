import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

for i in range(18):
  GPIO.output(24, i%2)
  time.sleep(1)
