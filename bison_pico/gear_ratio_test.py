"""
Use this script to find out the gear ratio of the motor's gear box.
Parts:
    Quadrature Rotary Encoder: YUMO E6B2-CWZ3E (https://www.robotshop.com/products/6mm-rotary-encoder-1024-p-r)
    DC Motor (for electric wheelchair)
Wiring:
    Pico: Micro-USB         -->     Computer: USB
    Encoder: Brown (VCC)    -->     Pico: VBUS
    Encoder: Blue (GND)     -->     Pico: GND
    Encoder: Orange (Z)     -->     Pico: GPIO15
Initialize:
    1. Run this script.
    2. Rotate MOTOR SHAFT (NOT the wheel) manually and slowly, until the encoder count number turns to 1 from 0.
    3. Stop spinning the motor shaft RIGHT AFTER the encoder count number turns to 1.
    4. Tape or mark wheel to a reference structure, so that the zero position can be observed from the wheel.  
Observe Gear Ratio:
    1. Run this script. Make sure the wheel starts at the zero position.
    2. Manually rotate the wheel until a full revolution is done. Record the encoder count number, which is the gear ratio. 
    3. Repeat step 1 and 2 a couple of times and calculate the averaged gear ratio. 
"""
from machine import Pin

# SETUP
z_pin = Pin(15, Pin.IN, Pin.PULL_DOWN)
z_counts = 0 
def count_zeros(pin):
    global z_counts
    z_counts += 1
z_pin.irq(trigger=Pin.IRQ_RISING, handler=count_zeros)

# LOOP
while True:
    from time import sleep
    print(z_counts)
    sleep(0.01)