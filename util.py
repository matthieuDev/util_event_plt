"""
List of matplotlib's event handler functions.
"""

from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.widgets import CheckButtons , Button

def expand_figure ( side , added_inch , ax =  None , fig = None ) :
    """
    expand the figure without expanding the axis.

    arguments :
    side : either 'LEFT' , 'RIGHT' , 'BOTTOM' or 'TOP'. Used to choose which side to expand.
    added_inch : number of inches added to the fig
    ax : the ax that should stay the same.
    fig : the figure to expand
    """

    # if fig or ax is unkown, get it
    ax = plt.gca() if ax is None else ax
    fig = plt.gcf() if fig is None else fig

    assert side in ['LEFT' , 'RIGHT' , 'BOTTOM' , 'TOP']

    is_vertical = side in ['BOTTOM' , 'TOP']
    is_vertical_int = int( is_vertical)
    is_min = side in ['LEFT' , 'BOTTOM']

    # get size of the figure and position of the axis.
    size_fig = fig.get_size_inches()
    ax_pos = ax.get_position()

    #get the position of the parts to change as a value between [0,1] that represents its relative position on the figure
    old_pos = [ax_pos.y0,ax_pos.y1] if is_vertical else [ax_pos.x0 , ax_pos.x1]
    #transform the position from relative of the figure to inches length
    old_coord  = [ p * size_fig[is_vertical_int] for p in old_pos ]
    
    #update the knew size of the figure after having added the inches.
    size_fig[is_vertical_int] = \
        size_fig[ is_vertical_int ] + added_inch   
    fig.set_size_inches( size_fig[0] , size_fig[1])

    #get the new position the axis should have
    new_pos = [ (c + 
        (added_inch if is_min else 0 ) ) 
        /  size_fig[is_vertical_int ] 
        for c in old_coord]

    #change the axis postition so that it keeps the same size as before the figure expansion.
    if is_vertical :
        plt.subplots_adjust(
            bottom =  new_pos[0] ,
            top  =  new_pos[1]
            )      
    else :
        plt.subplots_adjust(
            left=  new_pos[0] ,
            right =  new_pos[1]
            )


class event_handler :
    """
    Parent of the class used for the event handling. 
    """
    def __init__ (self ,  ax =  None , fig = None ) :
        """
        set the axis and figure. Find it if not given
        """
        self.ax = plt.gca() if ax is None else ax
        self.fig = plt.gcf() if fig is None else fig

    def activate(self) :
        """
        ativate all the functions needed for the event handling that are stocked in self.event_action.
        self.event_action should be a list of tuple :
            ( the event to which to react , 
            the function that manage the event. It should only take one argument of type event)
        """
        return [
            self.fig.canvas.mpl_connect( event , action )
            for event , action in self.event_action
        ]

    def activate_on_ax (self , ax) :
        """
        to use when there is multiple axis, so that the function only influence the axis that is currently used.
        """
        for event , action in self.event_action :
            self.fig.canvas.mpl_connect(
                 event , self.action_on_factory(action , ax) 
                 )

    def action_on_factory (self , action , ax) :
        """
        create the function if currently interact with axis == ax then do action. Used for activate_on_ax.
        """
        def action_on (event) :
            if event.inaxes == ax :
                action(event)
        return action_on
    


class grab_move (event_handler)  :
    """
    move the limit of an axis when the graph is grabbed around. Equivalent of the expanding arrow icon in the regular matplotlib window.
    """
    
    def __init__ ( self , button = MouseButton.RIGHT , ax = None , fig = None) :
        """
        button : the button to press to allow the graph to move with the mouse. 
        """
        super().__init__(ax,fig)
        self.button = button

        self.is_grabing = False

        self.event_action = [('button_press_event',self.grab),
                             ('button_release_event',self.release),
                             ('motion_notify_event',self.move)]

    

    def grab (self , event):
        #What to do when a mouse's button is pressed.
        if self.button == event.button :
            self.is_grabing = True
            self.pos = ( event.xdata, event.ydata )

    def release (self , event):
        #What to do when a mouse's button is released.
        if self.button == event.button :
            self.is_grabing = False

    def move (self , event):
        #what to do when the mouse is moving

        #if the graph is grabbed and we are on the graph, move the limit as much as the mouse was moved.
        if self.is_grabing :
            curr_pos = ( event.xdata, event.ydata )
            if all(curr_pos) :
                diff = [ self.pos [i] - curr_pos[i] for i in range(2) ]
                xlim , ylim = self.ax.get_xlim() , self.ax.get_ylim()

                self.ax.set_xlim (xlim[0] + diff[0] , xlim[1] + diff[0] )
                self.ax.set_ylim (ylim[0] + diff[1] , ylim[1] + diff[1] )
                
                plt.draw()

