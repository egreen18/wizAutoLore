from tools import *
from initialize import *
time.sleep(1)
tpl, coord = initialize()
points = tplLocate(tpl['cards']['hit'])
print(points)
for point in points:
    button(point)
