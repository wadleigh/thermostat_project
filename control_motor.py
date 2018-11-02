import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
stepPin=31
directionPin=33
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(directionPin, GPIO.OUT)
GPIO.output(stepPin, 0)
GPIO.output(directionPin, 0)

stepsInRot=200
amountToTurn=0.25
numSteps=round(stepsInRot*amountToTurn)

for i in range(numSteps):
  GPIO.output(stepPin, 1)
  time.sleep(0.001)
  GPIO.output(stepPin, 0)
  time.sleep(0.001)
GPIO.cleanup()