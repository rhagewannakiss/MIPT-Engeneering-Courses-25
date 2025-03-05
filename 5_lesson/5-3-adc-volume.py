import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11,  9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    return [int(elem) for elem in bin(num)[2:].zfill(8)]

def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2**i
        dac_val = dec2bin(k)
        GPIO.output(dac, dac_val)
        sleep(0.01)
        comp_val = GPIO.input(comp)
        print("i: ", i, "k:  ", k, "bin:  ", dac_val, "comp val: ", comp_val)
        if comp_val == 0:
            k -= 2**i
            print("k: ", k)
    return k

def Volume(val):
    val = int(val/256*10)
    print("value: ", val)
    arr = [0]*8
    for i in range(val - 1):
        arr[i] = 1
    return arr

try:
    while True:
        i = adc()
        if i:
            volume_val = Volume(i)
            GPIO.output(led, volume_val)
            print(int(i/256*10))
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")


...
i:  3 k:   8 bin:   [0, 0, 0, 0, 1, 0, 0, 0] comp val:  0
k:  0
i:  2 k:   4 bin:   [0, 0, 0, 0, 0, 1, 0, 0] comp val:  0
k:  0
i:  1 k:   2 bin:   [0, 0, 0, 0, 0, 0, 1, 0] comp val:  0
k:  0
i:  0 k:   1 bin:   [0, 0, 0, 0, 0, 0, 0, 1] comp val:  1
value:  0
EOP
Traceback (most recent call last):
  File "/home/b01-403/scripts/йоу/5-3-ADC-volume.py", line 46, in <module>
    GPIO.output(led, volume_val)
RuntimeError: The GPIO channel has not been set up as an OUTPUT


import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

def adc():
    value = 0
    for i in range(7, -1, -1):
        step = value + 2**i
        GPIO.output(dac, dec2bin(step))
        sleep(0.001)
        if GPIO.input(comp) == GPIO.HIGH:
            value = step
    return value

def volume_level(value):
    level = int(value / 256 * 8)
    return [1 if i < level else 0 for i in range(8)]

try:
    while True:
        adc_value = adc()
        leds_state = volume_level(adc_value)
        GPIO.output(led, leds_state)
        voltage = adc_value / 255 * 3.3
        print(f"ADC: {adc_value:3d}, Voltage: {voltage:.2f}V, LEDs: {sum(leds_state)}")

finally:
    GPIO.output(dac, 0)
    GPIO.output(led, 0)
    GPIO.cleanup()
    print("Program terminated")