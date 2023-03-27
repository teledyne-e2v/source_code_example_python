#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:13:58 2023

@author: teledyne
"""

import RPi.GPIO as GPIO
import time

output_pin = 18  # BCM pin 18, BOARD pin 12

def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT)   # you can set initial state with the argument : initial=GPIO.HIGH

    print("Starting demo now! Press CTRL+C to exit")
    tension = GPIO.HIGH
    try:
        while True:
            time.sleep(0.5)
            GPIO.output(output_pin, tension)
            tension ^= GPIO.HIGH # set to opposit value.
    finally:
        GPIO.cleanup() # clean GPIO when ended

if __name__ == '__main__':
    main()
