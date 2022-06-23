import tools
import pyautogui as auto

auto.click()
os_res = tools.osResGen()
templates = tools.loadTemplates(os_res)
coords = tools.loadCoords(os_res)
tools.playMatch(templates, coords)