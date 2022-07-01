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
mana = 0
run_max = 125
autoLore(runtime, run_max, spell_logic, mana)
