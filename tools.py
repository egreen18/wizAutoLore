import platform
import pyautogui as auto
import cv2
import mss
import os.path as os
import numpy as np
import time

def mssMon(shape):
    # Takes a resolution in the form of a 1,4 list and prepares it for input into mss screenshot function
    mon = {"top": shape[1], "left": shape[0], "width": shape[2]-shape[0], "height": shape[3]-shape[1]}
    return mon


def osResGen():
    res_val = auto.size()
    if platform.system() == 'Darwin':
        os_val = 'mac'
    elif platform.system() == 'Windows':
        os_val = 'pc'
    else:
        os_val = ''
    os_res = '_'.join([os_val, str(res_val[0])])
    return os_res


def loadCoords(os_res):
    coords = {}
    if os_res == 'pc_1680':
        coords = {
        }
    elif os_res == 'mac_1440':
        card_boxes = {
            '0': (510, 400, 580, 500),
            '1': (580, 400, 650, 500),
            '2': (650, 400, 720, 500),
            '3': (720, 400, 790, 500),
            '4': (790, 400, 860, 500),
            '5': (860, 400, 930, 500),
            '6': (930, 400, 1000, 500),
        }
        card_points = {
            '0': (540, 455),
            '1': (610, 455),
            '2': (680, 455),
            '3': (750, 455),
            '4': (820, 455),
            '5': (890, 455),
            '6': (960, 455),
        }
        player_boxes = {
            '0': (1110, 750, 1250, 820),
            '1': (820, 750, 940, 820),
            '2': (500, 750, 630, 820),
            '3': (190, 750, 320, 820),

        }
        player_points = {
            '0': (1110, 800),
            '1': (800, 800),
            '2': (500, 800),
            '3': (180, 500),

        }
        enemy_boxes = {
            '0': (110, 70, 240, 125),
            '1': (425, 70, 555, 125),
            '2': (750, 70, 870, 125),
            '3': (1065, 70, 1200, 125),

        }
        enemy_points = {
            '0': (95, 95),
            '1': (415, 95),
            '2': (730, 95),
            '3': (1050, 95),

        }
        coords = {
            'round': (440, 400, 510, 500),
            'card_boxes': card_boxes,
            'card_points': card_points,
            'player_boxes': player_boxes,
            'player_points': player_points,
            'enemy_boxes': enemy_boxes,
            'enemy_points': enemy_points,
        }
        return coords


def loadTemplates(os_res):
    # This function loads arrow templates into the workspace
    # Loading templates
    templates = {
        'blade':    cv2.imread(os.join('templates', os_res, 'blade_tpl.png')),
        'blade_e':  cv2.imread(os.join('templates', os_res, 'blade_e_tpl.png')),
        'hit':      cv2.imread(os.join('templates', os_res, 'hit_tpl.png')),
        'hit_e':    cv2.imread(os.join('templates', os_res, 'hit_e_tpl.png')),
        'trap':     cv2.imread(os.join('templates', os_res, 'trap_tpl.png')),
        'trap_e':   cv2.imread(os.join('templates', os_res, 'trap_e_tpl.png')),
        'round':    cv2.imread(os.join('templates', os_res, 'round_tpl.png')),
        'player':    cv2.imread(os.join('templates', os_res, 'player_tpl.png')),
        'loremaster': cv2.imread(os.join('templates', os_res, 'loremaster_tpl.png')),
    }

    # Converting to grayscale for cv2 processing
    for tpl in templates.keys():
        templates[tpl] = cv2.cvtColor(np.array(templates[tpl]), cv2.COLOR_BGR2GRAY)

    return templates


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


def checkLocation(loc, tpl):
    # Checks a location on the screen for a template
    # Provide location (loc) in the upper left lower right coordinate box format
    # Pulling screenshot
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


def jiggle():
    # Jiggles mouse to reactivate some buttons
    pos = auto.position()

    auto.moveTo((pos[0] + 2, pos[1] + 2))
    time.sleep(0.02)
    auto.moveTo((pos[0], pos[1]))


def button(coords):
    auto.moveTo(coords)
    time.sleep(0.1)
    jiggle()
    auto.click()
    time.sleep(0.1)


