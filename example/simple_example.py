"""
Example of a graph using mouse_zoom and grab_event.
"""
from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton

import numpy as np
from random import gauss

import sys
sys.path.append('..')

from util import grab_move , mouse_zoom

fig , ax = plt.subplots()

#draw a scatter plot
x = [gauss(0,10000) for _ in range(5000)]
y = [gauss(0,10000) for _ in range(5000)]

ax.scatter(x , y)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('simple example')

#add and activate the events
zoom_event = mouse_zoom(scale = 2 , bound = True  ,ax=ax,fig=fig)
zoom_event.activate()
grab_event = grab_move (button = MouseButton.RIGHT,ax=ax,fig=fig)
grab_event.activate()

plt.show()