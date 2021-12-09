import RPi.GPIO as GPIO
import time
from datetime import datetime



def water_plants(pin_value):
    '''turns on water pump'''
    GPIO.output(pin_value, GPIO.LOW)

def off_water(pin_value):
    '''turns off water pump'''
    GPIO.output(pin_value, GPIO.HIGH)
    
    
    