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

led = [24, 25, 8, 7, 12, 16, 20, 21]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT, initial = 0)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

def adc():
    volumes = [0, 1, 3, 7, 15, 31, 63, 127, 255]
    d = [i*32 for i in range(9)]
    result = 0

    check = [ 0 for i in range(8)]

    for i in range(8):
        check[i] = 1
        GPIO.output(dac,check)
        sleep(0.001)

        if GPIO.output(comp) == 0:
            result += 2**(7-i)
        else:
            check[i] = 0

    volumes_d = [abs(i-result) for i in d]
    print(result, volumes_d)

    return volumes[volumes_d.index(min(volumes_d))]

try:
    while True:
        GPIO.output(led, dec2bin(adc()))
        print(adc())

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()

b01-403@raspberrypi:~/scripts $ /bin/python3 /home/b01-403/scripts/йоу/5-3.py
b01-403@raspberrypi:~/scripts $ /bin/python3 /home/b01-403/scripts/йоу/5-3.py
b01-403@raspberrypi:~/scripts $ /bin/python3 /home/b01-403/scripts/йоу/5-3.py
Traceback (most recent call last):
  File "/home/b01-403/scripts/йоу/5-3.py", line 44, in <module>
    GPIO.output(led, dec2bin(adc()))
  File "/home/b01-403/scripts/йоу/5-3.py", line 32, in adc
    if GPIO.output(comp) == 0:
TypeError: function takes exactly 2 arguments (1 given)

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led = [24, 25, 8, 7, 12, 16, 20, 21]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT, initial=0)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

def adc():
    check = [0] * 8
    result = 0

    for i in range(8):
        check[i] = 1
        GPIO.output(dac, check)
        sleep(0.001)
        
        # Исправлено: GPIO.input() вместо GPIO.output()
        if GPIO.input(comp) == 0:
            result += 2**(7 - i)
        else:
            check[i] = 0

    volumes = [0, 32, 64, 96, 128, 160, 192, 224, 255]
    closest = min(volumes, key=lambda x: abs(x - result))
    return closest

try:
    while True:
        value = adc()
        GPIO.output(led, dec2bin(value))
        print(value)

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()