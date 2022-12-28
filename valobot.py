import cv2
import os
from mss import mss
import numpy as np
import win32api
import serial
import time
import keyboard
import winsound

os.system("color d")                        #useless
os.system("cls")                            #useless
print("Version : 0.1              ")        #useless
print("")                                   #useless
print("Made by Hustensaft       ")          #useless
print("")                                   #useless
print("Choose your settings")               #useless
print("")                                   #useless

fov = int(input("FOV: "))
print("")
 
sct = mss()
 
 
arduino = serial.Serial('COM3', 115200)     #change the COM3 to your arduinos COM
 
screenshot = sct.monitors[1]
screenshot['left'] = int((screenshot['width'] / 2) - (fov / 2))
screenshot['top'] = int((screenshot['height'] / 2) - (fov / 2))
screenshot['width'] = fov
screenshot['height'] = fov
center = fov/2

embaixo = np.array([140,111,160]) #highest color 
emcima = np.array([148,154,194]) # lowest color

speed = float(input("SPEED: "))     #speed for the moving of your crosshair
print("")
print("You are ready to go ")
print("")
print("Enjoy your day ! ")
print("")
current_time = time.strftime("    %H:%M:%S    ")        #current time of your system
print("The time is", current_time)
print("")

 
def mousemove(x):
    if x < 0: 
        x = x+256 
 
    pax = [int(x)]
    arduino.write(pax)
 




toggle = False

while True:
        if keyboard.is_pressed("f9"):
                toggle = not toggle
                frequency = 1500
                duration = 100
                winsound.Beep(frequency, duration)
                print("Toggle is ", toggle)
                time.sleep(1)

        if( toggle ):
            img = np.array(sct.grab(screenshot))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, embaixo,emcima)
            kernel = np.ones((3,3), np.uint8)
            dilated = cv2.dilate(mask,kernel,iterations= 5)
            thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(contours) != 0:
                mouse = cv2.moments(thresh)
                pixel = (int(mouse["m10"] / mouse["m00"]), int(mouse["m01"] / mouse["m00"]))
                aimzao = pixel[0] + 2
                diff_x = int(aimzao - center)
                alvo = diff_x * speed
                mousemove(alvo)

        #performance delay
        time.sleep(0.01) 