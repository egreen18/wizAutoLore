from match import *

time.sleep(1)
auto.click()
runtime = 100000
spell_logic = [
    ('e_hit', 0),
    ('e_blade', 'player'),
    ('blade', 'player'),
    ('e_hit', 0)

]
autoLore(runtime, spell_logic)