def create_gradual_scale ( x ,y , fixed_point , 
    factor = 2 , nb_element = 15) :
    """
    consider x and y as data for a graph, create a list of limit where for each step, the distance between each limit and the fixed_point
    is divided by factor; and where the first step is the regular limit given if you just plot the data.
    Used for easy values for fixed_zoom.

    x ,y : data along the x and y axis.
    fixed_point :central point that is considered to be zoomed on.
    factor : by what to divide between each step
    nb_element : how many step to create.

    return the steps with format : [x0,y0,x1,y1]
    """

    xmax , ymax = max (x) , max(y)
    xmin , ymin = min (x) , min(y)
    lengthx , lengthy = xmax - xmin , ymax - ymin

    return [( fixed_point[0] +  ( xmin - fixed_point[0] - lengthx *0.05 ) // (factor**i) ,
            fixed_point[1] + ( ymin - fixed_point[1] - lengthy * 0.05 ) // (factor**i) , 
            fixed_point[0] + ( xmax - fixed_point[0] + lengthx *0.05 ) // (factor**i) ,
            fixed_point[1] + ( ymax - fixed_point[1] + lengthy * 0.05 ) // (factor**i)) 
            for i in range(nb_element)]


class fixed_zoom (event_handler) :
    """
    zoom along the limit given by scales when scrolling.
    """
    
    def __init__(self , scales , ax = None , fig = None) :
        """
        scales : the values with which to delimite the axis. format : list where each element is (x0,y0,x1,y1).
        """
        super().__init__(ax,fig)

        self.scales = scales
        self.len = len(scales)
        self.i = 0

        self.event_action = [('scroll_event',self.zoom)]
    
    def zoom (self , event):
        #get the new position of the limits on the list.
        if event.button == 'up':
            self.i+=1
            
        elif event.button == 'down' :
            self.i-=1

        else :
            return
            
        
        self.i = max(0,min(self.len-1 , self.i))
        s = self.scales[self.i]

        #update the limits and redraw
        self.ax.set_xlim (s[0] , s[2] )
        self.ax.set_ylim (s[1] , s[3] )       
        
        plt.draw()


class mouse_zoom (event_handler) :
    """
    zoom on the mouse when scrolling. scroll down to zoom out and scroll up to zoom in.
    """

    def __init__ (self , scale = 2 , bound = True  , ax = None , fig = None) :
        """
        scale : how much to zoom for each scroll move.
        bound : if True does not zoom further that when the plot was created, and do not zoom too much away from the graph.
        """
        super().__init__(ax,fig)

        self.scale = scale
        self.bound = bound
        if bound :
            #limits of the graph at the beggining
            self.bound_limit = (ax.get_xlim() , ax.get_ylim())
            #size of the graph at the beggining
            self.bound_size = (
                self.bound_limit[0][1] - self.bound_limit[0][0] , 
                self.bound_limit[1][1] - self.bound_limit[1][0]
            )

        self.event_action = [('scroll_event',self.zoom)]


    def zoom (self,event) :
        # zoom on scroll

        #calculate the factor used to orientate in which direction to zoom.
        if event.button == 'up':
            factor =  1 / self.scale
            
        elif event.button == 'down' :
            factor = -self.scale

        else :
            return

        #calculate the new limites of the graph
        x , y = event.xdata , event.ydata
        
        xlim , ylim = self.ax.get_xlim() , self.ax.get_ylim() 

        new_x = (
            ( x - xlim[0] ) * factor + xlim[0],
            ( x - xlim[1] ) * factor + xlim[1]
        )
        new_y = (
            ( y - ylim[0] ) * factor + ylim[0],
            ( y - ylim[1] ) * factor + ylim[1]
        )

        

        if self.bound :
            #resize if the user zoom out too much

            #current size of the graph
            xsize , ysize = new_x[1] - new_x[0] , new_y[1] - new_y[0]
            #ratio between original and current size of the graph
            factorx , factory =  self.bound_size[0] / xsize ,  self.bound_size[1] / ysize

            #if a current size of the graph is bigger than the original one along one axis, we zoom in to have the same size between the 2..
            if factorx < 1 :
                new_x = ( x + ( new_x[0] - x  ) * factorx , 
                          x + ( new_x[1] -  x   ) * factorx )

            if factory < 1 :
                new_y = ( y + ( new_y[0] - y  ) * factory , 
                          y + ( new_y[1] -  y   ) * factory )

            
            #recenter if the user zoom outside the figure
            left_bound = max ( 0 , self.bound_limit[0][0] - new_x[0]  )
            new_x = ( new_x[0] + left_bound , new_x[1] + left_bound )
            right_bound = max ( 0 ,  new_x[1] - self.bound_limit[0][1] )
            new_x = ( new_x[0] - right_bound , new_x[1] - right_bound )

            bottom_bound = max ( 0 , self.bound_limit[1][0] - new_y[0]  )
            new_y = ( new_y[0] + bottom_bound , new_y[1] + bottom_bound )
            upper_bound = max ( 0 ,  new_y[1] - self.bound_limit[1][1] )
            new_y = ( new_y[0] - upper_bound , new_y[1] - upper_bound )

        #update the limits and redraw
        self.ax.set_xlim (new_x[0] , new_x[1] )
        self.ax.set_ylim (new_y[0] , new_y[1] )
        
        plt.draw()


class get_value (event_handler) :
    """
    given one or more line curve from data, given an x-value from the position of the mouse : 
    print the y-value and draw a point on the curves if it exists, i.e. for x = mouse x draw point (x,f(x)).
    Used only on line curve with data that can be considered as continuous function.
    """
    def __init__ ( self , data , name_curves = None , colors = "#0000ff", ax = None , fig = None) :
        """
        data : data of the curves must be a list of couple of data (x,y) where the lengths of x and y are equals.
        name_curves : name given for the curve, must be the same length as data.
        colors : color of the text. default is blue
        """
        super().__init__(ax,fig)

        self.data = data
        self.colors = colors
        #if there is no namae for the curves, name the curve 1, curve 2 ...
        self.name_curves = ['curve %d'%(i+1) for i in range(len(data))] \
            if name_curves is None else name_curves

        #points currently drawn
        self.points = None
        
        #expand the figure to have some space to put the printed values
        expand_figure ('LEFT' , 2 , ax , self.fig)

        ax_text = plt.axes([0.01, 0.05, 0.15, 0 ])
        ax_text.axis('off')
        self.text = ax_text.text(0.05, 0.8, '', fontsize=10)

        self.event_action = [('motion_notify_event',self.get_value)]


    def get_value ( self , event ) :
        #get the current value.

        mousex = event.xdata
        #if we have drawn points, delete them
        if not self.points is None :
            self.points.remove()

        #get the y for each curve
        coords = [ self.get_y(d , mousex) for d in self.data]
        #transform the value in string and print it.
        text = 'x\n' + str(mousex) + '\n' + \
            '\n'.join(
                [ name +'\n' + ('None' if c is None else str(c[1]) ) 
                for name , c in zip(self.name_curves , coords)
            ])
        self.text.set_text( text )
        #draw the points if possible
        coords = [c for c in coords if not c is None]
        self.points = self.ax.scatter(
                [x[0] for x in coords] ,
                [x[1] for x in coords] ,
                c = self.colors
                ) if coords else None

        #redraw graph
        plt.draw()


    def get_y ( self , data , mousex ) : 
        """
        given the the data of a curve as (x,y) where x and y are list of float of the same size representing a function f; and given an x value mousex,
        return y such that f(x) = y if it exists otherwise return None.
        """
        datax , datay = data
        if mousex is None or mousex < datax[0] or mousex > datax[-1] :
            return None
        for i , d in enumerate(datax[1:]) :
            if d == mousex :
                return (mousex,datay[i])
            elif mousex <= d :
                lx , rx = datax[i:i+2] 
                ly , ry = datay[i:i+2] 
                return ( mousex , ly + ( mousex - lx ) / ( rx - lx ) * (ry - ly) )


class choose_curve (event_handler) :
    """
    creates button to decide which curves will be visible
    """
    def __init__ ( self , curves , name_curves = None , recenter = True , ax = None , fig = None) :
        """
        curves: list of plot.
        name_curves : name_curves[i] is the name of the curve curves[i]. Must the same length as curves.
        recenter : recenter the graph each time we add or remove a plot.
        """
        super().__init__(ax,fig)

        self.curves = curves
        self.name_curves = ['curve %d'%(i+1) for i in range(len(data))] \
            if name_curves is None else name_curves
        self.recenter = recenter


    def add_button ( self , ax ) :
        #extend window to have some place to write the coordinate
        expand_figure ('LEFT' , 2 , ax , self.fig)

        ax_but = plt.axes([0.01, 0.05, 0.4, 0.8 ])
        #do not show the graph of the button axis
        ax_but.axis('off')

        #add buttons
        self.check = CheckButtons(ax_but, self.name_curves ,  [True for _ in self.curves] )
        #link the event handler function to the button
        self.check.on_clicked(self.on_click)
     
    #not usual activate because of the button so overwrite activate and activate_on_ax
    def activate ( self ) :
        self.add_button(self.ax)
        

    def activate_on_ax (self , ax) : 
        self.add_button(ax)

    def on_click(self,label):
        #get the current curve
        curve = self.curves[self.name_curves.index(label)]
        #set it invisivle if it is visible and vice versa
        curve.set_visible(not curve.get_visible())
        if self.recenter :
            # recompute the ax.dataLim
            self.ax.relim(visible_only=True)
            # update ax using the new dataLim
            self.ax.autoscale()
        #redraw graph
        plt.draw()


class hist2d_update (event_handler) :
    """
    Class that allows to recalculate an hist2d when looking at a different part of the graph while keeping the number of bin on that part constant.
    Different ways were used, the graph is updated either every time there is a change or when pressing a button; 
    and at each update we either redraw only the showed part or the whole dataset when zooming.

    When redrawing all the dataset, moving the graph with a little zoom is fast but the more you zoom in, the slower it becomes.
    When redrawing only the shown part :
        without a button, the speed is average and constant.
        with a button change are the fastest but when moving or zooming out there will be part not drawn. 
    """
    def __init__ (self , data , draw_hist , ax_button = None , hist_bins = (10,10) , redraw_whole = False, threshold = (0.8 , 1.2) , ax = None , fig = None) :
        """
        data : the dataset used to draw the hist2d
        draw_hist : a function that takes as argument (x , y , ax , bins) where x and y are the data of each axis, ax is the axis on which to draw,
            and bins are the bin specification for hist2d; and it must return a drawn histogram.
        ax_button : If None the update is done at every change, otherwise ax_button is the ax on which to draw the button.
        hist_bins : the bin specification for hist2d that should be visible.
        redraw_whole : True when we redraw the whole graph when zooming otherwise update at each movement (only the showed part).
        threshold : couple of float only used when redraw_whole == True, 
            redraw only if the current length of the graph is:
              - lower than the lower threshold * the length of the graph the last time the curve was drawn
              - bigger than the upper threshold * the length of the graph the last time the curve was drawn
            Used to prevent little move from causing a whole redraw.
        """
        super().__init__(ax,fig)

        self.data = list(zip(data[0] , data[1] ))
        self.draw_hist = draw_hist
        self.ax_button = ax_button
        self.hist_bins = hist_bins

        self.hist2d = self.draw_hist ( 
                [ x[0] for x in self.data ] , 
                [ x[1] for x in self.data ] ,
                self.ax ,
                self.hist_bins 
                )
        #create the colorbar for the legend
        self.colorbar =  plt.colorbar(self.hist2d, ax=self.ax)
        self.limit = (ax.get_xlim() , ax.get_ylim())
        #set the function to use
        self.update = self.update_zoom if redraw_whole else self.update_always

        #if we use zoom, save the size of the graph to detect zooms
        if redraw_whole :
            self.threshold = threshold
            self.begin_length = self.length = \
                (self.limit[0][1] - self.limit[0][0] , self.limit[1][1] - self.limit[1][0])

        #if we do not use button add the function to the event to activate
        if not ax_button :
            self.event_action = [('draw_event',self.update)]

        
 
    def update_always (self,event) :
        """
        Function used when we update at every change.
        """
        curr_limit = (self.ax.get_xlim() , self.ax.get_ylim() )
        
        #if we are moving or we using a button update the graph
        if curr_limit != self.limit or self.ax_button:
            self.limit = curr_limit 
            #get the data that should be shown on the screen
            curr_data = [
                x for x in self.data
                if x[0] >=self.limit[0][0] and x[0] <= self.limit[0][1]
                and x[1] >=self.limit[1][0] and x[1] <= self.limit[1][1]
            ]
                
            #redraw the hist2d and colorbar
            self.colorbar.remove()
            self.hist2d.remove()
            
            self.hist2d = self.draw_hist ( 
                [ x[0] for x in curr_data ] , 
                [ x[1] for x in curr_data ] ,
                self.ax ,
                self.hist_bins
                )
            self.colorbar =  plt.colorbar(self.hist2d, ax=self.ax) 

            self.fig.canvas.draw()


    def update_zoom (self,event) :
        """
        Function used when we update only while zooming.
        """
        def ratio_tuple( x , y) :
            return  [  x[i] / y[i]  for i in range(2) ]

        #use threshold to see if we zoomed enough to update also zoom if we used a button
        curr_limit = (self.ax.get_xlim() , self.ax.get_ylim() )
        curr_length =  (curr_limit[0][1] - curr_limit[0][0] , curr_limit[1][1] - curr_limit[1][0])
        ratio_new_length = ratio_tuple(curr_length , self.length)
        
        if any ([ r <= self.threshold[0] or r >= self.threshold[1] for r in ratio_new_length]) or self.ax_button :
            self.length = curr_length
            
            #calculate the bin needed for the whole dataset so that on the shown part we have the good number of bins.
            ratio_bins = ratio_tuple( self.length , self.begin_length)
                
            #redraw the hist2d and colorbar
            self.colorbar.remove()
            self.hist2d.remove()
            
            self.hist2d = self.draw_hist ( 
                [ x[0] for x in self.data ] , 
                [ x[1] for x in self.data ] ,
                self.ax ,
                ratio_tuple( self.hist_bins , ratio_bins )
                )
            self.colorbar =  plt.colorbar(self.hist2d, ax=self.ax)
            
            #set the good limit after redrawing 
            self.ax.set_xlim (curr_limit[0][0] , curr_limit[0][1] )
            self.ax.set_ylim (curr_limit[1][0] , curr_limit[1][1] )

            self.fig.canvas.draw()


    def add_button ( self  ) :
        self.but = Button(self.ax_button, 'redraw', color='red', hovercolor='green')
        self.but.on_clicked(self.update)

    #not usual activate because of the possible button so overwrite activate and activate_on_ax
    def activate (self) :
        if self.ax_button :
            self.add_button()
        else :
            super().activate()
    
    #event redraw only when the current graph changed so activate_on_ax does not really makes sense. Still use it to keep the structure.
    def activate_on_ax (self,ax) :
        self.activate()