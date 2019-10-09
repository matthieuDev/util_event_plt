"""
Example of the different ways to use hist2d.
"""
from matplotlib import pyplot as plt
import numpy as np
from random import gauss

import sys
sys.path.append('..')

from util import grab_move , mouse_zoom , hist2d_update

#create the data for the graphs
x = [gauss(0,10000) for _ in range(50000)]
y = [gauss(0,10000) for _ in range(50000)]
data = [x,y]

fig , axes = plt.subplots(2,2)
axes = axes.flatten()

#function used to draw the hist2d
def draw_hist (x , y , ax ,bins ) :
    h = ax.hist2d( x , y , bins  , cmin = 1 )
    return h[3]

#prepare the axis in advance so that we have a tight_layout already created for the buttons
for i in range (4) :
    ax = axes[i]
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title("title")

#optimize axis placement and size 
plt.tight_layout()
#add some space for the button
plt.subplots_adjust(hspace=0.7, wspace=0.7)


for i in range (4) :
    ax = axes[i]
    #for the first axis, add and activate hist2d_update that redraws only the shown part without buttons.
    if ( i == 0 ) :
        hur_true = hist2d_update(
            data = data , 
            draw_hist = draw_hist , 
            ax_button = None , 
            hist_bins = (50,50) , 
            redraw_whole = False ,
            threshold = None , 
            ax = ax , 
            fig = fig 
            ) 
        hur_true.activate_on_ax(ax)
        ax.set_title('hist2d_update_recalculate')
    #for the second axis, add and activate hist2d_update that redraws only the shown part with a button.
    elif ( i == 1 ) :
        #create the the axis for the button
        ax_button_1 = plt.axes([0.9 , 0.52 , 0.09 , 0.05 ])
        
        hur_false = hist2d_update(
            data = data , 
            draw_hist = draw_hist , 
            ax_button = ax_button_1 , 
            hist_bins = (50,50) , 
            redraw_whole = False ,
            threshold = None , 
            ax = ax , 
            fig = fig 
            ) 
        hur_false.activate_on_ax(ax)
        ax.set_title('hist2d_update_recalculate button')
    #for the third axis, add and activate hist2d_update that redraws the whole graph without buttons.
    elif ( i == 2 ) :
        hub_true = hist2d_update(
            data = data , 
            draw_hist = draw_hist , 
            ax_button = None , 
            hist_bins = (50,50) , 
            redraw_whole = True ,
            threshold = (0.8 , 1.2) , 
            ax = ax , 
            fig = fig 
            ) 
        hub_true.activate_on_ax(ax)
        ax.set_title('hist2d_update_redraw_whole')
    #for the fourth axis, add and activate hist2d_update that redraws the whole graph with a button.
    elif ( i == 3 ) :
        #create the the axis for the button
        ax_button_3 = plt.axes([0.9 , 0.02 , 0.09 , 0.05 ])
        hub_false = hist2d_update(
            data = data , 
            draw_hist = draw_hist , 
            ax_button = ax_button_3 , 
            hist_bins = (50,50) , 
            redraw_whole = True ,
            threshold = (0.8 , 1.2) , 
            ax = ax , 
            fig = fig 
            ) 
        hub_false.activate_on_ax(ax)
        ax.set_title('hist2d_update_redraw_whole button')

    # add and activate the event handler to move and zoom on the graph.
    mouse_zoom(ax=ax,fig=fig).activate_on_ax(ax)
    grab_move (ax=ax,fig=fig).activate_on_ax(ax)



plt.show()