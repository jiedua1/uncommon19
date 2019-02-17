import cv2
from slither import load_image, process_image, detect_blobs, save_image
import imutils
import numpy as np

#temporary function to test this
def find_snakes_helper(image, threshold):
    bw_image = process_image(image, threshold)
    #First, mask out the blobs 
    positions, sizes = detect_blobs(bw_image)
    return find_snakes(bw_image, positions)

def find_snakes(bw_image, positions):
    HEIGHT, WIDTH = bw_image.shape[:2]
    is_v2 = cv2.__version__.startswith("2.")

    for position in positions:
        x, y = int(position[0]), int(position[1])
        bw_image[y - HEIGHT//40: y + HEIGHT//40, x-WIDTH//70 : x+WIDTH//70] = 255
    
    bw_image = 255 - bw_image #invert it...
    output = cv2.connectedComponentsWithStats(bw_image)


    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]

    #print(stats)

    return num_labels, labels, stats, centroids

#image = load_image("full_screenshot5.png")
#bw_image = find_snakes_helper(image, 60) #lower threshold for snakes
#save_image(bw_image, "test_snekfilter5.png")