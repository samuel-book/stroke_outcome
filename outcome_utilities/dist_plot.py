"""
Functions for plotting mRS distributions as horizontal bars. 
"""
import numpy as np
import matplotlib.pyplot as plt 

def draw_horizontal_bar(dist, label='', colour_list=[], hatch_list=[], 
                        ecolour_list=[], linewidth=None, ax=None):
    """
    Draw a stacked horizontal bar chart of the values in 'dist'.
    
    dist  - list or np.array. The probability distribution 
            (non-cumulative).
    label - string. The name printed next to these stacked bars.
    """
    if ax==None:
        ax = plt.subplot()
        
    # Define any missing inputs: 
    if len(colour_list)<1:
        # Get current matplotlib style sheet colours:
        colour_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
        while len(colour_list)<len(dist):
            # Shouldn't need this, but in case dist is really long:
            colour_list += colour_list
        # Remove extra colours:
        colour_list = colour_list[:len(dist)-1]
        # Add grey for mRS=6 bin:
        colour_list.append('DarkSlateGray')
    if len(hatch_list)<1:
        hatch_list   = [None for d in dist]
    if len(ecolour_list)<1:
        ecolour_list = ['k' for d in dist]
        
        
    # The first bar will start at this point on the x-axis:
    left = 0
    for i in range(len(dist)):
        # Draw a bar starting from 'left', the end of the previous bar,
        # with a width equal to the probability of this mRS:
        ax.barh(label, width=dist[i], left=left, height=0.5, 
                 label=f'{i%7}', edgecolor=ecolour_list[i], color=colour_list[i],
                 hatch=hatch_list[i], linewidth=linewidth)
        # Update 'left' with the width of the current bar so that the 
        # next bar drawn will start in the correct place.    
        left += dist[i]
        

def draw_connections(dist_t0, dist_tne, top_tne=0.25, bottom_t0=0.75, ax=None):
    """
    Draw lines connecting the mRS bins in the top and bottom rows.
    
    dist_t0, dist_tne - lists or arrays. Probability distributions.
    top_tne, bottom_t0 - floats. y-coordinates just inside the bars. 
    """
    if ax==None:
        ax = plt.subplot()
        
    left_t0   = 0.0
    left_tne  = 0.0
    for i, d_t0 in enumerate(dist_t0):
        left_t0  += dist_t0[i]
        left_tne += dist_tne[i]
        ax.plot([left_t0,left_tne],[bottom_t0,top_tne],color='k')