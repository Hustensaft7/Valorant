# Valorant Cheat
a very simple color aimbot wich works with an Arduino Leonardo and a Host-shield

## code explanation:

### Imports:
````python
import cv2
import os
from mss import mss
import numpy as np
import win32api
import serial
import time
import keyboard
import winsound
````
imports all libarys that our program needs to function.

### setup code:
````python
os.system("color d")
os.system("cls")
print("Version : 0.1              ")
print("")
print("Made by Hustensaft       ")
print("")
print("Choose your settings")
print("")
````
basically useless code for other print color, version and a small made by.



### FOV and Serial connection for the Arduino:
````Python
fov = int(input("FOV: "))
print("")
 
sct = mss()
 
 
arduino = serial.Serial('COM3', 115200)
````
FOV is used to calculate the square in wich the cheat functions. The arduino connects to COM§ with a speed of 115200 Bits per sec. You can get your information about your arduino in the device manager.

### screen capture:

````python
screenshot = sct.monitors[1]
screenshot['left'] = int((screenshot['width'] / 2) - (fov / 2))
screenshot['top'] = int((screenshot['height'] / 2) - (fov / 2))
screenshot['width'] = fov
screenshot['height'] = fov
center = fov/2
````
basically calculates the middle of your screen with the FOV you typed in earlyer.

### Color setup: 

````python
embaixo = np.array([140,111,160])
emcima = np.array([148,154,194])
````
highest to lowest possible color for the bot the aim at. 
**changeble but may cause problems**

### mouse speed + spare text:
````python
speed = float(input("SPEED: "))
print("")
print("You are ready to go ")
print("")
print("Enjoy your day ! ")
print("")
current_time = time.strftime("    %H:%M:%S    ")
print("The time is", current_time)
print("")

````
creates a float for speed and wishes you a nice day and displays the current sytsem time.

### define mouse for arduino:

````python
def mousemove(x):
    if x < 0: 
        x = x+256 
 
    pax = [int(x)]
    arduino.write(pax)
 
````
defines mouse and adds if 256 if x cordinat is below 0 wich should not happen.

### Toggle for the actual mechanism:
````python
toggle = False

while True:
        if keyboard.is_pressed("f9"):
                toggle = not toggle
                frequency = 1500
                duration = 100
                winsound.Beep(frequency, duration)
                print("Toggle is ", toggle)
                time.sleep(1)
````
toggles the cheat after **F9** is pressed once.

### Actual mechanism of the cheat:

````python
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

        time.sleep(0.01) 
````
Grabs the screenshots translates colors from BGR into HSV trys to find a color wich is between our pre-set color values, if these where found in the screenshot it will move the mouse with the pre-set speed of x to the color. **If the speed is to slow for your sense it will not work same as with to fast**