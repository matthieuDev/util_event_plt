# Util Event matplolib

Little script containing event handlers for matplotlib.

## Util.py

File containing the scripts of the event handler :

grab_move :If you click on a graph and move your mouse, the graph move so that the point on which we clicked is always under the cursor. Equivalent to the expanding arrow button on the regular plt window.

fixed_zoom : Set different limit for your graph so that scrolling set those value as the limit of the axis. You can use the function create_gradual_scale to quickly create an example. Has other use than zooming if you set your limit differently.

mouse_zoom : If you scroll up zoom on the position of your mouse, if you scroll down zoom out of the position of your mouse.

get_value : Given one or more continuous function f represented by curves, for the x position of the mouse print x with the value f(x) and draw a point at the value of each curves if it exists.

choose_curve : Given some plots, add button to select the plots you wish to see on the graph.

hist2d_update : When moving or zooming on a hist2d, redraw the hist2d so that bins seen on the screen is constant.

## example

Folder containing example of uses of the different functions of util.py.
