import ftrobopy as ft
from time import sleep
import numpy as np


def rotate(txt, motor, angle, speed=512):
    impulses = int(round(abs(angle)/5))
    txt.SyncDataBegin()
    motor.setSpeed(speed * np.sign(angle))
    motor.setDistance(impulses)
    txt.SyncDataEnd()

    while not motor.finished():
        txt.updateWait()


txt = ft.ftrobopy('auto')
txt.startOnline()

motor = txt.motor(1)

while True:
    rotate(txt, motor, 45, 32)
    sleep(1)

    rotate(txt, motor, -90, 32)
    sleep(1)

    rotate(txt, motor, 45, 32)
    sleep(1)
