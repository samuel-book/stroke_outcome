"""
Functions for plotting mRS distributions as horizontal bars. 
"""
import numpy as np
import matplotlib.pyplot as plt 

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def draw_horizontal_bar(dist, 
                        #label='', 
                        y=0, colour_list=[], hatch_list=[], 
                        ecolour_list=[], linewidth=None, bar_height=0.5,
                        ax=None):
    """
    Draw a stacked horizontal bar chart of the values in 'dist'.
    
    dist  - list or np.array. The probability distribution 
            (non-cumulative).
    label - string. The name printed next to these stacked bars.
    """
    # Define any missing inputs: 
    if ax==None:
        ax = plt.subplot()
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
        # Don't add bar to legend if it has fancy hatch formatting:
        # legend_label = f'{i%7}' if hatch_list[i]==None else None 
        legend_label = None if hatch_list[i]!=None and '\\' in hatch_list[i] else f'{i%7}' 
        
        # Draw a bar starting from 'left', the end of the previous bar,
        # with a width equal to the probability of this mRS:
        ax.barh(y, 
                 width=dist[i], 
                 left=left, 
                 height=bar_height, 
                 label=legend_label, 
                 edgecolor=ecolour_list[i], 
                 color=colour_list[i],
                 hatch=hatch_list[i], 
                 linewidth=linewidth,
                 # tick_label=label
                )
        # Update 'left' with the width of the current bar so that the 
        # next bar drawn will start in the correct place.    
        left += dist[i]
        

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def draw_connections(dist_top, dist_bottom, 
                     top_of_bottom_bar=0.25, bottom_of_top_bar=0.75,
                     colour='k', linewidth=1.0, ax=None):
    """
    Draw lines connecting the mRS bins in the top and bottom rows.
    
    dist_t0, dist_tne - lists or arrays. Probability distributions.
    top_tne, bottom_t0 - floats. y-coordinates just inside the bars. 
    """
    
    # Define any missing inputs: 
    if ax==None:
        ax = plt.subplot()
        
    left_of_top_bar = 0.0
    left_of_bottom_bar = 0.0
    for i, d_t0 in enumerate(dist_top):
        left_of_top_bar += dist_top[i]
        left_of_bottom_bar += dist_bottom[i]
        ax.plot([left_of_top_bar,left_of_bottom_bar],
                 [bottom_of_top_bar,top_of_bottom_bar],
                 color=colour, linewidth=linewidth)
        

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def draw_horizontal_bar_excess(bins, bins_deaths,  
        draw_bottom=1, draw_top=1,
        #label_bottom='Discrete', label_top='Mixed',
        y_bottom=0, y_top=1, bar_height=0.5, draw_legend=1,
        ax=None, hatch=None):
    """
    Fancier formatting to show excess deaths. 
    
    Top is discrete, bottom is mixed.
    """

    # Define any missing inputs: 
    if ax==None:
        ax = plt.subplot()
        
    # Find the proportion of excess deaths for each mRS bin. 
    # The mRS<=6 bin will have opposite sign to the others because the 
    # other deaths are added to that bin.
    dist_excess_only = bins - bins_deaths

    # Find the probability distribution excluding all excess deaths 
    # _including_ in the mRS<=6 bin, i.e. this distribution will not 
    # sum to 1.
    dist_without_excess = np.concatenate((bins_deaths[:-1], [bins[-1]]))

    # Set up plotting style:
    colour_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_list.append('DarkSlateGray')

    hatch_without_excess = [hatch for d in dist_without_excess]
    hatch_excess_only    = ['////' for d in dist_excess_only]

    # Define distributions, hatches and colours for the first row...
    dist_top = np.stack((dist_without_excess, 
                           dist_excess_only), axis=1).ravel()
    hatch_top = np.stack((hatch_without_excess, 
                            hatch_excess_only), axis=1).ravel()
    colour_top = np.stack((colour_list, colour_list), axis=1).ravel()

    # ... and the second:
    dist_bottom = np.concatenate((dist_without_excess, dist_excess_only))
    hatch_bottom = np.concatenate((hatch_without_excess, 
                                     hatch_excess_only))
    colour_bottom = np.concatenate((colour_list, colour_list))
    

    # Make the plot as usual:
    if draw_bottom==1:
        # Draw t=0 distribution
        draw_horizontal_bar(dist_bottom[:-1], #label_bottom, 
                            y_bottom,
                            colour_bottom, hatch_bottom,
                            bar_height=bar_height, ax=ax
                            )
        if draw_legend==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])  
            # Legend below axis.
        
    if draw_top==1:
        # Draw no effect distribution
        draw_horizontal_bar(dist_top[:-1], #label_top,
                            y_top,
                            colour_top, hatch_top,
                            bar_height=bar_height, ax=ax)
        if draw_bottom==0 and draw_legend==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])
    if draw_bottom==1 and draw_top==1:        
        # Draw connecting lines
        draw_connections(bins, bins_deaths,
                         top_of_bottom_bar=y_bottom+0.5*bar_height, 
                         bottom_of_top_bar=y_top-0.5*bar_height,
                         ax=ax)
    
    if draw_legend==2:
        # dummy1 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=hatch_without_excess[0])#, visible=False)
        dummy2 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=hatch_excess_only[0])#, visible=False)
        ax.legend([
            # dummy1, 
                   dummy2], 
                  [
                      # 'mRS distribution', 
                   'Proportion removed by excess deaths'],
                 bbox_to_anchor=[1.1,0.5,0.2,0.2])
    

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------    
def draw_horizontal_bar_weighted(dist_not_weighted, weight=0.0, 
        draw_bottom=1, draw_top=1, 
        # label_bottom='Discrete', label_top='Mixed',
        y_bottom=1, y_top=0, bar_height=0.5, draw_legend=1,
        ax=None, dist2=[], hatch=None):
    """
    Fancier formatting to show effect of weighting.
    
    Top is discrete, bottom is mixed.
    """

    # Define any missing inputs: 
    if ax==None:
        ax = plt.subplot()
        
    if len(dist2)>0:
        dist_weighted = dist_not_weighted
        dist_removed = dist2
    else:
        # Find the proportion of each mRS bin that will be removed by the
        # weighting, i.e. this distribution will not sum to 1.
        dist_weighted = dist_not_weighted * np.abs(weight)
        dist_removed = dist_not_weighted - dist_weighted
    
    if weight>1.0:
        dist_weighted_smaller = dist_not_weighted * np.abs(1.0-weight)
        dist_removed_smaller = dist_not_weighted - dist_weighted_smaller

    # Set up plotting style:
    colour_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_list.append('DarkSlateGray')

    colour_weighted = colour_list
    colour_removed  = ['w' for colour in colour_list]

    hatch_weighted = [hatch for d in dist_weighted]
    hatch_removed  = ['//////' for d in dist_removed]

    ecolour_list_weighted = ['k' for d in dist_weighted]
    ecolour_list_removed  = [colour for colour in colour_list]

    # Define distributions, hatches and colours for the first row...
    dist_top = np.stack((dist_weighted,  dist_removed), axis=1).ravel()
    hatch_top = np.stack((hatch_weighted, hatch_removed), axis=1).ravel()
    colour_top = np.stack((colour_weighted, colour_removed), axis=1).ravel()
    ecolour_top = np.stack((ecolour_list_weighted,
                            ecolour_list_removed), axis=1).ravel()

    # ... and the second:
    dist_bottom = np.concatenate((dist_weighted, dist_removed))
    hatch_bottom = np.concatenate((hatch_weighted, hatch_removed))
    colour_bottom = np.concatenate((colour_weighted, colour_removed))
    ecolour_bottom = np.concatenate((ecolour_list_weighted, 
                                       ecolour_list_removed))

    if weight>1.0:
        hatch_unwanted = ['++++' for d in dist_removed]
        ecolour_list_unwanted = ['DarkSlateGrey' for d in dist_removed]
        # Define distribution for the first row...
        dist_top = np.stack((dist_weighted_smaller,  dist_removed_smaller), axis=1).ravel()
        hatch_bottom = np.stack((hatch_weighted, hatch_removed), axis=1).ravel()
        colour_bottom = np.stack((colour_weighted, colour_removed), axis=1).ravel()
        ecolour_bottom = np.stack((ecolour_list_weighted, 
                                  ecolour_list_removed), axis=1).ravel()
        # hatch_top = np.stack((hatch_unwanted, hatch_removed), axis=1).ravel()
        # colour_top = np.stack((colour_weighted, colour_removed), axis=1).ravel()
        # ecolour_top = np.stack((ecolour_list_unwanted, 
        #                         ecolour_list_removed), axis=1).ravel()
        # Define distributions, hatches and colours for the bottom row...
        dist_bottom = np.stack((dist_not_weighted,dist_weighted_smaller), axis=1).ravel()
        hatch_bottom = np.stack((hatch_weighted, hatch_removed), axis=1).ravel()
        colour_bottom = np.stack((colour_weighted, colour_removed), axis=1).ravel()
        ecolour_bottom = np.stack((ecolour_list_weighted, 
                                  ecolour_list_removed), axis=1).ravel()


    # Make the plot as usual:
    if draw_bottom==1:
        # Draw t=0 distribution
        draw_horizontal_bar(dist_bottom, 
                            #label_bottom, 
                            y_bottom,
                            colour_bottom, 
                            hatch_bottom, ecolour_bottom,
                            bar_height=bar_height, ax=ax)
        if draw_legend==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])   # Legend below axis.
    if draw_top==1:
        # Draw no effect distribution
        draw_horizontal_bar(dist_top, #label_top, 
                            y_top,
                            colour_top, 
                            hatch_top, ecolour_top,
                            bar_height=bar_height, ax=ax)
        if draw_bottom==0 and draw_legend==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])
        
    # Second plot just to get the outlines looking right
    draw_horizontal_bar(dist_not_weighted, #label_top, 
                        y_top,
                        ['None' for d in dist_not_weighted], linewidth=1,
                        bar_height=bar_height, ax=ax)
    draw_horizontal_bar(dist_weighted, #label_bottom, 
                        y_bottom,
                        ['None' for d in dist_weighted], linewidth=1,
                        bar_height=bar_height, ax=ax)

    if draw_bottom==1 and draw_top==1:     
        # Draw connecting lines
        draw_connections(dist_not_weighted, dist_weighted,
                         top_of_bottom_bar=y_bottom+0.5*bar_height, 
                         bottom_of_top_bar=y_top-0.5*bar_height,
                         ax=ax)

    if draw_legend==2:
        # dummy1 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=hatch_weighted[0])#, visible=False)
        dummy2 = plt.bar(np.NaN, 0.0, color='k', edgecolor='w', hatch=hatch_removed[0])#, visible=False)
        ax.legend([
                    # dummy1, 
                    dummy2], 
                  [
                   # 'mRS distribution', 
                   'Proportion removed by weighting'],
                 bbox_to_anchor=[1.1,0.5,0.2,0.2])

        

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------    
def draw_horizontal_bar_combo(dist_1, dist_2, 
        draw_bottom=1, draw_top=1, 
        # label_bottom='Discrete', label_top='Mixed',
        y_bottom=1, y_top=0, bar_height=0.5, draw_legend=1,
        ax=None, dist2=[], hatches=[None,'//////']):
    """
    Fancier formatting to show effect of weighting.
    
    Top is discrete, bottom is mixed.
    """

    # Define any missing inputs: 
    if ax==None:
        ax = plt.subplot()
    
    
    # Set up plotting style:
    colour_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_list.append('DarkSlateGray')

    colour_1 = colour_list
    colour_2  = ['w' for colour in colour_list]

    hatch_1 = [hatches[0] for d in dist_1]
    hatch_2 = [hatches[1] for d in dist_2]

    ecolour_1 = ['k' for d in dist_1]
    ecolour_2 = [colour for colour in colour_list]

    # Define distributions, hatches and colours for the first row...
    dist_top = np.stack((dist_1,  dist_2), axis=1).ravel()
    hatch_top = np.stack((hatch_1, hatch_2), axis=1).ravel()
    colour_top = np.stack((colour_1, colour_2), axis=1).ravel()
    ecolour_top = np.stack((ecolour_1, ecolour_2), axis=1).ravel()

    # ... and the second:
    dist_bottom = np.concatenate((dist_1, dist_2))
    hatch_bottom = np.concatenate((hatch_1, hatch_2))
    colour_bottom = np.concatenate((colour_1, colour_2))
    ecolour_bottom = np.concatenate((ecolour_1, ecolour_2))

    # Make the plot as usual:
    if draw_bottom==1:
        # Draw t=0 distribution
        draw_horizontal_bar(dist_bottom, 
                            #label_bottom, 
                            y_bottom,
                            colour_bottom, 
                            hatch_bottom, ecolour_bottom,
                            bar_height=bar_height, ax=ax)
        if draw_legend==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])   # Legend below axis.
    if draw_top==1:
        # Draw no effect distribution
        draw_horizontal_bar(dist_top, #label_top, 
                            y_top,
                            colour_top, 
                            hatch_top, ecolour_top,
                            bar_height=bar_height, ax=ax)
        if draw_bottom==0 and draw_legend==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])
        
    # Second plot just to get the outlines looking right
    draw_horizontal_bar(dist_1+dist_2, #label_top, 
                        y_top,
                        ['None' for d in dist_1+dist_2], linewidth=1,
                        bar_height=bar_height, ax=ax)
    # draw_horizontal_bar(dist_weighted, #label_bottom, 
    #                     y_bottom,
    #                     ['None' for d in dist_weighted], linewidth=1,
    #                     bar_height=bar_height, ax=ax)

    if draw_bottom==1 and draw_top==1:     
        # Draw connecting lines
        draw_connections(dist_1+dist_2, dist_1,
                         top_of_bottom_bar=y_bottom+0.5*bar_height, 
                         bottom_of_top_bar=y_top-0.5*bar_height,
                         ax=ax)

        
