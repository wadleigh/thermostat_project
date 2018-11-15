#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

#variables to determine rotation
#1 clockwise, 0 counterclockwise (when looking at motor, dial on heater is reversed)
# 0 turns up temp, 1 turns down temp
direction = 0
FracOfRotToTurn = 0.25

#pin number (not GPIO number)
stepPin = 31
directionPin = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(directionPin, GPIO.OUT)
GPIO.output(stepPin, 0)
GPIO.output(directionPin, direction)

stepsInRot = 200
numSteps = int(round(stepsInRot * FracOfRotToTurn))

timeStep = 0.001
for i in range(numSteps):
  GPIO.output(stepPin, 1)
  time.sleep(timeStep)
  GPIO.output(stepPin, 0)
  time.sleep(timeStep)
GPIO.cleanup()
