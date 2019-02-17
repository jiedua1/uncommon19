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
        height = image.shape[0]
        width = image.shape[1]

        grayimg = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        image_name = os.getcwd() + '\\snap__' + str(int(time.time())) + '.png'
        """
        plt.ion()
        im.show()
        """

        #process the image using thresholding, 85 color value works well for nibbles
        ret, thres_img = cv2.threshold(grayimg, 65, 255, cv2.THRESH_BINARY)
        #gaussian thresholding doesn't work well because it has the hexagons
        #thres_img = cv2.adaptiveThreshold(grayimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        #block out the map and current score in the thresholded image (hardcoded proprtions)
        thres_img[int(0.85*height):height , int(0.9*width):width] = 0
        thres_img[int(0.93*height):height, 0:width//10] = 0
        thres_img[0:int(0.34*height), int(0.8*width):width] = 0


        #now find the blobs that are approximately the size of nibbles

        # Setup SimpleBlobDetector parameters.
        """
        params = cv2.SimpleBlobDetector_Params()
        params.minThreshold = 200
        params.maxThreshold = 255
        params.filterByArea = False
        """

        #invert image
        thres_img = cv2.bitwise_not(thres_img)

        #syntax depends on opencv version...
        is_v2 = cv2.__version__.startswith("2.")
        if is_v2:
            detector = cv2.SimpleBlobDetector()
        else:
            detector = cv2.SimpleBlobDetector_create()

        keypoints = detector.detect(thres_img)
        #im_with_keypoints = cv2.drawKeypoints(thres_img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #drawKeypoints is broken in opencv 4.0
        im_with_keypoints = thres_img.copy()

        for marker in keypoints:
            print(marker.pt)
            im_with_keypoints = cv2.drawMarker(im_with_keypoints, tuple(int(i) for i in marker.pt), color=128, markerType = cv2.MARKER_CROSS, markerSize = height//30, thickness = 5)

        cv2.imshow("Keypoints", im_with_keypoints)
        cv2.waitKey(0)

        cv2.imwrite(image_name, thres_img)
    #print(datetime.datetime.now() - oldTime)

def main():
    screenGrab()

if __name__ == '__main__':
    main()
