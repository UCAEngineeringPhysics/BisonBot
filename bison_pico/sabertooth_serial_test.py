from machine import UART, Pin
from time import sleep

uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
l = Pin('LED', Pin.OUT)

i = 0
for i in range(20):
    l.value(1)
    uart0.write(bytes("M1: -1024\r\n".encode('utf-8')))
    uart0.write(bytes("M2: -1024\r\n".encode('utf-8')))
    i += 1
    sleep(0.25)
    l.value(0)
    sleep(0.25)
uart0.write(bytes("M1: 0\r\n".encode('utf-8')))
uart0.write(bytes("M2: 0\r\n".encode('utf-8')))
