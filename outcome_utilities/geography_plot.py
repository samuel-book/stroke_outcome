"""
A place to dump all of the big plotting functions from the geography 
notebook.
"""
import numpy as np
import matplotlib.pyplot as plt
# For two_grids_and_diff:
import matplotlib.gridspec as gridspec
# For circle_plot:
from matplotlib.path    import Path
from matplotlib.patches import PathPatch

def plot_two_grids_and_diff(grid1, grid2, grid_diff,
        titles=['','',''], cbar_labels=['',''], extent=None, 
        vlims=[[],[]], cmaps=[None, None],
        ivt_coords=[np.NaN, np.NaN], mt_coords=[np.NaN, np.NaN], 
        plot_contours=0, contour_levels=[], return_axes=0,
        xlabel='Travel time in x (mins)', ylabel='Travel time in y (mins)'):
    """
    Plot two grids + shared colourbar and the difference grid + colourbar.
    
    The resulting figure looks like this:
    +--+ +--+ ,   +--+ ,
    |  | |  | |   |  | |
    +--+ +--+ '   +--+ '
    Grid Grid     Diff
     1    2       (1-2)
     
    It is optional to draw contours over the difference grid imshow 
    but it's fiddly.
    
    Inputs:
    ---                                                               WRITE ME
    
    Returns:
    ---                                                               WRITE ME
    """

    # Define some variables if defaults not given: 
    if len(vlims[0])<1:
        vlims = [[np.min([grid1, grid2]), np.max([grid1, grid2])], vlims[1]]
    if len(vlims[1])<1:
        vlims = [vlims[0], [np.min(grid_diff), np.max(grid_diff)]]
    
    # Figure setup:
    fig = plt.figure(figsize=(16,4))
    gs = gridspec.GridSpec(1, 6, width_ratios=(32,32,1,16,32,1), wspace=0.01)
    # Subplots:
    ax_grid1 = plt.subplot(gs[0,0])
    ax_grid2 = plt.subplot(gs[0,1])
    ax_cbar1 = plt.subplot(gs[0,2])
    # (leave gs[0,3] blank on purpose)
    ax_gridd = plt.subplot(gs[0,4])
    ax_cbard = plt.subplot(gs[0,5])
    
    
    # Draw grids 1 and 2, and their shared colourbar:
    g = ax_grid1.imshow(grid1, origin='lower', extent=extent, 
                        vmin=vlims[0][0], vmax=vlims[0][1], cmap=cmaps[0])
    ax_grid2.imshow(grid2, origin='lower', extent=extent, 
                    vmin=vlims[0][0], vmax=vlims[0][1], cmap=cmaps[0])
    plt.colorbar(g, cax=ax_cbar1, label=cbar_labels[0])
    
    # Draw the difference grid and its colourbar: 
    d = ax_gridd.imshow(grid_diff, origin='lower', extent=extent, 
                        vmin=vlims[1][0], vmax=vlims[1][1], cmap=cmaps[1])
    plt.colorbar(d, cax=ax_cbard, label=cbar_labels[1])
    
    
    if plot_contours>0:
        # Add contours over the difference grid imshow. 
        if len(contour_levels)<1:
            # If no levels specified, define some now:
            contour_levels = None#np.linspace(vlims[1][0], vlims[1][1], 10)[1:-1]
        img1 = ax_gridd.contour(grid_diff, extent=extent,
                                levels=contour_levels,
                                colors='k', linewidths=0.5)
        # Add value label to each contour line:
        ax_gridd.clabel(img1, inline=True, fontsize=10)
        # Usually wise to reset the aspect after drawing contours:
        ax_gridd.set_aspect('equal')
        
    # Format the axes:
    for i, ax in enumerate([ax_grid1, ax_grid2, ax_gridd]):
        ax.set_title(titles[i])
        # Mark the treatment centre locations:
        ax.scatter(*ivt_coords, marker='o', color='k', edgecolor='w', s=50)
        ax.scatter(*mt_coords,  marker='D', color='k', edgecolor='w', s=50)
        # Axis labels:
        ax.set_xlabel(xlabel)
        if i!=1:
            ax.set_ylabel(ylabel)
        # Ticks on all sides:
        ax.tick_params(top=True, bottom=True, left=True, right=True, which='both')
    # Remove tick labels from the left-hand-side of axis 2, 
    # else they'll clash with axis 1. Meant to be sharing a y-axis. 
    ax_grid2.set_yticklabels([])
    
    if return_axes==1:
        return [ax_grid1, ax_grid2, ax_cbar1, ax_gridd, ax_cbard]
    
    
# ------
# ----- Radiating circles plot -----

