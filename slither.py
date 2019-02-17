import numpy as np
import matplotlib.pyplot as plt
import pyautogui
import time
import webbrowser


GREYSCALE_VECTOR = [0.299, 0.587, 0.114]
WIDTH, HEIGHT = pyautogui.size()
VALID_DIST = min(WIDTH / 4, HEIGHT / 4)
CENTER = np.array([WIDTH / 2, HEIGHT / 2])
URL = 'http://slither.io'



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


def grab_screen(threshold):
    image = np.dot(np.array(pyautogui.screenshot()), GREYSCALE_VECTOR)
    image = 255 * (image > threshold)
    image[int(0.85*HEIGHT): , int(0.9*WIDTH):] = 0
    image[int(0.93*HEIGHT):, :int(0.1*WIDTH)] = 0
    image[:int(0.34*HEIGHT), int(0.8*WIDTH):] = 0
    return image


def save_image(image, name):
    plt.gray()
    plt.imshow(image)
    plt.savefig("{}.png".format(name))


if __name__=="__main__":
    open_game(URL)
    displacement = np.random.choice([-VALID_DIST, 0, VALID_DIST], 2)
    move_mouse(displacement)
    time.sleep(5)
    image = grab_screen(60)
    save_image(image, 1)
