import pyautogui as auto
import cv2
import mss
import numpy as np
import time


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


def checkLocation(tpl, loc=0):
    # Checks a location on the screen for a template
    # If no location is given, checks entire screen
    # Provide location (loc) in the upper left lower right coordinate box format
    # Pulling screenshot
    if not loc:
        with mss.mss() as sct:
            pic = sct.grab(sct.monitors[1])
    else:
        with mss.mss() as sct:
            pic = sct.grab(mssMon(loc))

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
