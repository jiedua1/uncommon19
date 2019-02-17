import cv2
import datetime
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyautogui
import time
import webbrowser
import snake_detection


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
    time.sleep(5)
    pyautogui.press('f11')
    time.sleep(1)
    pyautogui.press('enter')


def move_mouse(position):
    pyautogui.click(*position)


def grab_screen():
    image = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    return image


def process_image(image, threshold):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret, threshold_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    threshold_image[int(0.85*HEIGHT): , int(0.9*WIDTH):] = 0
    threshold_image[int(0.93*HEIGHT):, :int(0.1*WIDTH)] = 0
    threshold_image[:int(0.34*HEIGHT), int(0.8*WIDTH):] = 0
    return cv2.bitwise_not(threshold_image)


def save_image(image, name):
    cv2.imwrite(name, image)

#Return: float array positions, int array size
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


def draw_marker(image, position):
    return cv2.drawMarker(image, (int(position[0]), int(position[1])),
        color = 128, markerType = cv2.MARKER_CROSS, markerSize = HEIGHT // 30, thickness = 5)

def run_slither_bot(threshold, iterations):
    open_game(URL)
    delta_time = 0 #time it took for last iteration
    for i in range(iterations):
        image = process_image(grab_screen(), threshold)
        oldTime = datetime.datetime.now()
        positions, sizes = detect_blobs(image)
        old_mouse_position = None

        if positions:
            best_position = get_best_position(positions, sizes)

            #limit angular velocity
            new_vector = best_position - CENTER
            last_vector = old_mouse_position - CENTER

            #adjust for lag... about 4 seconds to go across width of screen
            velocity = WIDTH / 8
            #how much the snake has moved in the meantime
            snake_delta = np.array([0,0])
            best_position -= snake_delta #account for the snake movement

            
            #AVOID SNAKES IF WE SEE ONE:
            num_labels, labels, stats, centroids = snake_detection.find_snakes(image, positions)
            valid_snake_ids = []
            for i in range(1, num_labels):
                if stats[i][4] > WIDTH * WIDTH / 1000: #~10000 pixels, big snek
                    valid_snake_ids.append(i)

            not_too_close_ids = []
            not_too_close_values = [] #closest snakes that are not too close to our snake (to avoid the own snake)
            for i in range(len(valid_snake_ids)):
                position = centroids[valid_snake_ids[i]]
                if np.linalg.norm(position - CENTER) > WIDTH/8:
                    not_too_close_ids.append(valid_snake_ids[i])
                    not_too_close_values.append(position)

            if len(not_too_close_ids) > 0:
                not_too_close_distances = [np.linalg.norm(vec) for vec in not_too_close_values]
                closest_snake_pos = not_too_close_values[np.argmin(not_too_close_distances)]
                curVec = best_position - CENTER #current direction vector
                dirToSnake = closest_snake_pos - CENTER
                if np.dot(curVec, dirToSnake) < 0:
                    best_position = CENTER-dirToSnake

            move_mouse(best_position)
            image = draw_marker(image, best_position)
            #save_image(image, "{}.png".format(i))
            delta_time = (datetime.datetime.now() - oldTime).total_seconds()
            print(delta_time)
            old_mouse_position = best_position
        

if __name__=="__main__":
    run_slither_bot(65, 80)
