import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def dec2bin(num): 
    return [int(num >> (7 - i)) & 1 for i in range (8)]

try:
    period = float(input("Enter a period of sygnal: "))
    while True:
        x = 0
        while(x <= 255):
            GPIO.output(dac, dec2bin(x))
            x = x + 1
            sleep(period/512)
            print("num:", x, "voltage: ", x/256.0 * 3.3)
        x = x - 1
        while(x >= 0):
            GPIO.output(dac, dec2bin(x))
            x = x - 1
            sleep(period/512)
        else: break

except Exception:
    print("Enter a number!")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("End Of Programm!")
