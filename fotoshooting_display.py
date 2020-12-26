import ftrobopy as ft
from time import sleep, localtime, strftime
import cv2
import numpy as np


class Button():
    OFF = 0
    ON = 1


txt = ft.ftrobopy('auto')
txt.startOnline()
txt.startCameraOnline()

trigger = txt.input(1)

sleep(2.5)
print('Camera is ready')

while trigger.state() == Button.OFF:
    txt.updateWait()

pic = txt.getCameraFrame()

txt.stopCameraOnline()
txt.stopOnline()

pic2 = bytearray(pic)
img = cv2.imdecode(np.frombuffer(pic2), cv2.IMREAD_UNCHANGED)

cv2.imshow('img', img)
cv2.waitKey(0)