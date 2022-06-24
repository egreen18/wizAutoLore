from tools import *
from initialize import *


def checkHand(tpl, coords):
    # This function constructs a hand containing the coordinates and identity of all cards pulled
    # Predefining card dictionary
    hand = {}
    with mss.mss() as sct:
        pic = sct.grab(mssMon(coords['in_match']))
    
    pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

    # Identifying the card
    for card in tpl['cards'].keys():
        points = tplLocate(pic, tpl['cards'][card])
        if points:
            hand[card] = points+np.array(coords['in_match'][:2])
    print(hand)
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
    while 'trap_e' in hand.keys():
        # And a trap can be enchanted
        if 'trap' in hand.keys():
            # Enchanting trap
            button(hand['trap_e'][0])
            button(hand['trap'][0])
            # Update hand
            hand = checkHand(tpl, coords)
        else:
            break

    # Same for blade
    while 'blade_e' in hand.keys():
        if 'blade' in hand.keys():
            # Enchanting blade
            button(hand['blade_e'][0])
            button(hand['blade'][0])
            # Update hand
            hand = checkHand(tpl, coords)
        else:
            break

    # Same for hit
    while 'hit_e' in hand.keys():
        if 'hit' in hand.keys():
            # Enchanting hit
            button(hand['hit_e'][0])
            button(hand['hit'][0])
            # Update hand
            hand = checkHand(tpl, coords)
        else:
            break
    return hand


def castSpell(tpl, spell, target, coords):
    # Casts a spell (string) from the hand (list) at the target (screen coordinates)
    # Starts by checking and cleaning hand
    hand = checkHand(tpl, coords)
    hand = cleanHand(hand, tpl, coords)

    # Selecting spell
    print("Casting {}".format(spell))
    button(hand[spell])

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
    }

    for spell in spell_logic:
        castSpell(tpl, spell[0], target[spell[1]], coords)
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
        while not checkLocation(tpl['in_match'], coords['in_match']):
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
        spell_logic = [
            ('e_blade', 'player'),
            ('e_hit', 0),
            ('blade', 'player'),
            ('e_hit', 0)
        ]
        playMatch(tpl, coords, spell_logic)
