import platform
import pyautogui as auto
import cv2
import mss
import os.path as os
import numpy as np
import time
import pickle


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
            '3': (180, 800),

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
            'health': (39, 718, 85, 734),
            'mana': (104, 758, 135, 768),
            'commons': (1214, 770),
            'in_match': (440, 400, 1030, 530),
            'team_up': (725, 790),
            'team_go': (710, 630),
            'pass': (530, 540),
            'teleport': (1295, 770),
            'mark': (1268, 786),
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
    cards = {
        'blade':        cv2.imread(os.join('templates', os_res, 'blade_tpl.png')),
        'blade_e':      cv2.imread(os.join('templates', os_res, 'blade_e_tpl.png')),
        'hit':          cv2.imread(os.join('templates', os_res, 'hit_tpl.png')),
        'hit_e':        cv2.imread(os.join('templates', os_res, 'hit_e_tpl.png')),
        'trap':         cv2.imread(os.join('templates', os_res, 'trap_tpl.png')),
        'trap_e':       cv2.imread(os.join('templates', os_res, 'trap_e_tpl.png')),
    }
    templates = {
        'cards':        cards,
        'in_match':     cv2.imread(os.join('templates', os_res, 'in_match_tpl.png')),
        'player':       cv2.imread(os.join('templates', os_res, 'player_tpl.png')),
        'loremaster':   cv2.imread(os.join('templates', os_res, 'loremaster_tpl.png')),
        'in_client':    cv2.imread(os.join('templates', os_res, 'in_client_tpl.png')),
        'team_up':      cv2.imread(os.join('templates', os_res, 'team_up_tpl.png')),
    }

    # Converting to grayscale for cv2 processing
    # Converting to grayscale for cv2 processing
    for tpl in templates.keys():
        if tpl == 'cards':
            for card in templates['cards'].keys():
                templates['cards'][card] = cv2.cvtColor(np.array(templates['cards'][card]), cv2.COLOR_BGR2GRAY)
        else:
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
        for card in tpl['cards'].keys():
            if tplComp(pic, tpl['cards'][card]):
                hand.append(card)
                break

    return hand


def selectCard(hand, coords, card):
    # Returns the coordinates of a card in the hand
    # If there are repeated cards, returns the first of the series
    minC = coords['card_points']['0'][0]
    step = coords['card_points']['1'][0] - minC
    if card in hand:
        index = hand.index(card)
    else:
        return 0
    handMax = 7
    coords = (minC + index*step + (handMax - len(hand))*70/2, 455)
    return coords


def waitRound(tpl, coords):
    # Waits until a round has finished animating
    # Returns positive if the round ends because the match is over
    # Returns null if the round ends because a new round has begun
    while not checkLocation(tpl['in_match'], coords['in_match']):
        if checkLocation(tpl['in_client']):
            return 1
    time.sleep(0.5) # Waiting some time after round begins to let everything initialize in game
    return 0


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
                return coords['player_points'][position], position
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


def getMana(tpl, coords):
    # Teleporting to commons to get mana orbs
    button(coords['commons'])

    # Waiting for client to load after teleporting
    while checkLocation(tpl['in_client']):
        pass
    while not checkLocation(tpl['in_client']):
        pass

    # Running around commons
    while not checkMana(coords):
        with auto.hold('a'):
            with auto.hold('w'):
                time.sleep(5)

    # Returning to loremaster
    teleport(tpl, coords)
    return


def checkMana(coords):
    with mss.mss() as sct:
        pic = sct.grab(mssMon(coords['mana']))
    blue = np.array(pic)[:, :, 0]

    if np.average(blue) < 210:
        return 0

    return 1


def checkHealth(coords):
    with mss.mss() as sct:
        pic = sct.grab(mssMon(coords['health']))
    red = np.array(pic)[:, :, 2]

    while np.average(red) < 200:
        time.sleep(5)
        with mss.mss() as sct:
            pic = sct.grab(mssMon(coords['health']))
        red = np.array(pic)[:, :, 2]

    return


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


def passRound(coords):
    button(coords['pass'])


