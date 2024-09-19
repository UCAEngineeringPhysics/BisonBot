from machine import Pin, PWM
from time import sleep

# SETUP
INA1 = Pin(14, Pin.OUT)
INA2 = Pin(15, Pin.OUT)
PWMA = PWM(Pin(13))
PWMA.freq(1000)
INB1 = Pin(16, Pin.OUT)
INB2 = Pin(17, Pin.OUT)
PWMB = PWM(Pin(18))
PWMB.freq(1000)

def stop_A():
    PWMA.duty_u16(0)
    INA1.low()
    INA2.low()

def forward_A(duty):
    INA1.high()
    INA2.low()
    PWMA.duty_u16(duty)

def backward_A(duty):
    INA1.low()
    INA2.high()
    PWMA.duty_u16(duty)

def stop_B():
    PWMB.duty_u16(0)
    INB1.low()
    INB2.low()

def forward_B(duty):
    INB1.high()
    INB2.low()
    PWMB.duty_u16(duty)

def backward_B(duty):
    INB1.low()
    INB2.high()
    PWMB.duty_u16(duty)

# LOOP
for d in range(65):
    forward_A(d*1000)
    forward_B(d*1000)
    sleep(0.1)
for d in reversed(range(65)):
    forward_A(d*1000)
    forward_B(d*1000)
    sleep(0.1)
for d in range(65):
    backward_A(d*1000)
    backward_B(d*1000)
    sleep(0.1)
for d in reversed(range(65)):
    backward_A(d*1000)
    backward_B(d*1000)
    sleep(0.1)
stop_A()