import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from initialize import *

tpl, coords = initialize()
imgplot = plt.imshow(tpl['cards']['hit_e'])
plt.show()