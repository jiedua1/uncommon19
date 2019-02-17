from PIL import ImageGrab
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import win32gui
import os
import time
import cv2
import pyautogui
import datetime

def screenGrab():
    box = ()
    time.sleep(1)
    #im = ImageGrab.grab()
    im = Image.open(os.getcwd() + '\\full_screenshot.png', mode = 'r')
    #oldTime = datetime.datetime.now()
    for i in range(1):
        image = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        grayimg = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        image_name = os.getcwd() + '\\snap__' + str(int(time.time())) + '.png'
        """
        plt.ion()
        im.show()
        """

        #process the image using thresholding, 85 color value works well for nibbles
        ret, thres_img = cv2.threshold(grayimg, 85, 255, cv2.THRESH_BINARY)
        #thres_img = cv2.adaptiveThreshold(grayimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        cv2.imwrite(image_name, thres_img)
    #print(datetime.datetime.now() - oldTime)

def main():
    screenGrab()

if __name__ == '__main__':
    main()
