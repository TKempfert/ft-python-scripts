import ftrobopy as ft
from time import sleep, localtime, strftime


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
date_str = strftime("%Y-%m-%d_%H-%M-%S", localtime())

txt.stopCameraOnline()
txt.stopOnline()

filename = 'img_' + date_str + '.jpg'

with open(filename,'wb') as f:
   f.write(bytearray(pic))