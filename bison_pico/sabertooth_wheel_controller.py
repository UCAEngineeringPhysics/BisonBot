from machine import Pin, UART, Timer
from math import pi

class WheelController:
    def __init__(self, enca_id: int, encb_id: int, motor_id: str = 'M1') -> None:
        self.motor_id = motor_id
        self.sabertooth_bridge = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
        self.ENCA_PIN = Pin(enca_id, Pin.IN, Pin.PULL_DOWN)
        self.ENCB_PIN = Pin(encb_id, Pin.IN, Pin.PULL_DOWN)
        self.ENCA_PIN.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING, handler=self.inc_counts)
        # self.ENCB_PIN.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING, handler=self.inc_counts)
        # Properties
        self.WHEEL_RADIUS = 0.127  # m, diameter is 10"
        self.GEAR_RATIO = 32
        self.CPR = 1024
        self.K_P = 0.2
        self.K_I = 0.
        self.K_D = 0.
        # Variables
        self.wdir = 0  # wheel direction: 1: forward
        self.enc_counts = 0
        self.prev_enc_counts = 0
        self.lin_vel = 0.
        self.duty = 0.
        self.err = 0.
        self.prev_err = 0.
        self.err_sum = 0.
        self.ref_vel = 0.
        # Velocity monitor timer
        # self.monitor_timer = Timer()
        # self.monitor_timer.init(freq=100, callback=self.mon_cb)
        # # velocity controller timer
        # self.controller_timer = Timer()
        # self.controller_timer.init(freq=100, callback=self.con_cb)

    def inc_counts(self, pin):
        self.enc_counts += self.wdir

    # def mon_cb(self, timer):
    #     enc_diff = self.enc_counts - self.prev_enc_counts
    #     omega_m = enc_diff / self.CPR * 2 * pi * 100 # angular velocity on motor shaft (rad / s)
    #     omega_w = omega_m / self.GEAR_RATIO
    #     self.lin_vel = omega_w * self.WHEEL_RADIUS
    #     self.prev_enc_counts = self.enc_counts

    # def con_cb(self, timer):
    #     self.err = self.ref_vel - self.lin_vel
    #     self.err_sum += self.err  # err_sum = err_sum + err
    #     self.err_diff = self.err - self.prev_err
    #     self.prev_err = self.err
    #     duty_inc = self.K_P * self.err + self.K_I * self.err_sum + self.K_D * self.err_diff  # Proportional, Integral, Derivative
    #     self.duty += duty_inc
    #     if self.duty > 0:  # forward
    #         if self.duty >= 1:
    #             self.duty = 0.999
    #         self._forward(self.duty)
    #     elif self.duty < 0:  # backward
    #         if self.duty <= -1:
    #             self.duty = -0.999
    #         self._backward(-self.duty)
    #     else:
    #         self.stop()
    #     if self.ref_vel == 0:
    #         self.dc = 0.
    #         self.stop()

    def set_vel(self, target_vel):
        if target_vel is not self.ref_vel:
            self.ref_vel = target_vel
            self.err_sum = 0.

    def _set_duty(self, duty: float = 0.0):
        """
        Sabertooth's dutycycle range: [-2047, 2047].
        Map that to [-1, 1]
        """
        assert -1.<=duty<= 1.
        self.sabertooth_bridge.write(bytes(f"{self.motor_id}: {int(duty*2047)}\r\n".encode('utf-8')))
        if duty > 0:
            self.wdir = 1
        elif duty < 0:
            self.wdir = -1
        else:
            self.wdir = 0

    def _stop(self):
        self.sabertooth_bridge.write(bytes(f"{self.motor_id}: 0\r\n".encode('utf-8')))
        self.wdir = 0 

    def halt(self):
        self._stop()
        self.wdir = 0 

# TEST
if __name__ == '__main__':
    from time import sleep
    lwh = WheelController(2, 3)
    rwh = WheelController(4, 5, motor_id='M2')

    for d in range(40):
        lwh._set_duty(duty=d/40)
        # rwh._set_duty(duty=d/100)
        # print(lwh.enc_counts, rwh.enc_counts)
        # print(lwh.lin_vel, rwh.lin_vel)
        sleep(0.1)
    # print(lwh.enc_counts, rwh.enc_counts)
    # for d in reversed(range(40)):
        # lwh._set_duty(duty=d/40)
        # rwh._set_duty(duty=d/100)
        # print(lwh.enc_counts, rwh.enc_counts)
        # print(lwh.lin_vel, rwh.lin_vel)
        # sleep(0.1)
    # print(lwh.enc_counts, rwh.enc_counts)
    # for d in range(0, -40, -1):
        # lwh._set_duty(duty=d/40)
        # rwh._set_duty(duty=d/100)
        # print(lwh.enc_counts, rwh.enc_counts)
        # print(lwh.lin_vel, rwh.lin_vel)
        # sleep(0.1)
    # print(lwh.enc_counts, rwh.enc_counts)
    # for d in reversed(range(0, -40, -1)):
    #     lwh._set_duty(duty=d/40)
        # rwh._set_duty(duty=d/100)
        # print(lwh.enc_counts, rwh.enc_counts)
        # print(lwh.lin_vel, rwh.lin_vel)
    #     sleep(0.1)
    # print(lwh.enc_counts, rwh.enc_counts)

    # lwh.set_vel(-0.44)
    # rwh.set_vel(-0.4)
    # for _ in range(400):
    #     print(lwh.lin_vel, rwh.lin_vel)
    #     sleep(0.01)
    # for d in range(10):
    #     lwh.set_vel(d/10)
    #     rwh.set_vel(d/10)
    #     print(lwh.lin_vel, rwh.lin_vel)
    #     sleep(0.5)
    # print(lwh.lin_vel, rwh.lin_vel)
    # for d in reversed(range(10)):
    #     lwh.set_vel(d/10)
    #     rwh.set_vel(d/10)
    #     print(lwh.lin_vel, rwh.lin_vel)
    #     sleep(0.5)
    # print(lwh.lin_vel, rwh.lin_vel)
    # for d in range(10):
    #     lwh.set_vel(-d/10)
    #     rwh.set_vel(-d/10)
    #     print(lwh.lin_vel, rwh.lin_vel)
    #     sleep(0.5)
    # print(lwh.lin_vel, rwh.lin_vel)
    # for d in reversed(range(10)):
    #     lwh.set_vel(-d/10)
    #     rwh.set_vel(-d/10)
    #     print(lwh.lin_vel, rwh.lin_vel)
    #     sleep(0.5)
    # print(lwh.lin_vel, rwh.lin_vel)
    # lwh.controller_timer.deinit()
    # rwh.controller_timer.deinit()

    lwh._stop()
    rwh._stop()
    lwh.halt()
    rwh.halt()