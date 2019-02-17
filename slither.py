import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyautogui
import time
import webbrowser


WIDTH, HEIGHT = pyautogui.size()
VALID_DIST = min(WIDTH / 4, HEIGHT / 4)
CENTER = np.array([WIDTH / 2, HEIGHT / 2])
URL = 'http://slither.io'


def load_image(file):
    global WIDTH, HEIGHT
    image = cv2.cvtColor(np.array(Image.open(file)), cv2.COLOR_RGB2BGR)
    HEIGHT, WIDTH = image.shape[:2]
    return image


def open_game(url):
    webbrowser.open(url)
    time.sleep(2)
    pyautogui.press('f11')
    time.sleep(5)
    play = pyautogui.locateCenterOnScreen('play.png')
    pyautogui.click(play)


def move_mouse(displacement):
    position = CENTER + displacement
    pyautogui.click(*position)


def grab_screen():
    image = np.array(pyautogui.screenshot())
    return image


def process_image(image, threshold):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret, threshold_image = cv2.threshold(image, 65, 255, cv2.THRESH_BINARY)
    threshold_image[int(0.85*HEIGHT): , int(0.9*WIDTH):] = 0
    threshold_image[int(0.93*HEIGHT):, :int(0.1*WIDTH)] = 0
    threshold_image[:int(0.34*HEIGHT), int(0.8*WIDTH):] = 0
    return cv2.bitwise_not(threshold_image)


def save_image(image, name):
    plt.gray()
    plt.imshow(image)
    plt.savefig("{}.png".format(name))


def detect_blobs(image):
    is_v2 = cv2.__version__.startswith("2.")
    detector = cv2.SimpleBlobDetector() if is_v2 else cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(image)
    im_with_keypoints = image.copy()

    for marker in keypoints:
        print(marker.pt)
        im_with_keypoints = cv2.drawMarker(im_with_keypoints, tuple(int(i) for i in marker.pt), color=128, markerType = cv2.MARKER_CROSS, markerSize = HEIGHT//30, thickness = 5)

    return im_with_keypoints


if __name__=="__main__":
    # open_game(URL)
    # displacement = np.random.choice([-VALID_DIST, 0, VALID_DIST], 2)
    # move_mouse(displacement)
    # time.sleep(5)
    # image = grab_screen(60)
    # save_image(image, 1)
    image = process_image(load_image('full_screenshot.png'), 65)
    im_with_keypoints = detect_blobs(image)
    save_image(im_with_keypoints, 1)
    # save_image(image, 1)
