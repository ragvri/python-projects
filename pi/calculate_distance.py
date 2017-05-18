import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
from time import sleep

TRIG = 23
ECHO = 24

print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


while True :
  GPIO.output(TRIG, False)

  GPIO.output(TRIG, True)
  sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150

  distance = round(distance, 2)

  print (distance)

  sleep(1)

GPIO.cleanup()
