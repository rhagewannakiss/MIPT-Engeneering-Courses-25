import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]


def dec2bin(num):
    return [(num >> 1) & 1 for i in range (7, -1, -1)]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

sec = 10

period = sec / 256

#start_time = time.time()
#for i in range(256):
#    print("number:", i, "bin:", dec2bin(i), "voltage: ", i / 256.0 * 3.3)
#    elapsed_time = time.time() - start_time
#    target_time = (i + 1) * (period)
#    sleep_duration = max(target_time - elapsed_time, 0)

#    time.sleep(sleep_duration)


try:
    while True:
        num = input("Enter a number from 0 to 255:\n")
        try:
            num = float(num)
            if num % 1.0 != 0:
                print("Enter an integer!\n")
            elif 0 <= num <= 255:
                GPIO.output(dac, dec2bin(int(num)))

                voltage = num / 256.0 * 3.3

                print(f"Output voltage is approximately {voltage:.4} volt\n")
            else:
                if num < 0:
                    print("Number have to be >=0! Try again...\n")
                elif num > 255:
                    print("Number is out of range [0, 255]! Try again...\n")
        except Exception:
            if num == "q": break
            print("You have to type a number, not string! Try again...\n")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("End of programm!\n")