def draw_horizontal_bar_combo_sum(dist_1, dist_2, 
        draw_bottom=1, draw_top=1, 
        # label_bottom='Discrete', label_top='Mixed',
        y_bottom=1, y_top=0, bar_height=0.5, draw_legend=1,
        ax=None, dist2=[], hatches=[None,'//////']):
    """
    Fancier formatting to show effect of weighting.
    
    Top is discrete, bottom is mixed.
    """

    # Define any missing inputs: 
    if ax==None:
        ax = plt.subplot()
    
    
    # Set up plotting style:
    colour_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_list.append('DarkSlateGray')

    colour_1 = colour_list
    colour_2  = colour_list#['w' for colour in colour_list]

    hatch_1 = [hatches[0] for d in dist_1]
    hatch_2 = [hatches[1] for d in dist_2]

    ecolour_1 = ['k' for d in dist_1]
    ecolour_2 = ['k' for colour in colour_list]#[colour for colour in colour_list]

    # Define distributions, hatches and colours for the first row...
    dist_top = np.stack((dist_1,  dist_2), axis=1).ravel()
    hatch_top = np.stack((hatch_1, hatch_2), axis=1).ravel()
    colour_top = np.stack((colour_1, colour_2), axis=1).ravel()
    ecolour_top = np.stack((ecolour_1, ecolour_2), axis=1).ravel()

    # ... and the second:
    dist_bottom = np.concatenate((dist_1, dist_2))
    hatch_bottom = np.concatenate((hatch_1, hatch_2))
    colour_bottom = np.concatenate((colour_1, colour_2))
    ecolour_bottom = np.concatenate((ecolour_1, ecolour_2))

    # Make the plot as usual:
    if draw_bottom==1:
        # Draw t=0 distribution
        draw_horizontal_bar(dist_bottom, 
                            #label_bottom, 
                            y_top,
                            colour_bottom, 
                            hatch_bottom, ecolour_bottom,
                            bar_height=bar_height, ax=ax)
        if draw_legend==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])   # Legend below axis.
    if draw_top==1:
        # Draw no effect distribution
        draw_horizontal_bar(dist_top, #label_top, 
                            y_bottom,
                            colour_top, 
                            hatch_top, ecolour_top,
                            bar_height=bar_height, ax=ax)
        if draw_bottom==0 and draw_legend==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])
        
    # Second plot just to get the outlines looking right
    # draw_horizontal_bar(dist_1+dist_2, #label_top, 
    #                     y_top,
    #                     ['None' for d in dist_1+dist_2], linewidth=1,
    #                     bar_height=bar_height, ax=ax)
    draw_horizontal_bar(dist_1+dist_2, #label_bottom, 
                        y_bottom,
                        ['None' for d in dist_1+dist_2], linewidth=1,
                        bar_height=bar_height, ax=ax)

    if draw_bottom==1 and draw_top==1:     
        # Draw connecting lines
        draw_connections(dist_1, dist_2+dist_1,
                         top_of_bottom_bar=y_bottom+0.5*bar_height, 
                         bottom_of_top_bar=y_top-0.5*bar_height,
                         ax=ax)
        
