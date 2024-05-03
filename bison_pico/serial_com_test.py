from machine import UART, Pin
from time import sleep

uart0 = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))
l = Pin('LED', Pin.OUT)

i = 0
while True:
    l.value(1)
    tx_str = f"Hellow from Pico: {i}"
    uart0.write(bytes(f"Hello from Pico: {i}\n\r".encode('utf-8')))
    i += 1
    sleep(0.25)
    l.value(0)
    sleep(0.25)