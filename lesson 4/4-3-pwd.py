import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)



n = 10
p = GPIO.PWM(24, 1000)
p.start(0)

try:
    while True:
        print("Enter value:  \n")
        f = input()
        if f == "q": 
            break
        f = int(f)
        p.ChangeDutyCycle(f)

        print(3.3*f/100)

finally:
    p.stop()
    GPIO.output(24, 0)
    GPIO.cleanup()
    print("End Of programm!")

