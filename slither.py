import numpy as np
import pyautogui
import time
import webbrowser

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


if __name__=="__main__":
    open_game(URL)
    while True:
        displacement = np.random.choice([-VALID_DIST, 0, VALID_DIST], 2)
        move_mouse(displacement)
        time.sleep(1)
