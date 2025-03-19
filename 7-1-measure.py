import RPi.GPIO as GPIO
import time as t
import matplotlib.pyplot as plt

dac     = [26, 19, 13, 6, 5, 11, 9, 10]
leds    = [21,20,16,12,7,8,25,24]
comp    = 4
troyka  = 17

vt=[]
st=t.time()

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = 0)

def binarize(number):
    return [int(i) for i in bin(number)[2:].zfill(8)]

def adc_sar():
    value=127
    for i in range(-6,1):
        i=-i
        GPIO.output(dac,binarize(value))

        t.sleep(0.005)
        
        if GPIO.input(comp):value+=(2**i)
        else:value+=-(2**i)
    
    return value

def led_ind(value):
    GPIO.output(leds,binarize(value))
    
try:
    GPIO.output(troyka,1)
    mes=0                                                                                                                                 
    while mes<46:
        mes=adc_sar()
        vt.append(mes)
        print (mes)
        #led_ind(mes)
    GPIO.output(troyka,0)
    print('pазрядка')
    for i in range(0,2000):
        mes=adc_sar()
        vt.append(mes)
        print (mes)
        #print(str(mes))
except KeyboardInterrupt:
    pass

GPIO.output(troyka,GPIO.LOW)
GPIO.output(dac,GPIO.LOW)
GPIO.cleanup()

vts=""
for i in vt:
    vts=vts+(str(i)+"\n")

with open("data.txt","w") as data:
    data.write(vts)
with open("settings.txt","w") as data:
    data.write("Freq=1000, Step=13")
    
print('Общая продолжительность эксперимента: '+str(t.time()-st)+"c")
print("период одного измерения: 1мс")
print("Средняя частота дискретизации: 1кГц")
print("Шаг квантования АЦП: 13мВ")
    
plt.plot([i for i in range(0,len(vt))],[(i/255)*3.3 for i in vt],c="blue")
plt.grid()
plt.show()
