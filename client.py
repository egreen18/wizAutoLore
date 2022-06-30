from tools import *


def getMana(tpl, coords):
    # Teleporting to commons to get mana orbs
    button(coords['commons'])
    time.sleep(2)
    button(coords['commons'])

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
    while not checkMana(coords, 220):
        with auto.hold('d'):
            with auto.hold('w'):
                time.sleep(5)

    # Returning to loremaster
    teleport(tpl, coords)
    return


def checkMana(coords, threshold):
    # Checks the status of the mana globe
    with mss.mss() as sct:
        pic = sct.grab(mssMon(coords['mana']))
    blue = np.array(pic)[:, :, 0]
    if np.average(blue) < threshold:
        return 0

    return 1


def checkHealth(coords):
    # Checking health
    with mss.mss() as sct:
        pic = sct.grab(mssMon(coords['health']))
    red = np.array(pic)[:, :, 2]

    now = time.time()
    while np.average(red) < 200:
        time.sleep(5)
        with mss.mss() as sct:
            pic = sct.grab(mssMon(coords['health']))
        red = np.array(pic)[:, :, 2]
        # Returning to commons if health is not regenerating; could be stuck in boss room
        if time.time() > now+120:
            button(coords['commons'])

    return


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

    # Waiting for mark timer to run out
    while time.time() < now+30:
        pass

    # Resetting mark
    button(coords['mark'])
    return
