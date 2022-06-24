from tools import *
from initialize import *


def cardCount(tpl, coords):
    # Counts the number of cards in the hand by analyzing the position of the top deck card
    start = coords['card_boxes']['start']
    step = coords['card_boxes']['int']
    for slot in range(8):
        # Defining coordinates of the slot
        box = (start[0]+step*slot/2, start[1], start[2]+step*slot/2, start[3])

        # Screenshotting
        with mss.mss() as sct:
            pic = sct.grab(mssMon(box))

        # Converting to grayscale for cv2 processing
        pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

        # Checking for the deck card
        if tplComp(pic, tpl['in_match']):
            # Returning the number of cards in the deck
            return 7-slot


def checkHand(tpl, coords):
    # This function identifies the order of the hand of cards pulled from the deck and returns it as a list of strings
    # Predefining card array
    hand = []
    count = cardCount(tpl, coords)
    print("{} cards".format(count))
    start = coords['card_boxes']['start']
    step = coords['card_boxes']['int']
    for slot in range(count):
        box = (start[0]+(step+1)*slot, start[1], start[2]+(step+1)*slot, start[3])
        with mss.mss() as sct:
            # Grabbing a picture of the location of the card in the hand
            pic = sct.grab(mssMon(box))

        # Converting to grayscale for cv2 processing
        pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

        # Identifying the card
        for card in tpl['cards'].keys():
            if tplComp(pic, tpl['cards'][card]):
                hand.append(card)
                break
    print(hand)
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
    # Returns positive if the round ends because the match is over
    # Returns null if the round ends because a new round has begun
    while not checkLocation(tpl['in_match'], coords['in_match']):
        if checkLocation(tpl['in_client']):
            return 1
    time.sleep(0.5)  # Waiting some time after round begins to let everything initialize in game
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
            hand = checkHand(tpl, coords)
        else:
            break

    # Same for blade
    while 'blade_e' in hand:
        if 'blade' in hand:
            # Enchanting blade
            button(selectCard(hand, coords, 'blade_e'))
            button(selectCard(hand, coords, 'blade'))
            # Update hand
            hand = checkHand(tpl, coords)
        else:
            break

    # Same for hit
    while 'hit_e' in hand:
        if 'hit' in hand:
            # Enchanting hit
            button(selectCard(hand, coords, 'hit_e'))
            button(selectCard(hand, coords, 'hit'))
            # Update hand
            hand = checkHand(tpl, coords)
        else:
            break
    return hand


def castSpell(hand, spell, tpl, coords, target):
    # Casts a spell (string) from the hand (list) at the target (screen coordinates)
    # Starts by cleaning hand
    hand = cleanHand(hand, tpl, coords)
    print("Casting {}".format(spell))
    button(selectCard(hand, coords, spell))
    # Hit-all spells are target-less
    if target:
        button(target)
    # Update hand
    hand = checkHand(tpl, coords)
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
    hand = castSpell(hand, 'e_blade', tpl, coords, player)
    # Wait for round
    if waitRound(tpl, coords):
        leaveMatch(position)
        return

    # Cast enchanted hit
    hand = castSpell(hand, 'e_hit', tpl, coords, 0)
    # Wait for round
    if waitRound(tpl, coords):
        leaveMatch(position)
        return

    # Cast blade
    hand = castSpell(hand, 'blade', tpl, coords, player)
    # Wait for round
    if waitRound(tpl, coords):
        leaveMatch(position)
        return

    # Cast enchanted hit
    hand = castSpell(hand, 'e_hit', tpl, coords, 0)
    # Wait for round
    if waitRound(tpl, coords):
        leaveMatch(position)
        return

    leaveMatch(position)
    return


def startMatch(tpl, coords):
    dist = 0.5
    while not checkLocation(tpl['team_up']):
        jigglePlayer(dist)
        dist += 0.02  # Increasing the intensity of the player jiggle to try and catch the team up button on screen
        time.sleep(dist)

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
    tpl, coords = initialize()

    while time.time() < now+runtime:
        # Waiting to make sure that client is open
        while not checkLocation(tpl['in_client']):
            pass
        startMatch(tpl, coords)
        playMatch(tpl, coords)
