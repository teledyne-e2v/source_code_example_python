#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:13:58 2023

@author: teledyne

This code show how to use GPIO on Jetson Nano
"""

import RPi.GPIO as GPIO
import time

output_pin = 12  # BOARD pin 12

def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT)   # you can set initial state with the argument : initial=GPIO.HIGH

    print("Starting demo now! Press CTRL+C to exit")
    tension = GPIO.HIGH
    
    frequency=10
    
    try:
        while True: 
            time.sleep(1/(2*frequency)) #With this sleep the frequency should be 1Hz
            GPIO.output(output_pin, tension)
            tension ^= GPIO.HIGH # set to opposit value.
    finally:
        GPIO.cleanup() # clean GPIO when ended

if __name__ == '__main__':
    main()

