from tools import *
from initialize import *
from match import *

time.sleep(2)
auto.click()
runtime = 100000
tpl, coords = initialize()
spell_logic = [
    ('e_hit', 0),
    ('e_blade', 'player'),
    ('blade', 'player'),
    ('e_hit', 0)

]
playMatch(tpl, coords, spell_logic)
