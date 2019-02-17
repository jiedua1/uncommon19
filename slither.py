import cv2
import datetime
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
    global WIDTH, HEIGHT, CENTER
    image = cv2.cvtColor(np.array(Image.open(file)), cv2.COLOR_RGB2BGR)
    HEIGHT, WIDTH = image.shape[:2]
    CENTER = np.array([WIDTH / 2, HEIGHT / 2])
    return image


def open_game(url):
    webbrowser.open(url)
    time.sleep(2)
    pyautogui.press('f11')
    time.sleep(5)
    play = pyautogui.locateCenterOnScreen('play.png')
    pyautogui.click(play)


def move_mouse(position):
    pyautogui.click(*position)


def grab_screen():
    image = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    return image


def process_image(image, threshold):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret, threshold_image = cv2.threshold(image, 65, 255, cv2.THRESH_BINARY)
    threshold_image[int(0.85*HEIGHT): , int(0.9*WIDTH):] = 0
    threshold_image[int(0.93*HEIGHT):, :int(0.1*WIDTH)] = 0
    threshold_image[:int(0.34*HEIGHT), int(0.8*WIDTH):] = 0
    return cv2.bitwise_not(threshold_image)


def save_image(image, name):
    cv2.imwrite(name, image)


def detect_blobs(image):
    is_v2 = cv2.__version__.startswith("2.")
    detector = cv2.SimpleBlobDetector() if is_v2 else cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(image)
    positions = [np.array([marker.pt[0], marker.pt[1]]) for marker in keypoints]
    sizes = [marker.size for marker in keypoints]
    return positions, sizes


def get_best_position(positions, sizes):
    position = min(positions, key=lambda position: np.linalg.norm(position - CENTER))
    return position


def run_slither_bot(threshold, iterations):
    open_game(URL)
    for i in range(iterations):
        image = process_image(grab_screen(), threshold)
        oldTime = datetime.datetime.now()
        positions, sizes = detect_blobs(image)
        if positions:
            best_position = get_best_position(positions, sizes)
            move_mouse(best_position)
        else:
            pass
        print(datetime.datetime.now() - oldTime)


if __name__=="__main__":
    run_slither_bot(65, 100)
