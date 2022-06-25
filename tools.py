import pyautogui as auto
import cv2
import mss
import numpy as np
import time
from imutils.object_detection import non_max_suppression


def mssMon(shape):
    # Takes a resolution in the form of a 1,4 list and prepares it for input into mss screenshot function
    mon = {"top": shape[1], "left": shape[0], "width": shape[2]-shape[0], "height": shape[3]-shape[1]}
    return mon


def tplComp(image, tpl):
    # This function compares template and image to identify text or arrows
    # Perform match operations.
    res = cv2.matchTemplate(image, tpl, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = 0.8

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    # If matched area coordinates exist, arrow is identified. Return positive
    if len(loc[0]) > 0:
        return 1
    else:
        return 0


def tplLocate(tpl, image=0):
    # This function returns the center coordinates of the location of a template identified in an image
    # Coordinates are with respect to the image, not necessarily the entire screen
    # Takes images in BGRx or BGR format
    # Can return a list of coordinates if a template appears multiple times

    # By default, takes a screenshot of the entire screen if no image is provided
    if not image:
        with mss.mss() as sct:
            image = sct.grab(sct.monitors[1])

    # Pulling the blue space of the images to allow for distinction between enchanted and non-enchanted cards
    image = np.array(image)[:, :, 0]

    # Matching template to image
    result = cv2.matchTemplate(image, tpl, cv2.TM_CCOEFF_NORMED)

    # Defining threshold
    threshold = 0.8

    # Locating template
    (yCoords, xCoords) = np.where(result >= threshold)

    # Finding bounding boxes
    rects = []
    (tH, tW) = tpl.shape
    for (x, y) in zip(xCoords, yCoords):
        # update our list of rectangles
        rects.append((x, y, x + tW, y + tH))

    # Apply non-maxima suppression to the rectangles
    pick = non_max_suppression(np.array(rects))

    # Getting resolution information
    comp_res = auto.size()
    image_res = image.shape

    # Adjusting for resolution differences between screenshot and mouse coordinate plane
    points = []
    for box in pick:
        points.append(((box[0]+tW/2)*comp_res[0]/image_res[1], (box[1]+tH/2)*comp_res[1]/image_res[0]))

    return points


def checkLocation(tpl, loc=0):
    # Checks a location on the screen for a template
    # If no location is given, checks entire screen
    # Provide location (loc) in the upper left lower right coordinate box format

    # Pulling screenshot
    if loc:
        with mss.mss() as sct:
            pic = sct.grab(mssMon(loc))
    else:
        with mss.mss() as sct:
            pic = sct.grab(sct.monitors[1])

    # Converting to grayscale for cv2 processing
    pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

    # Checking arrows against templates
    if tplComp(pic, tpl):
        identified = 1
    else:
        identified = 0

    return identified


def jiggleMouse():
    # Jiggles mouse to reactivate some buttons
    pos = auto.position()

    auto.moveTo((pos[0] + 2, pos[1] + 2))
    time.sleep(0.02)
    auto.moveTo((pos[0], pos[1]))


def jigglePlayer(dist):
    # Jiggles player position to reactivate some buttons
    # Range indicates how long the buttons will be held down
    with auto.hold('s'):
        time.sleep(1.5*dist)
    with auto.hold('w'):
        time.sleep(dist)


def button(coords):
    auto.moveTo(coords)
    time.sleep(0.1)
    jiggleMouse()
    auto.click()
    time.sleep(0.1)
