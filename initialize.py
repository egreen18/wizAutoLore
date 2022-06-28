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
    if os_res == 'pc_1920':
        player_boxes = {
            '0': (1523, 990, 1664, 1012),
            '1': (1105, 990, 1252, 1019),
            '2': (690, 991, 835, 1015),
            '3': (272, 992, 419, 1015),

        }
        player_points = {
            '0': (1491, 1016),
            '1': (1072, 1010),
            '2': (663, 1008),
            '3': (244, 1010),

        }
        enemy_boxes = {
            '0': (140, 5, 297, 59),
            '1': (566, 6, 742, 56),
            '2': (994, 10, 1171, 56),
            '3': (1422, 7, 1599, 56),

        }
        enemy_points = {
            '0': (125, 51),
            '1': (550, 49),
            '2': (978, 50),
            '3': (1405, 51),

        }
        coords = {
            'health': (46, 905, 121, 926),
            'mana': (138, 964, 181, 976),
            'commons': (1603, 975),
            'in_match': (570, 450, 1341, 596),
            'team_up': (959, 1011),
            'team_go': (964, 786),
            'pass': (696, 655),
            'teleport': (1731, 984),
            'mark': (1689, 999),
            'player_boxes': player_boxes,
            'player_points': player_points,
            'enemy_boxes': enemy_boxes,
            'enemy_points': enemy_points,
        }
    elif os_res == 'mac_1440':
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
            'health': (405, 348, 530, 370),
            'mana': (566, 347, 670, 368),
            'commons': (1214, 770),
            'in_match': (440, 400, 1030, 530),
            'team_up': (725, 790),
            'team_go': (710, 630),
            'pass': (530, 540),
            'teleport': (1295, 770),
            'mark': (1268, 786),
            'player_boxes': player_boxes,
            'player_points': player_points,
            'enemy_boxes': enemy_boxes,
            'enemy_points': enemy_points,
        }
    return coords


def loadImage(os_res, name, card=0):
    if not card:
        return cv2.imread(os.join('templates', os_res, name))
    elif card:
        return cv2.imread(os.join('templates', os_res, 'cards', name))


def loadTemplates(os_res):
    # This function loads arrow templates into the workspace
    # Loading templates
    cards = {
        'blade':        loadImage(os_res, 'blade_tpl.png', 1),
        'blade_e':      loadImage(os_res, 'blade_e_tpl.png', 1),
        'e_blade':      loadImage(os_res, 'e_blade_tpl.png', 1),
        'hit':          loadImage(os_res, 'hit_tpl.png', 1),
        'hit_e':        loadImage(os_res, 'hit_e_tpl.png', 1),
        'e_hit':        loadImage(os_res, 'e_hit_tpl.png', 1),
        'trap':         loadImage(os_res, 'trap_tpl.png', 1),
        'trap_e':       loadImage(os_res, 'trap_e_tpl.png', 1),
        'e_trap':       loadImage(os_res, 'e_trap_tpl.png', 1),
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
                # Taking the blue space of the image to allow for distinction between enchanted and non-enchanted spells
                templates['cards'][card] = np.array(templates['cards'][card])[:, :, 0]
        else:
            # Taking the grayscale in all other cases
            templates[tpl] = cv2.cvtColor(np.array(templates[tpl]), cv2.COLOR_BGR2GRAY)

    return templates


def initialize():
    os_res = osResGen()
    coords = loadCoords(os_res)
    templates = loadTemplates(os_res)
    return templates, coords
