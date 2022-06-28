from initialize import *
from client import *
import pickle
from datetime import datetime


def checkHand(tpl, coords):
    # This function constructs a hand containing the coordinates and identity of all cards pulled
    # Predefining card dictionary
    hand = {}

    # Moving mouse to a location that won't obscure hand
    auto.moveTo(coords['team_up'])
    for card in tpl['cards'].keys():
        point = tplLocate(tpl['cards'][card])
        if point:
            hand[card] = point
    return hand


def waitRound(tpl, coords):
    # Waits until a round has finished animating
    # Returns positive if the round ends because the match is over
    # Returns null if the round ends because a new round has begun
    while not checkLocation(tpl['in_match'], coords['in_match']):
        if checkLocation(tpl['in_client']):
            return 1
    time.sleep(0.5)  # Waiting some time after round begins to let everything initialize in game
    return 0


def passRound(coords):
    button(coords['pass'])


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
    return 0, 0


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


def enchant(hand, spell, tpl, coords):
    # Enchants a spell when requested by the spell logic
    # Checks to see if spell enchantment is in hand
    base = spell[spell.index('_')+1:]
    if base+'_e' in hand:
        # Enchanting spell
        button(hand[base+'_e'][0])
        button(hand[base][0])

        # Updating hand
        hand = checkHand(tpl, coords)

        # Successful indicator
        status = 1

    # If enchantment is not available, notify castSpell to cast unenchanted spell instead
    else:
        status = 0
    return hand, status


def castSpell(tpl, spell, target, coords):
    # Casts a spell (string) from the hand (list) at the target (screen coordinates)
    # Starts by constructing hand
    hand = checkHand(tpl, coords)

    # Checks for the need to enchant a spell
    # Is the request enchanted? Is the enchant in the hand? Is the base spell in the hand?
    if 'e_' in spell and spell not in hand and spell[spell.index('_')+1:] in hand:
        hand, status = enchant(hand, spell, tpl, coords)
        if not status:
            # Casting unenchanted spell instead if enchant is unavailable
            spell = spell[spell.index('_')+1:]

    # Selecting spell
    if spell in hand.keys():
        button(hand[spell][0])
    # Or passing if the spell is not in hand for some reason
    else:
        passRound(coords)

    # Select a target for the spell if it requires one
    if target:
        button(target)

    return


def playMatch(tpl, coords, spell_logic):
    # Waiting for round to begin
    waitRound(tpl, coords)

    # Identifying unit positions
    player, position = identifyPlayer(tpl, coords)
    boss = identifyBoss(tpl, coords)
    target = {
        'player': player,
        'boss': boss,
        0: 0,
    }

    for spell in spell_logic:
        castSpell(tpl, spell[0], target[spell[1]], coords)
        if waitRound(tpl, coords):
            leaveMatch(position)
            return

    leaveMatch(position)
    return


def startMatch(tpl, coords):
    # Attempts to start match, returns 0 if failed
    dist = 0.5
    while not checkLocation(tpl['team_up']):
        jigglePlayer(dist)
        # Increasing the intensity of the player jiggle to try and catch the team up button on screen
        dist += 0.02
        time.sleep(dist)

        # If this fails, teleport to the mark in front of the sigil
        if dist >= 0.6:
            teleport(tpl, coords)
            return 0

    # Starting team up queue
    button(coords['team_up'])
    button(coords['team_go'])
    now = time.time()
    with auto.hold('w'):
        while not checkLocation(tpl['in_match'], coords['in_match']):
            # If a few minutes have elapsed, restart the process of starting the match
            # This could be because something went wrong or because no one joined the team up queue
            if time.time() > now+150:
                return 0
    return 1


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


def autoLore(runtime, spell_logic):
    # Automatically runs loremaster battles for a given runtime in seconds
    # Takes spell logic as a list of lists containing spells casted and their targets in desired order

    # Initialization
    now = time.time()
    tpl, coords = initialize()

    while time.time() < now + runtime:
        # Waiting to make sure that client is open
        while not checkLocation(tpl['in_client']):
            pass
        checkHealth(tpl, coords)
        if not checkMana(coords, 160):
            getMana(tpl, coords)
        # Tries to start match, if failed, returns 0 and triggers a restart of the function
        if not startMatch(tpl, coords):
            autoLore(runtime, spell_logic)
        playMatch(tpl, coords, spell_logic)
        with open('runCount.pkl', 'rb') as file:
            count = pickle.load(file)
        count += 1
        current = datetime.now()
        current_time = current.strftime("%H:%M:%S")
        print("{} runs completed at {}".format(str(count), str(current_time)))
        with open('runCount.pkl', 'wb') as file:
            pickle.dump(count, file)

