from PIL import ImageGrab
import win32gui
import os
import time
import cv2
import pyautogui

def screenGrab():
    box = ()
    im = ImageGrab.grab()
    for i in range(3):
        im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
        im.show()

def main():
    screenGrab()

if __name__ == '__main__':
    main()