def castSpell(hand, spell, coords, tpl, target):
    # Casts a spell (string) from the hand (list) at the target (screen coordinates)
    # Starts by cleaning hand
    hand = cleanHand(hand, tpl, coords)

    # Making sure that card is in hand and passing else
    if not selectCard(hand, coords, spell):
        passRound(coords)
        return hand

    # Selecting spell
    button(selectCard(hand, coords, spell))

    # Selecting target if applicable
    if target:
        button(target)
    # Update hand
    hand.remove(spell)
    return hand


def playMatch(tpl, coords):
    # Waiting for round to begin
    waitRound(tpl, coords)

    # Identifying unit positions
    player, position = identifyPlayer(tpl, coords)
    boss = identifyBoss(tpl, coords)

    # Analyzing hand
    hand = checkHand(tpl, coords)

    # Cast enchanted blade
    hand = castSpell(hand, 'e_blade', coords, tpl, player)
    # Wait for round
    if waitRound(tpl, coords):
        leaveMatch(position)
        return

    # Cast enchanted hit
    hand = castSpell(hand, 'e_hit', coords, tpl, 0)
    # Wait for round
    if waitRound(tpl, coords):
        leaveMatch(position)
        return

    # Cast blade
    hand = castSpell(hand, 'blade', coords, tpl, player)
    # Wait for round
    if waitRound(tpl, coords):
        leaveMatch(position)
        return

    # Cast enchanted hit
    hand = castSpell(hand, 'e_hit', coords, tpl, 0)
    # Wait for round
    if waitRound(tpl, coords):
        leaveMatch(position)
        return

    # Will pass until game is overs
    while not checkLocation(tpl['in_client']):
        waitRound(tpl, coords)
        passRound(coords)
        pass

    leaveMatch(position)
    return


def teleport(tpl, coords):
    button(coords['teleport'])
    # Waiting for client to load after teleporting
    while checkLocation(tpl['in_client']):
        pass
    while not checkLocation(tpl['in_client']):
        pass
    time.sleep(2)
    # Resetting mark
    button(coords['mark'])
    return


def startMatch(tpl, coords):
    dist = 0.5
    while not checkLocation(tpl['team_up']):
        jigglePlayer(dist)
        dist += 0.02  # Increasing the intensity of the player jiggle to try and catch the team up button on screen
        time.sleep(dist)
        if dist > 0.6:
            # If something is stopping the player from being in the right location, use the set marker to return
            teleport(tpl, coords)
            dist = 0.5

    # Starting team up queue
    button(coords['team_up'])
    button(coords['team_go'])
    with auto.hold('w'):
        while not checkLocation(tpl['in_match'],coords['in_match']):
            pass
    return


def leaveMatch(position):
    if position == '0':
        with auto.hold('d'):
            time.sleep(0.5)
        with auto.hold('s'):
            time.sleep(2.5)
    elif position == '1':
        with auto.hold('d'):
            time.sleep(0.2)
        with auto.hold('s'):
            time.sleep(2.5)
    elif position == '2':
        with auto.hold('a'):
            time.sleep(0.2)
        with auto.hold('s'):
            time.sleep(2.5)
    elif position == '3':
        with auto.hold('a'):
            time.sleep(0.5)
        with auto.hold('s'):
            time.sleep(2.5)


def autoLore(runtime):
    # Automatically runs loremaster battles for a given runtime in seconds

    # Initialization
    now = time.time()
    os_res = osResGen()
    tpl = loadTemplates(os_res)
    coords = loadCoords(os_res)

    while time.time() < now+runtime:
        # Waiting to make sure that client is open
        while not checkLocation(tpl['in_client']):
            pass
        checkHealth(coords)
        if not checkMana(coords):
            getMana(tpl, coords)
        startMatch(tpl, coords)
        playMatch(tpl, coords)
        with open('runCount.pkl', 'rb') as file:
            count = pickle.load(file)
        count += 1
        print("{} runs completed".format(str(count)))
        with open('runCount.pkl', 'wb') as file:
            pickle.dump(count, file)

