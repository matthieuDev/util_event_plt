"""
Example using both zoom : fixed_zoom and mouse_zoom.
"""

from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np
from random import gauss

import sys
sys.path.append('..')

from util import fixed_zoom , mouse_zoom , grab_move , create_gradual_scale

fig , axes = plt.subplots(1,2)

### fixed_zoom ###
#draw a scatter plot
axes = axes.flatten()
ax = axes[0]
data = np.random.standard_cauchy((2,10000))*100
x,y= data[0] , data[1]

ax.scatter(x , y)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('example fixed_zoom')

zoom_scale = create_gradual_scale( 
   x = x ,
   y = y ,
   fixed_point = ( np.median(x) , np.median(y) ) ,
   factor = 2 , 
   nb_element = 15
)

#add and activate fixed_zoom and grab_move
fixed_zoom = fixed_zoom( 
   zoom_scale , ax , fig
   ).activate_on_ax(ax)
fixed_grab = grab_move (ax=ax,fig=fig).activate_on_ax(ax)

### mouse_zoom ###
#draw a scatter plot
ax = axes[1]
x = [gauss(0,10000) for _ in range(5000)]
y = [gauss(0,10000) for _ in range(5000)]

ax.scatter(x , y)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('example mouse_zoom')

#add and activate mouse_zoom and grab_move
mouse_zoom = mouse_zoom(ax=ax,fig=fig).activate_on_ax(ax)
mouse_grab = grab_move (MouseButton.RIGHT ,ax=ax,fig=fig).activate_on_ax(ax)


plt.show()