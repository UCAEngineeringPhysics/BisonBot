"""
Use this script to estimate wheel's speed.
Parts:
    Quadrature Rotary Encoder: YUMO E6B2-CWZ3E (https://www.robotshop.com/products/6mm-rotary-encoder-1024-p-r)
    DC Motor (from electric wheelchair)
    Motor Driver Board (Optional): Cytron MD20A
Wiring:
    Pico: Micro-USB         -->     Computer: USB
    Encoder: Brown (VCC)    -->     Pico: VBUS
    Encoder: Blue (GND)     -->     Pico: GND
    Encoder: Black (A)      -->     Pico: GPIO13
Count encoder triggers:
    1. Run this script.
    2. Power up motor with a battery (12V - 24V) and watch the estimated speed.
    2. (Alternative) Press "MA" or "MB" button on the motor driver board and watch the estimated speed 
"""
from machine import freq, Pin, Timer
freq(125000000)  # default 125000000 Hz, or 125 MHz
print(f"CPU speed: {freq()} Hz")

# SETUP
enc_pin = Pin(18, Pin.IN)
trig_counts = 0 
def inc_counts(pin):
    global trig_counts
    trig_counts += 1
enc_pin.irq(trigger=Pin.IRQ_RISING, handler=inc_counts)

speed = 0.
prev_trig_counts = 0
# TIMER WILL SCREW UP EVERYTHING!
# def comp_speed(timer):
#     global trig_counts
#     global prev_trig_counts
#     global speed 
#     speed = (trig_counts - prev_trig_counts) * 100.
#     prev_trig_counts = trig_counts
# speed_monitor_timer = Timer()
# speed_monitor_timer.init(mode=Timer.PERIODIC, freq=100, callback=comp_speed)

# LOOP
from time import sleep
while True:
    speed = (trig_counts - prev_trig_counts) * 100.  # counts per second
    prev_trig_counts = trig_counts
    print(speed)
    sleep(0.01)