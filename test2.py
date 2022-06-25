from tools import *
time.sleep(2)
auto.click()
os_res = osResGen()
tpl = loadTemplates(os_res)
coords = loadCoords(os_res)
checkMana(coords)
