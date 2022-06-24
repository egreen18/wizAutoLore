import pyautogui as auto
import platform
import cv2
import os.path as os
import numpy as np


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
            # At a full deck:
            'start': (440, 400, 510, 500),  # At the deck card
            'int': 70,                      # Horizontal length of a card
            'end': (930, 400, 1000, 500),   # At the last cast
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
            'in_match': (440, 400, 1030, 530),
            'team_up': (725, 790),
            'team_go': (710, 630),
            'pass': (530, 540),
            'card_boxes': card_boxes,
            'card_points': card_points,
            'player_boxes': player_boxes,
            'player_points': player_points,
            'enemy_boxes': enemy_boxes,
            'enemy_points': enemy_points,
        }
        return coords


def loadImage(os_res, name):
    return cv2.imread(os.join('templates', os_res, name))


def loadTemplates(os_res):
    # This function loads arrow templates into the workspace
    # Loading templates
    cards = {
        'blade':        loadImage(os_res, 'blade_tpl.png'),
        'blade_e':      loadImage(os_res, 'blade_e_tpl.png'),
        'e_blade':      loadImage(os_res, 'e_blade_tpl.png'),
        'hit':          loadImage(os_res, 'hit_tpl.png'),
        'hit_e':        loadImage(os_res, 'hit_e_tpl.png'),
        'e_hit':        loadImage(os_res, 'e_hit_tpl.png'),
        'trap':         loadImage(os_res, 'trap_tpl.png'),
        'trap_e':       loadImage(os_res, 'trap_e_tpl.png'),
        'e_trap':       loadImage(os_res, 'e_trap_tpl.png'),
    }
    templates = {
        'cards':        cards,
        'in_match':     loadImage(os_res, 'in_match_tpl.png'),
        'player':       loadImage(os_res, 'player_tpl.png'),
        'loremaster':   loadImage(os_res, 'loremaster_tpl.png'),
        'in_client':    loadImage(os_res, 'in_client_tpl.png'),
        'team_up':      loadImage(os_res, 'team_up_tpl.png'),
    }

    # Converting to grayscale for cv2 processing
    for tpl in templates.keys():
        if tpl == 'cards':
            for card in templates['cards'].keys():
                templates['cards'][card] = cv2.cvtColor(np.array(templates['cards'][card]), cv2.COLOR_BGR2GRAY)
        else:
            templates[tpl] = cv2.cvtColor(np.array(templates[tpl]), cv2.COLOR_BGR2GRAY)

    return templates


def initialize():
    os_res = osResGen()
    coords = loadCoords(os_res)
    templates = loadTemplates(os_res)
    return templates, coords