def circle_plot(grid, travel_ivt_to_mt, time_travel_max, time_step_circle, 
                vmin, vmax, extent=None, circ_linewidth=0.5, imshow=1, 
                cmap='viridis', 
                cbar_label='', cbar_format_str=None, 
                n_contour_steps=5, levels=[], 
                ivt_coords=[np.NaN, np.NaN], mt_coords=[np.NaN, np.NaN],
                return_ax=0, ax=None, cax=None, cbar_orientation=None,
                cbar_ticks=None):
    """
    
    
    The resulting figure looks like this, but less ugly:
       ________
      / ______ \    ||
     / / ,__, \ \   ||
    | | |,__,| | |  ||
     \_\______/_/   ||
    
    Inputs:
    ---                                                               WRITE ME
    
    Returns:
    ---                                                               WRITE ME
    """
    if ax==None:
        fig, ax = plt.subplots(figsize=(10,6))

    # ----- Treatment centres ----- 
    # Mark the treatment centre locations:
    ax.scatter(*ivt_coords, marker='o', color='k', s=50, zorder=5, 
               label='IVT centre')
    ax.scatter(*mt_coords, marker='D', color='k', s=50, 
               label='IVT+MT centre')
    # And draw a connecting line:
    ax.plot([ivt_coords[0],mt_coords[0]], 
            [ivt_coords[1],mt_coords[1]], color='k')


    # ----- Radiating circles ----- 
    # Define times for the radiating circles:
    circle_times = np.arange(time_step_circle, 
        time_travel_max + time_step_circle, time_step_circle)

    # Define coordinates and plot the radiating circles:
    for travel_time in circle_times:
        if travel_time<time_travel_max:
            # Don't show the flat bottom line (gets thickened) 
            trunc_val = np.NaN
        else:
            # Show the flat bottom line 
            trunc_val = None
        # Define coordinates of the travel time circle.
        x_circ, y_circ = make_coords_truncated_circle(
            travel_time, travel_ivt_to_mt, trunc_val=trunc_val)

        if travel_time<time_travel_max:
            ax.plot(x_circ, y_circ, color='k', linewidth=circ_linewidth)
        else:
            # Make a patch using these coordinates. 
            # Use np.stack to get a series of ((x,y), (x,y), ... (x,y)) coords.
            circle_path  = Path(np.stack((x_circ,y_circ),axis=1))
            circle_patch = PathPatch(circle_path, 
                                     edgecolor='k', facecolor='None',
                                     linewidth = circ_linewidth)
            # Draw the patch:
            ax.add_patch(circle_patch)


    # ----- Grid of times ----- 
    if imshow>0:
        # Draw the grid as usual:
        imshow_grid = ax.imshow(grid, origin='lower', 
                                extent=extent, cmap=cmap,
                                vmin=vmin, vmax=vmax
                               )
        # Remove everything outside the biggest radiating circle:
        imshow_grid.set_clip_path(circle_patch)
        # Colourbar:
        if cax==None:
            cbar = plt.colorbar(imshow_grid, ax=ax, label=cbar_label, 
                                orientation=cbar_orientation,
                               ticks=cbar_ticks)
        else:
            cbar = plt.colorbar(imshow_grid, cax=cax, label=cbar_label, 
                                orientation=cbar_orientation,
                               ticks=cbar_ticks)
    else:
        if len(levels)<1:
            levels = np.linspace(vmin, vmax, n_contour_steps+1)
        # Draw the grid as usual:
        contours = ax.contourf(grid, origin='lower', 
                               extent=extent, cmap=cmap, 
                               levels=levels)
        # Remove everything outside the biggest radiating circle:
        for line in contours.collections:
            line.set_clip_path(circle_patch)
        # Colourbar:
        if cax==None:
            cbar = plt.colorbar(contours, ax=ax, label=cbar_label, 
                                orientation=cbar_orientation,
                                spacing='proportional',
                                ticks=cbar_ticks)
        else:
            cbar = plt.colorbar(contours, cax=cax, label=cbar_label, 
                                orientation=cbar_orientation,
                                spacing='proportional', ticks=cbar_ticks)
            

    if cbar_format_str != None:
        cbar.ax.set_yticklabels(
            [cbar_format_str.format(i) for i in cbar.get_ticks()]) 
        
        
    # ----- Other setup -----
    ax.set_aspect('equal')
    ax.set_xlim(-time_travel_max*1.02, time_travel_max*1.02)
    ax.set_ylim(-travel_ivt_to_mt-15, time_travel_max+15)
    
    ax.set_xlabel('x co-ordinate (time from IVT-only unit, minutes)')
    ax.set_ylabel('y co-ordinate (time from IVT-only unit, minutes)')
    
    if return_ax==1:
        return ax

    
def make_coords_truncated_circle(time_travel, time_travel_ivt_to_mt, 
                                 trunc_val=None, n_coords=360):
    """
    Helper function to draw radiating circles from the IVT centre.
    """
    # Find the point halfway between the treatment centres:
    y_halfway = -0.5*time_travel_ivt_to_mt
    if trunc_val == None:
        trunc_val = y_halfway
    
    # Make a normal circle...
    angles_circle = np.linspace(0,2.0*np.pi,n_coords)
    x_circ = time_travel * np.sin(angles_circle)
    y_circ = time_travel * np.cos(angles_circle)
    # ... then cut it off at the halfway point between the treatment 
    # centres:
    y_circ[np.where(y_circ < y_halfway)] = trunc_val 

    return x_circ, y_circ


def find_mask_within_flattened_circle(grid_diff, grid_ivt, time_travel_max):
    """
    # Determine the coordinates in the area of the largest flattened
    # circle. 
    """
    # Make a copy of the grid that we'll delete invalid values from:
    grid_vals_uncovered = np.zeros_like(grid_diff)
    
    # Find values below the flat circle bottom:
    y_grid_halfway = np.where(grid_diff == np.nanmin(np.abs(grid_diff)))[0][0]
    
    # Find values outside the radius of the largest circle:
    coords_outside_max_time = np.where(grid_ivt > time_travel_max)
    
    # Remove unwanted values:
    grid_vals_uncovered[:y_grid_halfway]         = 1
    grid_vals_uncovered[coords_outside_max_time] = 1
    
    return grid_vals_uncovered



