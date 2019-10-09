"""
example of the use of get_value.
"""
import matplotlib.pyplot as plt

import sys
sys.path.append('..')

from util import grab_move , mouse_zoom , choose_curve

#plot simple curve big and small
fig , ax = plt.subplots()

#create different data for the plot of functions
data = [
    [[-10,10],[-10,10]],
    [[(x-1000) / 100 for x in range(2000)] , [((x-1000) / 100)**2 for x in range(2000)]],
    [[-10,10],[10,-10]] ,
    [[x / 100 for x in range(1000)] , [ x**0.5 for x in range(1000)]] ,
    [ [x - 10 for x in range (20)]  , [(x%2 - 0.5)*2 for x in range (20)] ],
]

#plot the curves
curves = [ ax.plot(d[0],d[1])[0] for d in data ]
#get the name of the curves
name_curves = ['linear' , 'square' , 'linear neg' , 'root' , 'high and low']

plt.xlabel('x')
plt.ylabel('y')
plt.title('example')

#add and activate the events
choose_event = choose_curve(
    curves=curves , 
    name_curves = name_curves , 
    recenter = True , 
    ax = ax , 
    fig = fig
)
choose_event.activate()
zoom_event=mouse_zoom(scale = 2 , bound = True  ,ax=ax,fig=fig)
zoom_event.activate()
grab_event = grab_move (ax=ax,fig=fig)
grab_event.activate()


plt.show()