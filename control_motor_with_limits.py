#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

#variables to determine rotation
#1 clockwise, 0 counterclockwise (when looking at motor, dial on heater is reversed)
# zero turns up temp, 1 turns down temp
direction = 1
FracOfRotToTurn = 0.25
signOfDirection = 1 - direction * 2

#pin number (not GPIO number)
stepPin = 31
directionPin = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(directionPin, GPIO.OUT)
GPIO.output(stepPin, 0)
GPIO.output(directionPin, direction)

curPos = 0
maxPos = 0.75 #It can actually go a little past 0.75 turns, so this is conservative
minPos = 0
hitExtrema = 0

intendedPos = curPos + signOfDirection * FracOfRotToTurn
if intendedPos > maxPos :
  hitExtrema = 1
  intendedPos = maxPos
elif intendedPos < minPos:
  hitExtrema = 1
  intendedPos = minPos

FracOfRotToTurn = (intendedPos - curPos) / signOfDirection 

stepsInRot = 200
numSteps = int(round(stepsInRot * FracOfRotToTurn))

timeStep = 0.001
for i in range(numSteps):
  GPIO.output(stepPin, 1)
  time.sleep(timeStep)
  GPIO.output(stepPin, 0)
  time.sleep(timeStep)
GPIO.cleanup()
