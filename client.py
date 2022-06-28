from tools import *
import pytesseract
import re


def getHealth(tpl, coords):
    # Idles to collect health until above 95%, re-checking status in 15 second intervals
    status, original = checkHealth(coords, 0.95)

    # Status is negative if health is below threshold
    while not status:
        time.sleep(15)
        status, actual = checkHealth(coords, 0.95)

        # If health is not regenerating, this means that the player may be stuck in the boss room
        # Teleporting to commons to alleviate this issue, startMatch will realize this and return to mark later
        if not actual > original:
            commons(coords)

    return


def getMana(tpl, coords):
    # Teleporting to commons to get mana orbs
    commons(coords)

    # Waiting for client to load after teleporting
    now = time.time()

    # Waiting for loading screen to start
    while checkLocation(tpl['in_client']):
        # Breaking out of this restriction, sometimes teleports don't trigger a loading screen or they fail
        if time.time() > now + 8:
            break
        pass

    # Waiting for loading screen to end
    while not checkLocation(tpl['in_client']):
        pass
    time.sleep(2)

    # Running around commons
    # Continues until mana is above 95% full
    # Attempts to collect mana in 15 second intervals
    while not checkMana(coords, 0.95):
        with auto.hold('d'):
            with auto.hold('w'):
                time.sleep(15)
                # Re-centering in the commons occasionally or avoiding a failed teleport to the commons
                commons(coords)

    # Returning to loremaster
    teleport(tpl, coords)
    return


def getStat(stat, coords):
    # Returns mana or health
    # Returns a list containing integer values of the stat [actual, total]
    # Opens the character menu for a period of time
    # Used for checking health and mana status since it provides low interference images of text containing info
    auto.press('c')
    time.sleep(3)

    # Grabbing the stat status and closing the character menu
    with mss.mss() as sct:
        pic = sct.grab(mssMon(coords[stat]))
    auto.press('c')

    # Processing the image of the mana status into string variable
    text = pytesseract.image_to_string(np.array(pic))

    # Checking to make sure mana was successfully interpreted
    if not text:
        # Return negative if failed
        return 0

    # Removing all non-numbers interpreted by tesseract from the string
    text = re.sub("[^0-9 /]", "", text)

    # Finishing mana status analysis
    print(text)
    text = text.split('/')
    statVal = []
    for num in text:
        statVal.append(int(num))

    return statVal


def checkMana(coords, threshold):
    # Checks mana and returns 0 if below threshold, 1 if above
    # Threshold is a value between 0 and 1
    mana = getStat('mana', coords)

    # If getStat failed, try again
    if not mana:
        checkMana(coords, threshold)

    # Checking if mana is above or below threshold
    print(mana)
    if mana[0]/mana[1] < threshold:
        return 0
    else:
        return 1


def checkHealth(coords, threshold):
    # Checks health and returns two variables:
    # A binary indicator, positive if health is above threshold and negative otherwise
    # The current value of the health for the purpose of making sure that health is actually regenerating
    # Checking health
    health = getStat('health', coords)

    # If getStat failed, try again
    if not health:
        checkHealth(coords, threshold)

    # Checking if health is above or below threshold
    print(health)
    if health[0] / health[1] < threshold:
        return 0, health[0]
    else:
        return 1, health[0]


def teleport(tpl, coords):
    button(coords['teleport'])
    # Waiting for client to load after teleporting
    now = time.time()

    # Waiting for loading screen to start
    while checkLocation(tpl['in_client']):
        # Breaking out of this restriction, sometimes teleports don't trigger a loading screen
        if time.time() > now+8:
            break
        pass

    # Waiting for loading screen to end
    while not checkLocation(tpl['in_client']):
        pass
    time.sleep(2)
    # Resetting mark
    button(coords['mark'])
    return


def commons(coords):
    # Teleports to commons
    # Tries twice because problems have been observed in game with teleport not happening after a single press
    button(coords['commons'])
    time.sleep(1)
    button(coords['commons'])
    return
