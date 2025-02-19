import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(26, GPIO.IN)

while True:
  GPIO.output(24, GPIO.input(26))
  
