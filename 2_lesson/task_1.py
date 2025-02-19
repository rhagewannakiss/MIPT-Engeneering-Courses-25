import RPi.GPIO as g
import time

leds = [3, 2, 4, 17, 27, 22, 10, 9]

g.setmode(g.BCM)
g.setup(leds, g.OUT)

while True:
    for i in range(3):
        for j in range(8):
            g.output(leds[j], 1)
          time.sleep(0,1)
      g.output(leds[j], 0)

g.output(leds, 0)
g.cleanup()