def checkHand(tpl, coords):
    # This function identifies the order of the hand of cards pulled from the deck and returns it as a list of strings
    # Predefining card array
    hand = []
    for slot in coords['card_boxes'].keys():
        with mss.mss() as sct:
            # Grabbing a picture of the location of the card in the hand
            pic = sct.grab(mssMon(coords['card_boxes'][slot]))

        # Converting to grayscale for cv2 processing
        pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

        # Identifying the card
        for card in tpl.keys():
            if tplComp(pic, tpl[card]):
                hand.append(card)
                break

    return hand


def selectCard(hand, coords, card):
    # Returns the coordinates of a card in the hand
    # If there are repeated cards, returns the first of the series
    minC = coords['card_points']['0'][0]
    step = coords['card_points']['1'][0] - minC
    index = hand.index(card)
    handMax = 7
    coords = (minC + index*step + (handMax - len(hand))*70/2, 455)
    return coords


def waitRound(tpl, coords):
    # Waits until a round has finished animating
    print('Waiting for round to begin...')
    while not checkLocation(coords['round'], tpl['round']):
        pass
    time.sleep(0.5) # Waiting some time after round begins to let everything initialize in game


def identifyPlayer(tpl, coords):
    # Identifies the players position based off of their name
    # If another wizard shares their name, this could misidentify the player
    for position in coords['player_boxes'].keys():
        with mss.mss() as sct:
            # Grabbing a picture of the name of the wizard in each position
            pic = sct.grab(coords['player_boxes'][position])

            # Converting to grayscale for cv2 processing
            pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

            # Checking to see if player is in that position
            if tplComp(pic, tpl['player']):
                return coords['player_points'][position]
    return 0


def identifyBoss(tpl, coords):
    # Identifies the players position based off of their name
    # If another wizard shares their name, this could misidentify the player
    for position in coords['enemy_boxes'].keys():
        with mss.mss() as sct:
            # Grabbing a picture of the name of the wizard in each position
            pic = sct.grab(coords['enemy_boxes'][position])

            # Converting to grayscale for cv2 processing
            pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

            # Checking to see if player is in that position
            if tplComp(pic, tpl['loremaster']):
                return coords['enemy_points'][position]
    return 0


def cleanHand(hand, tpl, coords):
    # Cleans hand by applying all enchantments
    # If a trap enchantment is present
    while 'trap_e' in hand:
        # And a trap can be enchanted
        if 'trap' in hand:
            # Enchanting trap
            button(selectCard(hand, coords, 'trap_e'))
            button(selectCard(hand, coords, 'trap'))
            # Update hand
            hand[hand.index('trap')] = 'e_trap'
            hand.remove('trap_e')
        else:
            break

    # Same for blade
    while 'blade_e' in hand:
        if 'blade' in hand:
            # Enchanting blade
            button(selectCard(hand, coords, 'blade_e'))
            button(selectCard(hand, coords, 'blade'))
            # Update hand
            hand[hand.index('blade')] = 'e_blade'
            hand.remove('blade_e')
        else:
            break

    # Same for hit
    while 'hit_e' in hand:
        if 'hit' in hand:
            # Enchanting hit
            button(selectCard(hand, coords, 'hit_e'))
            button(selectCard(hand, coords, 'hit'))
            # Update hand
            hand[hand.index('hit')] = 'e_hit'
            hand.remove('hit_e')
        else:
            break
    return hand


def castSpell(hand, spell, coords, target):
    # Casts a spell (string) from the hand (list) at the target (screen coordinates)
    print("Casting {}".format(spell))
    button(selectCard(hand, coords, spell))
    # Hit-all spells are target-less
    if target:
        button(target)
    # Update hand
    hand.remove(spell)
    return


def playMatch(tpl, coords):
    # Waiting for round to begin
    waitRound(tpl, coords)

    # Identifying unit positions
    player = identifyPlayer(tpl, coords)
    boss = identifyBoss(tpl, coords)

    # Analyzing hand
    hand = checkHand(tpl, coords)

    # Cleaning hand
    hand = cleanHand(hand, tpl, coords)

    # Cast enchanted blade
    castSpell(hand, 'e_blade', coords, player)
    # Wait for round
    waitRound(tpl, coords)

    # Cast enchanted hit
    castSpell(hand, 'hit', coords, 0)
    waitRound(tpl, coords)

    # Wait for end of battle

    return
