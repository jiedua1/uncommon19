import cv2
import datetime
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyautogui
from sklearn.cluster import KMeans
import time
import webbrowser


WIDTH, HEIGHT = pyautogui.size()
VALID_DIST = min(WIDTH / 4, HEIGHT / 4)
CENTER = np.array([WIDTH / 2, HEIGHT / 2])
URL = 'http://slither.io'
SNAKE_THRESHOLD = WIDTH ** 2 / 1000
MIN_DIST_TO_YOUR_SNAKE = WIDTH / 10


def load_image(file):
    global WIDTH, HEIGHT, CENTER, SNAKE_THRESHOLD
    image = cv2.cvtColor(np.array(Image.open(file)), cv2.COLOR_RGB2GRAY)
    HEIGHT, WIDTH = image.shape[:2]
    CENTER = np.array([WIDTH / 2, HEIGHT / 2])
    SNAKE_THRESHOLD = WIDTH ** 2 / 1000
    MIN_DIST_TO_YOUR_SNAKE = WIDTH / 8
    return image


def open_game(url):
    webbrowser.open(url)
    time.sleep(3)
    pyautogui.press('f11')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)


def move_mouse(position):
    pyautogui.click(*position)


def grab_screen():
    return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY)


def process_image(image, threshold):
    ret, threshold_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    threshold_image[int(0.85*HEIGHT): , int(0.9*WIDTH):] = 0
    threshold_image[int(0.93*HEIGHT):, :int(0.1*WIDTH)] = 0
    threshold_image[:int(0.34*HEIGHT), int(0.8*WIDTH):] = 0
    return cv2.bitwise_not(threshold_image)


def save_image(image, name):
    cv2.imwrite(name, image)


def detect_blobs(image):
    # set parameters
    params = cv2.SimpleBlobDetector_Params()
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.1

    # Create a detector with the parameters
    is_v2 = cv2.__version__.startswith("2.")
    detector = cv2.SimpleBlobDetector() if is_v2 else cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(image)
    positions = [[marker.pt[0], marker.pt[1]] for marker in keypoints]
    sizes = [marker.size for marker in keypoints]
    return positions, sizes


def detect_snakes(image):
    image = 255 - image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(image)
    closest_snake = [None, None]
    for i in range(num_labels):
        if stats[i][-1] > SNAKE_THRESHOLD and np.linalg.norm(centroids[i]-CENTER) > MIN_DIST_TO_YOUR_SNAKE:
            print(centroids[i])
            if not closest_snake[0] or np.linalg.norm(centroids[i]-CENTER) < np.linalg.norm(closest_snake-CENTER):
                closest_snake = centroids[i]
    print("closest snake", closest_snake)
    return closest_snake


def normalize(position):
    difference_vector = position - CENTER
    norm = np.linalg.norm(difference_vector)
    return difference_vector / norm, norm


def get_best_position(positions, sizes, previous_position, closest_snake):
    if closest_snake[0]:
        return 2 * CENTER - closest_snake
    num_positions = len(positions)
    kmeans = KMeans(n_clusters=int(np.sqrt(num_positions))) \
        .fit(positions, [sizes[i] / np.linalg.norm(positions[i]) for i in range(num_positions)])
    centers = kmeans.cluster_centers_
    index = kmeans.predict([CENTER])[0]
    return centers[index]


    previous_position_norm = np.linalg.norm(previous_position)
    new_position = np.array([0.0, 0.0])
    for position in positions:
        normalized_vector, norm = normalize(position)
        angle_closeness_measure = np.dot(previous_position, normalized_vector) + 4 * previous_position_norm
        new_position += normalized_vector * angle_closeness_measure # / norm

    normalized_new_vector = 200 * new_position / np.linalg.norm(new_position)
    return CENTER + normalized_new_vector


def draw_marker(image, position):
    return cv2.drawMarker(image, (int(position[0]), int(position[1])),
        color = 128, markerType = cv2.MARKER_CROSS, markerSize = HEIGHT // 30, thickness = 5)


def run_slither_bot(threshold, iterations):
    open_game(URL)
    best_position = CENTER + np.array([0,200])
    for i in range(iterations):
        # time1 = datetime.datetime.now()
        image = process_image(grab_screen(), threshold)
        positions, sizes = detect_blobs(image)
        closest_snake = detect_snakes(image)

        if positions:
            best_position = get_best_position(positions, sizes, best_position, closest_snake)
            move_mouse(best_position)
            image = draw_marker(image, best_position)
            save_image(image, "{}.png".format(i))

if __name__=="__main__":
    run_slither_bot(65, 500)

    # positions, sizes = detect_blobs(image)
    # for position in positions:
    #     image = draw_marker(image, position)
    # plt.imshow(image)
    # plt.show()
    # image = load_image('full_screenshot.png')
    # image = process_image(image, 50)
    # closest_snake = detect_snakes(image)
