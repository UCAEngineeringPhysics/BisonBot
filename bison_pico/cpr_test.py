"""
Use this script to verify encoder's CPR (~2048).
Parts:
    Quadrature Rotary Encoder: YUMO E6B2-CWZ3E (https://www.robotshop.com/products/6mm-rotary-encoder-1024-p-r)
    DC Motor (for electric wheelchair)
Wiring:
    Pico: Micro-USB         -->     Computer: USB
    Encoder: Brown (VCC)    -->     Pico: VBUS
    Encoder: Blue (GND)     -->     Pico: GND
    Encoder: Black (A)      -->     Pico: GPIO10
    Encoder: White (B)      -->     Pico: GPIO11
Count encoder triggers:
    1. Run this script.
    2. Manually rotate the wheel and observe how many times the encoders are triggered.
"""
from machine import Pin

# SETUP
a_pin = Pin(10, Pin.IN, Pin.PULL_DOWN)
b_pin = Pin(11, Pin.IN, Pin.PULL_DOWN)
trig_counts = 0 
def inc_counts(pin):
    global trig_counts
    trig_counts += 1
a_pin.irq(trigger=Pin.IRQ_RISING, handler=inc_counts)
b_pin.irq(trigger=Pin.IRQ_RISING, handler=inc_counts)

# LOOP
while True:
    from time import sleep
    print(trig_counts)
    sleep(0.01)