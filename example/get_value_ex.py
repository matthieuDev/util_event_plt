"""
example of the use of get_value.
"""
import sys
sys.path.append('..')

from util import get_value , grab_move , mouse_zoom
from random import gauss

import matplotlib.pyplot as plt

fig , ax = plt.subplots()

#create different data for the plot of functions
data = [
    [[-10,10],[-10,10]],
    [[(x-1000) / 100 for x in range(2000)] , [((x-1000) / 100)**2 for x in range(2000)]],
    [[-10,10],[10,-10]] ,
    [[x / 100 for x in range(1000)] , [ x**0.5 for x in range(1000)]] ,
    [ [x - 10 for x in range (20)]  , [(x%2 - 0.5)*2 for x in range (20)] ],
]
#get their names
name_curves = ['linear' , 'square' , 'linear neg' , 'root' , 'high and low']
#plot the functions
for d in data :
    plt.plot(d[0],d[1])
plt.xlabel('x')
plt.ylabel('y')
plt.title('example')


#extend window to have some place to write the coordinate
plt.legend(name_curves , bbox_to_anchor=(1.04,1))
fig.tight_layout ()

#add and activate the events
zoom_event=mouse_zoom(scale = 2 , bound = True  ,ax=ax,fig=fig)
zoom_event.activate()
grab_event = grab_move (ax=ax,fig=fig)
grab_event.activate()
value_event = get_value(data=data , 
    name_curves = name_curves , 
    colors = "#0000ff",
    ax=ax,
    fig=fig)
value_event.activate()


plt.show()