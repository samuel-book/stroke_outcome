"""
Beware, this file is long and horrid. 

Bespoke plotting functions to derive each mRS distribution.

To do, pep-8 this 
"""

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from outcome_utilities.dist_plot import draw_horizontal_bar, \
    draw_connections, draw_horizontal_bar_excess, \
    draw_horizontal_bar_weighted, draw_horizontal_bar_combo, \
    draw_horizontal_bar_combo_sum


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def plot_prestroke_excess(
    pre_stroke_nlvo_bins, pre_stroke_nlvo_bins_ivt_deaths,
    pre_stroke_lvo_bins, pre_stroke_lvo_bins_ivt_deaths,
    pre_stroke_lvo_bins_mt, pre_stroke_lvo_bins_mt_deaths):

    bh = 0.2 # bar height
    y_gap = 2.0*bh

    
    # Set up figure:
    fig = plt.figure(figsize=(18,5))
    gs = gridspec.GridSpec(1,3, wspace=0.8)
    
    ax_nlvo_ivt = plt.subplot(gs[0,0])
    ax_lvo_ivt = plt.subplot(gs[0,1])
    ax_lvo_mt = plt.subplot(gs[0,2])
    
    ax_nlvo_ivt.set_title('nLVO, IVT: treatment at t=0')
    ax_lvo_ivt.set_title('LVO, IVT: treatment at t=0')
    ax_lvo_mt.set_title('LVO, MT: treatment at t=0')
    
    y_labels = [
        [ # nLVO IVT:
        'Starting data:\nSAMueL-1 pre-stroke NIHSS<11',
        'Define excess deaths\n(1.1%)',
        'Apply excess deaths\n(1.1%)'
        ],
        [ # LVO IVT:
        'Starting data:\nSAMueL-1 pre-stroke NIHSS>10',
        'Define excess deaths\n(3.41%)',
        'Apply excess deaths\n(3.41%)'
        ],
        [# LVO MT:
        'Starting data:\nSAMueL-1 pre-stroke NIHSS>10',
        'Define excess deaths\n(3.6%)',
        'Apply excess deaths\n(3.6%)'
        ]]
        
    y_bars = np.arange(y_gap*len(y_labels[0]),0.0,-y_gap)[1:]
    
    bins_prestroke = [pre_stroke_nlvo_bins,
                      pre_stroke_lvo_bins,
                      pre_stroke_lvo_bins_mt]
    bins_deaths = [pre_stroke_nlvo_bins_ivt_deaths,
                   pre_stroke_lvo_bins_ivt_deaths,
                   pre_stroke_lvo_bins_mt_deaths]
    axs = [ax_nlvo_ivt, ax_lvo_ivt, ax_lvo_mt] 
    
    for i in range(3):
        ax = axs[i]
        bins_p = bins_prestroke[i]
        bins_d = bins_deaths[i]
        
        # Draw pre-stroke distribution:
        draw_horizontal_bar(bins_p, y_bars[0], bar_height=bh, 
                            ax=ax)
        if i==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[0.5,0.0,0.0,-0.5])  
            # Legend below axis.
            
        # Connect top and second bars:
        draw_connections(bins_p, 
                         bins_p,
                         bottom_of_top_bar=y_bars[0]-bh*0.5, 
                         top_of_bottom_bar=y_bars[1]+bh*0.5, 
                         ax=ax)
        # Draw excess death bars: 
        draw_horizontal_bar_excess(bins_p, 
                                   bins_d,
                                   bar_height=bh, 
                                   y_top=y_bars[1], y_bottom=y_bars[2],
                                   draw_legend=0,
                                   ax=ax)

        # Update the y-axis labels: 
        ax.set_yticks(y_bars)
        # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
        ax.set_yticklabels(y_labels[i])#yticklabels)


    for i,ax in enumerate(axs):
        # Add general content
        ax.set_xlabel('Probability')
        ax.set_xlim(0,1)
        # plt.gca().set_aspect(0.8)
    plt.show()
    

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def plot_noeffect_excess(
    no_treatment_nlvo_lvo_bins, no_treatment_nlvo_lvo_bins_ivt_deaths,
    no_treatment_lvo_bins, no_treatment_lvo_bins_ivt_deaths):

    bh = 0.2 # bar height
    y_gap = 2.0*bh
    
    # Set up figure:
    fig = plt.figure(figsize=(12,5))
    gs = gridspec.GridSpec(1,2, wspace=0.8)
    
    ax_nlvo_lvo_ivt = plt.subplot(gs[0,0])
    ax_lvo_ivt = plt.subplot(gs[0,1])
    
    ax_nlvo_lvo_ivt.set_title('nLVO+LVO, IVT: treatment at no-effect-time')
    ax_lvo_ivt.set_title('LVO, IVT: treatment at no-effect-time')
    
    y_labels = [
        [ # nLVO+LVO IVT:
        'Starting data:\nLees et al. 2010\nuntreated control group',
        'Define excess deaths\n(1.1%)',
        'Apply excess deaths\n(1.1%)'
        ],
        [ # LVO IVT:
        'Starting data:\nGoyal et al. 2016\nuntreated control group',
        'Define excess deaths\n(3.41%)',
        'Apply excess deaths\n(3.41%)'
        ]]
        
    y_bars = np.arange(y_gap*len(y_labels[0]),0.0,-y_gap)[1:]
    
    bins_noeffect = [no_treatment_nlvo_lvo_bins,
                     no_treatment_lvo_bins]
    bins_deaths = [no_treatment_nlvo_lvo_bins_ivt_deaths,
                   no_treatment_lvo_bins_ivt_deaths]
    axs = [ax_nlvo_lvo_ivt, ax_lvo_ivt] 
    
    for i in range(2):
        ax = axs[i]
        bins_p = bins_noeffect[i]
        bins_d = bins_deaths[i]
        
        # Draw pre-stroke distribution:
        draw_horizontal_bar(bins_p, y_bars[0], bar_height=bh, 
                            ax=ax)
        if i==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[-0.5,0.0,0.0,-0.5])  
            # Legend below axis.
            
        # Connect top and second bars:
        draw_connections(bins_p, 
                         bins_p,
                         bottom_of_top_bar=y_bars[0]-bh*0.5, 
                         top_of_bottom_bar=y_bars[1]+bh*0.5, 
                         ax=ax)
        # Draw excess death bars: 
        draw_horizontal_bar_excess(bins_p, 
                                   bins_d,
                                   bar_height=bh, 
                                   y_top=y_bars[1], y_bottom=y_bars[2],
                                   draw_legend=0,
                                   ax=ax)

        # Update the y-axis labels: 
        ax.set_yticks(y_bars)
        # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
        ax.set_yticklabels(y_labels[i])#yticklabels)


    for i,ax in enumerate(axs):
        # Add general content
        ax.set_xlabel('Probability')
        ax.set_xlim(0,1)
        # plt.gca().set_aspect(0.8)
    plt.show()
    
    
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def plot_noeffect_excess_mt(
    no_treatment_lvo_bins, no_treatment_lvo_bins_ivt_deaths,
    no_treatment_lvo_bins_mt, no_treatment_lvo_bins_mt_deaths):

    bh = 0.2 # bar height
    y_gap = 2.0*bh
    
    # Set up figure:
    fig = plt.figure(figsize=(12,5))
    gs = gridspec.GridSpec(1,2, wspace=0.8)
    
    ax_lvo_ivt = plt.subplot(gs[0,0])
    ax_lvo_mt = plt.subplot(gs[0,1])
    
    ax_lvo_ivt.set_title('LVO, IVT: treatment at no-effect-time')
    ax_lvo_mt.set_title('LVO, MT: treatment at no-effect-time')
    
    y_labels = [
        [ # nLVO+LVO IVT:
        'Starting data:\nGoyal et al. 2016\nuntreated control group',
        'Define excess deaths\n(3.41%)',
        'Apply excess deaths\n(3.41%)'
        ],
        [ # LVO IVT:
        'Starting data:\nGoyal et al. 2016\nuntreated control group',
        'Define excess deaths\n(3.6%)',
        'Apply excess deaths\n(3.6%)'
        ]]
        
    y_bars = np.arange(y_gap*len(y_labels[0]),0.0,-y_gap)[1:]
    
    bins_noeffect = [no_treatment_lvo_bins,
                     no_treatment_lvo_bins_mt]
    bins_deaths = [no_treatment_lvo_bins_ivt_deaths,
                   no_treatment_lvo_bins_mt_deaths]
    axs = [ax_lvo_ivt, ax_lvo_mt] 
    
    for i in range(2):
        ax = axs[i]
        bins_p = bins_noeffect[i]
        bins_d = bins_deaths[i]
        
        # Draw pre-stroke distribution:
        draw_horizontal_bar(bins_p, y_bars[0], bar_height=bh, 
                            ax=ax)
        if i==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=7, title='mRS', 
                       bbox_to_anchor=[-0.5,0.0,0.0,-0.5])  
            # Legend below axis.
            
        # Connect top and second bars:
        draw_connections(bins_p, 
                         bins_p,
                         bottom_of_top_bar=y_bars[0]-bh*0.5, 
                         top_of_bottom_bar=y_bars[1]+bh*0.5, 
                         ax=ax)
        # Draw excess death bars: 
        draw_horizontal_bar_excess(bins_p, 
                                   bins_d,
                                   bar_height=bh, 
                                   y_top=y_bars[1], y_bottom=y_bars[2],
                                   draw_legend=0,
                                   ax=ax)

        # Update the y-axis labels: 
        ax.set_yticks(y_bars)
        # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
        ax.set_yticklabels(y_labels[i])#yticklabels)


    for i,ax in enumerate(axs):
        # Add general content
        ax.set_xlabel('Probability')
        ax.set_xlim(0,1)
        # plt.gca().set_aspect(0.8)
    plt.show()
    
    

# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def plot_nlvo_noeffect(
    no_treatment_nlvo_lvo_bins, weight_nlvo_lvo,
    no_treatment_lvo_bins, weight_lvo):

    bh = 0.2 # bar height
    y_gap = 2.0*bh
    
    # width_ratios = [(1.0/3.0) for i in range(7)]
    # width_ratios[0] = weight_nlvo_lvo-(2.0/3.0)
    # width_ratios[3] = weight_nlvo_lvo-(2.0/3.0)
    
    # height_ratios = [1.0+bh+y_gap, 1.0]

    # Set up figure:
    fig = plt.figure(figsize=(15,12))
    gs = gridspec.GridSpec(2,7, wspace=1.0, hspace=0.6,
                           # width_ratios=width_ratios,
                           # height_ratios=height_ratios
                          )
    
    ax_nlvo_lvo = plt.subplot(gs[0,0:3])
    ax_lvo = plt.subplot(gs[0,4:7])
    ax_combo = plt.subplot(gs[1,2:5])
    
    ax_nlvo_lvo.set_title('nLVO+LVO, IVT: treatment at no-effect-time')
    ax_lvo.set_title('LVO, IVT: treatment at no-effect-time')
    ax_combo.set_title('nLVO, IVT: treatment at no-effect-time')
    
    y_labels = [
        [ # nLVO+LVO IVT:
        'Starting data:\nLees et al. 2010\nuntreated control group',
        f'Define weighted distribution\n(weighted data = {abs(weight_nlvo_lvo)*100-100.0:1.1f}% of start data)',
        f'Add the weights\n(new data = {abs(weight_nlvo_lvo)*100:1.1f}% of start data)'
        ],
        [ # LVO IVT:
        'Starting data:\nGoyal et al. 2016\nuntreated control group',
        f'Define weighted distribution\n(new data = {abs(weight_lvo)*100:1.1f}% of start data)',
        f'Subtract the weights\n(new data = {abs(weight_lvo)*100:1.1f}% of start data)'
        ],
        [ # Combined group:
        'Weighted nLVO+LVO:',
        'Draw minus weighted LVO\nfrom the end of each mRS bin',
        'Subtract LVO from nLVO+LVO' 
        ]]
        
    y_bars_top = np.arange(y_gap*len(y_labels[0]),0.0,-y_gap)[1:]
    y_bars_bottom = np.arange(y_gap*len(y_labels[-1]),0.0,-y_gap)[1:]
    if y_bars_bottom[-1]!=0.0:
        y_bars_bottom = np.append(y_bars_bottom,0.0)
    
    bins_noeffect = [no_treatment_nlvo_lvo_bins,
                     no_treatment_lvo_bins]
    # The "weight" for the combo bin is actually the target value
    # that determined the values of the weights. It doesn't affect
    # any sums but is marked on the final x-axis. 
    weights = [weight_nlvo_lvo,  weight_lvo, 0.46]
    axs = [ax_nlvo_lvo, ax_lvo, ax_combo] 
    hatches = [None, None]#'..']
    
    for i in range(2):
        ax = axs[i]
        bins_p = bins_noeffect[i]
        weight = weights[i]
        hatch = hatches[i]
        
        # Draw pre-stroke distribution:
        draw_horizontal_bar(bins_p, y_bars_top[0], bar_height=bh, 
                            ax=ax, hatch_list=[hatch for b in bins_p])
        if i==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=1, title='mRS', 
                       bbox_to_anchor=[1.2,0.5,0.0,0.0])  
            # Legend below axis.
            
        # Connect top and second bars:
        draw_connections(bins_p, 
                         bins_p,
                         bottom_of_top_bar=y_bars_top[0]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[1]+bh*0.5, 
                         ax=ax)
        # Draw weighted dist bars: 
        draw_horizontal_bar_weighted(bins_p, weight,
                                     y_top=y_bars_top[1], 
                                     y_bottom=y_bars_top[2],
                                     bar_height=bh, 
                                     draw_legend=0, 
                                     ax=ax,
                                     hatch=hatch)

        # Update the y-axis labels: 
        ax.set_yticks(y_bars_top)
        # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
        ax.set_yticklabels(y_labels[i])#yticklabels)
        
    # Combo axis
    ax = axs[2]
    bins_w1 = no_treatment_nlvo_lvo_bins * weight_nlvo_lvo
    bins_w2 = -no_treatment_lvo_bins * weight_lvo
    
    dist_1 = bins_w1 - bins_w2
    dist_2 = bins_w2
    
    # Draw the larger weighted one first:
    draw_horizontal_bar(bins_w1, y_bars_bottom[0], bar_height=bh, 
                        ax=ax)
        
    # Connect top and second bars:
    draw_connections(bins_w1, 
                     bins_w1,
                     bottom_of_top_bar=y_bars_bottom[0]-bh*0.5, 
                     top_of_bottom_bar=y_bars_bottom[1]+bh*0.5, 
                     ax=ax)
        
    # Draw weighted dist bars: 
    draw_horizontal_bar_combo(dist_1, dist_2,
                                 y_top=y_bars_bottom[1], 
                                 y_bottom=y_bars_bottom[2],
                                 bar_height=bh, 
                                 draw_legend=0, 
                                 ax=ax, 
                             #    hatches=hatches
                             )
    

    # Update the y-axis labels: 
    ax.set_yticks(y_bars_bottom)
    # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
    ax.set_yticklabels(y_labels[2])#yticklabels)


    for i,ax in enumerate(axs):
        # Add general content
        ax.set_xlabel('Probability')
        max_weight = np.max([weight_nlvo_lvo, weight_lvo])
        ax.set_xticks(np.sort(np.unique(np.concatenate((
            ax.get_xticks(), [abs(max_weight), abs(weights[i])])))))
        if abs(max_weight)<1.0:
            ax.set_xlim(0,1)
        else:
            ax.set_xlim(0, max_weight)
        ax.tick_params(rotation=55, axis='x')
        # plt.gca().set_aspect(0.8)
        
    # Draw some fancy arrows because why not 
    # Left-hand to bottom-central plot:
    plt.annotate('', 
                 (0.19,0.47), # tail 
                 (0.28,0.32), # head
                 arrowprops=dict(color='k', 
                                 arrowstyle='<|-,head_length=1,head_width=1', 
                                 linewidth=4, 
                                 connectionstyle='arc3,rad=-0.5'),
                 xycoords='figure fraction',
                 textcoords='figure fraction',
                 ha='center', va='center')
    # Right-hand to bottom-central plot: 
    plt.annotate('', 
             (0.72,0.47), # tail 
             (0.75,0.22), # head
             arrowprops=dict(color='k', 
                             arrowstyle='<|-,head_length=1,head_width=1', 
                             linewidth=4, 
                             connectionstyle='arc3,rad=0.5'),
             xycoords='figure fraction',
             textcoords='figure fraction',
             ha='center', va='center')
    plt.show()
    
    


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def plot_nlvo_noeffect_excess(
    no_treatment_nlvo_lvo_bins,
    no_treatment_nlvo_lvo_bins_ivt_deaths, 
    weight_nlvo_lvo,
    no_treatment_lvo_bins,
    no_treatment_lvo_bins_ivt_deaths, 
    weight_lvo):

    bh = 0.2 # bar height
    y_gap = 2.0*bh
    
    # width_ratios = [(1.0/3.0) for i in range(7)]
    # width_ratios[0] = weight_nlvo_lvo-(2.0/3.0)
    # width_ratios[3] = weight_nlvo_lvo-(2.0/3.0)
    
    height_ratios = [1.0+1.0*(bh+y_gap), 1.0]

    # Set up figure:
    fig = plt.figure(figsize=(15,15))
    gs = gridspec.GridSpec(2,7, wspace=1.0, hspace=0.6,
                           # width_ratios=width_ratios,
                           height_ratios=height_ratios
                          )
    
    ax_nlvo_lvo = plt.subplot(gs[0,0:3])
    ax_lvo = plt.subplot(gs[0,4:7])
    ax_combo = plt.subplot(gs[1,2:5])
    
    ax_nlvo_lvo.set_title('nLVO+LVO, IVT: treatment at no-effect-time')
    ax_lvo.set_title('LVO, IVT: treatment at no-effect-time')
    ax_combo.set_title('nLVO, IVT: treatment at no-effect-time')

    y_labels = [
        [ # nLVO+LVO IVT:
        'Starting data:\nLees et al. 2010\nuntreated control group',
        'Define excess deaths\n(1.1%)',
        'Apply excess deaths\n(1.1%)',
        f'Define weighted distribution\n(weighted data = {abs(weight_nlvo_lvo)*100-100.0:1.1f}% of start data)',
        f'Add the weights\n(new data = {abs(weight_nlvo_lvo)*100:1.1f}% of start data)'
        ],
        [ # LVO IVT:
        'Starting data:\nGoyal et al. 2016\nuntreated control group',
        'Define excess deaths\n(3.41%)',
        'Apply excess deaths\n(3.41%)',
        f'Define weighted distribution\n(new data = {abs(weight_lvo)*100:1.1f}% of start data)',
        f'Subtract the weights\n(new data = {abs(weight_lvo)*100:1.1f}% of start data)'
        ],
        [ # Combined group:
        'Weighted nLVO+LVO:',
        'Draw minus weighted LVO\nfrom the end of each mRS bin',
        'Subtract LVO from nLVO+LVO' 
        ]]

    # For the combo axis:
    bins_w1 = no_treatment_nlvo_lvo_bins_ivt_deaths * weight_nlvo_lvo
    bins_w2 = -no_treatment_lvo_bins_ivt_deaths * weight_lvo

    dist_1 = bins_w1 - bins_w2
    dist_2 = bins_w2

    weight_combo = 0.46
        
    y_bars_top = np.arange(y_gap*len(y_labels[0]),0.0,-y_gap)[1:]
    y_bars_bottom = np.arange(y_gap*len(y_labels[-1]),0.0,-y_gap)[1:]
    if y_bars_top[-1]!=0.0:
        y_bars_top = np.append(y_bars_top,0.0)
    if y_bars_bottom[-1]!=0.0:
        y_bars_bottom = np.append(y_bars_bottom,0.0)
        
    
    bins_noeffect = [no_treatment_nlvo_lvo_bins,
                     no_treatment_lvo_bins]
    bins_deaths = [no_treatment_nlvo_lvo_bins_ivt_deaths,
                   no_treatment_lvo_bins_ivt_deaths]
    # The "weight" for the combo bin is actually the target value
    # that determined the values of the weights. It doesn't affect
    # any sums but is marked on the final x-axis. 
    weights = [weight_nlvo_lvo,  weight_lvo, weight_combo]
    axs = [ax_nlvo_lvo, ax_lvo, ax_combo] 
    hatches = [None, None]#'..']
    
    for i in range(2):
        ax = axs[i]
        bins_p = bins_noeffect[i]
        bins_d = bins_deaths[i]
        weight = weights[i]
        hatch = hatches[i]
        
        # Draw pre-stroke distribution:
        draw_horizontal_bar(bins_p, y_bars_top[0], bar_height=bh, 
                            ax=ax, hatch_list=[hatch for b in bins_p])
        if i==1:
            # Add legend now to prevent doubling all the labels:
            ax.legend(loc='center',ncol=1, title='mRS', 
                       bbox_to_anchor=[1.2,0.5,0.0,0.0])  
            # Legend below axis.
            
        # Connect top and second bars:
        draw_connections(bins_p, 
                         bins_p,
                         bottom_of_top_bar=y_bars_top[0]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[1]+bh*0.5, 
                         ax=ax)
        
        # Draw excess death bars: 
        draw_horizontal_bar_excess(bins_p, 
                                   bins_d,
                                   bar_height=bh, 
                                   y_top=y_bars_top[1], 
                                   y_bottom=y_bars_top[2],
                                   draw_legend=0,
                                   ax=ax)
        
        
        # Connect top and second bars:
        draw_connections(bins_d, 
                         bins_d,
                         bottom_of_top_bar=y_bars_top[2]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[3]+bh*0.5, 
                         ax=ax)
        
        # Draw weighted dist bars: 
        draw_horizontal_bar_weighted(bins_d, weight,
                                     y_top=y_bars_top[3], 
                                     y_bottom=y_bars_top[4],
                                     bar_height=bh, 
                                     draw_legend=0, 
                                     ax=ax,
                                     hatch=hatch)

        # Update the y-axis labels: 
        ax.set_yticks(y_bars_top)
        # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
        ax.set_yticklabels(y_labels[i])#yticklabels)
        
    # Combo axis
    ax = axs[2]
    
    # Draw the larger weighted one first:
    draw_horizontal_bar(bins_w1, y_bars_bottom[0], bar_height=bh, 
                        ax=ax)
        
    # Connect top and second bars:
    draw_connections(bins_w1, 
                     bins_w1,
                     bottom_of_top_bar=y_bars_bottom[0]-bh*0.5, 
                     top_of_bottom_bar=y_bars_bottom[1]+bh*0.5, 
                     ax=ax)
        
    # Draw weighted dist bars: 
    draw_horizontal_bar_combo(dist_1, dist_2,
                                 y_top=y_bars_bottom[1], 
                                 y_bottom=y_bars_bottom[2],
                                 bar_height=bh, 
                                 draw_legend=0, 
                                 ax=ax, 
                             #    hatches=hatches
                             )
    

    # Update the y-axis labels: 
    ax.set_yticks(y_bars_bottom)
    # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
    ax.set_yticklabels(y_labels[2])#yticklabels)


    for i,ax in enumerate(axs):
        # Add general content
        ax.set_xlabel('Probability')
        max_weight = np.max([weight_nlvo_lvo, weight_lvo])
        ax.set_xticks(np.sort(np.unique(np.concatenate((
            ax.get_xticks(), [abs(max_weight), abs(weights[i])])))))
        if abs(max_weight)<1.0:
            ax.set_xlim(0,1)
        else:
            ax.set_xlim(0, max_weight)
        ax.tick_params(rotation=55, axis='x')
        # plt.gca().set_aspect(0.8)
        if i<2:
            ax.set_ylim(y_bars_top[-1]-y_gap*0.3, y_bars_top[0]+y_gap*0.3)
        else:
            ax.set_ylim(y_bars_bottom[-1]-y_gap*0.3, y_bars_bottom[0]+y_gap*0.3)
        
    # Draw some fancy arrows because why not 
    # Left-hand to bottom-central plot:
    plt.annotate('', 
                 (0.21,0.4), # tail 
                 (0.30,0.25), # head
                 arrowprops=dict(color='k', 
                                 arrowstyle='<|-,head_length=1,head_width=1', 
                                 linewidth=4, 
                                 connectionstyle='arc3,rad=-0.5'),
                 xycoords='figure fraction',
                 textcoords='figure fraction',
                 ha='center', va='center')
    # Right-hand to bottom-central plot: 
    plt.annotate('', 
             (0.72,0.4), # tail 
             (0.75,0.17), # head
             arrowprops=dict(color='k', 
                             arrowstyle='<|-,head_length=1,head_width=1', 
                             linewidth=4, 
                             connectionstyle='arc3,rad=0.5'),
             xycoords='figure fraction',
             textcoords='figure fraction',
             ha='center', va='center')
    plt.show()
    
    
    
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def plot_nlvo_t0_excess(
    no_treatment_nlvo_lvo_bins,
    no_treatment_nlvo_lvo_bins_ivt_deaths, 
    weight_nlvo_lvo,
    no_treatment_lvo_bins,
    no_treatment_lvo_bins_ivt_deaths, 
    weight_lvo):

    bh = 0.2 # bar height
    y_gap = 2.0*bh
    
    # width_ratios = [(1.0/3.0) for i in range(7)]
    # width_ratios[0] = weight_nlvo_lvo-(2.0/3.0)
    # width_ratios[3] = weight_nlvo_lvo-(2.0/3.0)
    
    height_ratios = [1.0+3.0*(bh+y_gap), 1.0]

    # Set up figure:
    fig = plt.figure(figsize=(15,15))
    gs = gridspec.GridSpec(2,7, wspace=1.0, hspace=0.6,
                           # width_ratios=width_ratios,
                           height_ratios=height_ratios
                          )
    
    ax_nlvo_lvo = plt.subplot(gs[0,0:3])
    ax_lvo = plt.subplot(gs[0,4:7])
    ax_combo = plt.subplot(gs[1,2:5])

    ax_nlvo_lvo.set_title('nLVO, IVT: pre-stroke distribution')
    ax_lvo.set_title('nLVO, IVT: treatment at no-effect-time')
    ax_combo.set_title('nLVO, IVT: treatment at t=0')

    y_labels = [
        [ # nLVO+LVO IVT:
        'Starting data:\nSAMueL-1 pre-stroke NIHSS<11',
        'Define excess deaths\n(1.1%)',
        'Apply excess deaths\n(1.1%)',
        f'Define weighted distribution\n(new data = {abs(weight_nlvo_lvo)*100:1.1f}% of start data)',
        f'Apply the weights\n(new data = {abs(weight_nlvo_lvo)*100:1.1f}% of start data)'
        ],
        [ # LVO IVT:
        'Starting data:\nLees et al. 2010\nuntreated control group',
        'Define excess deaths\n(1.1%)',
        'Apply excess deaths\n(1.1%)',
        f'Define weighted distribution\n(new data = {abs(weight_lvo)*100:1.1f}% of start data)',
        f'Apply the weights\n(new data = {abs(weight_lvo)*100:1.1f}% of start data)'
        ],
        [ # Combined group:
        'Sum the two weighted\ndistributions',
        'Sort into increasing mRS bins' 
        ]]

    weight_combo = 0.63
        
    y_bars_top = np.arange(y_gap*len(y_labels[0]),0.0,-y_gap)[1:]
    y_bars_bottom = np.arange(y_gap*len(y_labels[-1]),0.0,-y_gap)[1:]
    if y_bars_top[-1]!=0.0:
        y_bars_top = np.append(y_bars_top,0.0)
    if y_bars_bottom[-1]!=0.0:
        y_bars_bottom = np.append(y_bars_bottom,0.0)
        
    
    bins_noeffect = [no_treatment_nlvo_lvo_bins,
                     no_treatment_lvo_bins]
    bins_deaths = [no_treatment_nlvo_lvo_bins_ivt_deaths,
                   no_treatment_lvo_bins_ivt_deaths]
    # The "weight" for the combo bin is actually the target value
    # that determined the values of the weights. It doesn't affect
    # any sums but is marked on the final x-axis. 
    weights = [weight_nlvo_lvo,  weight_lvo, weight_combo]
    axs = [ax_nlvo_lvo, ax_lvo, ax_combo] 
    hatches = [None, '-']
    combo_hatches=hatches#[None, '---']
    
    for i in range(2):
        ax = axs[i]
        bins_p = bins_noeffect[i]
        bins_d = bins_deaths[i]
        weight = weights[i]
        hatch = hatches[i]
        
        # Draw pre-stroke distribution:
        draw_horizontal_bar(bins_p, y_bars_top[0], bar_height=bh, 
                            ax=ax, hatch_list=[hatch for b in bins_p])
        # if i==1:
        #     # Add legend now to prevent doubling all the labels:
        #     ax.legend(loc='center',ncol=1, title='mRS', 
        #                bbox_to_anchor=[1.2,0.5,0.0,0.0])  
        #     # Legend below axis.
            
        # Connect top and second bars:
        draw_connections(bins_p, 
                         bins_p,
                         bottom_of_top_bar=y_bars_top[0]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[1]+bh*0.5, 
                         ax=ax)
        
        # Draw excess death bars: 
        draw_horizontal_bar_excess(bins_p, 
                                   bins_d,
                                   bar_height=bh, 
                                   y_top=y_bars_top[1], 
                                   y_bottom=y_bars_top[2],
                                   draw_legend=0,
                                   ax=ax,
                                   hatch=hatch)
        
        
        # Connect top and second bars:
        draw_connections(bins_d, 
                         bins_d,
                         bottom_of_top_bar=y_bars_top[2]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[3]+bh*0.5, 
                         ax=ax)
        
        # Draw weighted dist bars: 
        draw_horizontal_bar_weighted(bins_d, weight,
                                     y_top=y_bars_top[3], 
                                     y_bottom=y_bars_top[4],
                                     bar_height=bh, 
                                     draw_legend=0, 
                                     ax=ax,
                                     hatch=hatch)

        # Update the y-axis labels: 
        ax.set_yticks(y_bars_top)
        # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
        ax.set_yticklabels(y_labels[i])#yticklabels)
        
    # Combo axis
    ax = axs[2]
        
    # For the combo axis:
    bins_w1 = no_treatment_nlvo_lvo_bins_ivt_deaths * weight_nlvo_lvo
    bins_w2 = no_treatment_lvo_bins_ivt_deaths * weight_lvo
    
    # Draw weighted dist bars: 
    draw_horizontal_bar_combo_sum(bins_w1, bins_w2,
                                 y_top=y_bars_bottom[0], 
                                 y_bottom=y_bars_bottom[1],
                                 bar_height=bh, 
                                 draw_legend=0, 
                                 ax=ax, 
                                 hatches=combo_hatches
                             )
    

    # Update the y-axis labels: 
    ax.set_yticks(y_bars_bottom)
    # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
    ax.set_yticklabels(y_labels[2])#yticklabels)


    for i,ax in enumerate(axs):
        # Add general content
        ax.set_xlabel('Probability')
        max_weight = np.max([weight_nlvo_lvo, weight_lvo])
        
        if abs(max_weight)<1.0:
            ax.set_xlim(0,1)
            ax.set_xticks(np.sort(np.unique(np.concatenate((
                ax.get_xticks(), [abs(weights[i])])))))
        else:
            ax.set_xlim(0, max_weight)
            ax.set_xticks(np.sort(np.unique(np.concatenate((
                ax.get_xticks(), [abs(max_weight), abs(weights[i])])))))
        ax.tick_params(rotation=55, axis='x')
        # plt.gca().set_aspect(0.8)
        if i<2:
            ax.set_ylim(y_bars_top[-1]-y_gap*0.3, y_bars_top[0]+y_gap*0.3)
        else:
            ax.set_ylim(y_bars_bottom[-1]-y_gap*0.3, y_bars_bottom[0]+y_gap*0.3)
        
    # Draw some fancy arrows because why not 
    # Left-hand to bottom-central plot:
    plt.annotate('', 
                 (0.21,0.33), # tail 
                 (0.30,0.15), # head
                 arrowprops=dict(color='k', 
                                 arrowstyle='<|-,head_length=1,head_width=1', 
                                 linewidth=4, 
                                 connectionstyle='arc3,rad=-0.5'),
                 xycoords='figure fraction',
                 textcoords='figure fraction',
                 ha='center', va='center')
    # Right-hand to bottom-central plot: 
    plt.annotate('', 
             (0.71,0.33), # tail 
             (0.71,0.15), # head
             arrowprops=dict(color='k', 
                             arrowstyle='<|-,head_length=1,head_width=1', 
                             linewidth=4, 
                             connectionstyle='arc3,rad=0.5'),
             xycoords='figure fraction',
             textcoords='figure fraction',
             ha='center', va='center')    
    
    # Legends
    dummies = []
    colour_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_list.append('DarkSlateGray')
    for i in range(7):
        dummy = plt.bar(np.NaN, 0.0, color=colour_list[i], edgecolor='k')
        dummies.append(dummy)
         
    dummy1 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=combo_hatches[0])
    dummy2 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=combo_hatches[1])
    dummy3 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch='////')
    dummy4 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch='//////')
    
    fig.legend([*dummies], range(7), 
              loc='lower left',ncol=1, title='mRS', 
              bbox_to_anchor=[0.7,0.15,0.0,0.0]) 
    fig.legend([dummy3, dummy4], 
              ['Excess deaths', 
               'Weighted proportion'],
               loc='lower left',
             bbox_to_anchor=[0.75,0.2,0.2,0.2])
    fig.legend([dummy1, dummy2], 
              ['Weighted pre-stroke distribution', 
               'Weighted no-effect distribution'],
               loc='lower left',
             bbox_to_anchor=[0.75,0.15,0.2,0.2])
        
    plt.show()
    

    
    
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def plot_lvo_t0_excess(
    pre_stroke_lvo_bins,
    pre_stroke_lvo_bins_ivt_deaths, 
    weight_pre_stroke_lvo,
    no_treatment_lvo_bins,
    no_treatment_lvo_bins_ivt_deaths, 
    weight_no_treatment_lvo):

    bh = 0.2 # bar height
    y_gap = 2.0*bh
    
    # width_ratios = [(1.0/3.0) for i in range(7)]
    # width_ratios[0] = weight_nlvo_lvo-(2.0/3.0)
    # width_ratios[3] = weight_nlvo_lvo-(2.0/3.0)
    
    height_ratios = [1.0+3.0*(bh+y_gap), 1.0]

    # Set up figure:
    fig = plt.figure(figsize=(15,15))
    gs = gridspec.GridSpec(2,7, wspace=1.0, hspace=0.6,
                           # width_ratios=width_ratios,
                           height_ratios=height_ratios
                          )
    
    ax_pre_stroke = plt.subplot(gs[0,0:3])
    ax_no_treatment = plt.subplot(gs[0,4:7])
    ax_combo = plt.subplot(gs[1,2:5])

    ax_pre_stroke.set_title('LVO, IVT: pre-stroke distribution')
    ax_no_treatment.set_title('LVO, IVT: treatment at no-effect-time')
    ax_combo.set_title('LVO, IVT: treatment at t=0')

    y_labels = [
        [ # pre-stroke LVO IVT:
        'Starting data:\nSAMueL-1 pre-stroke NIHSS>10',
        'Define excess deaths\n(3.41%)',
        'Apply excess deaths\n(3.41%)',
        f'Define weighted distribution\n(new data = {abs(weight_pre_stroke_lvo)*100:1.1f}% of start data)',
        f'Apply the weights\n(new data = {abs(weight_pre_stroke_lvo)*100:1.1f}% of start data)'
        ],
        [ # time-of-no-effect LVO IVT:
        'Starting data:\nGoyal et al. 2016\nuntreated control group',
        'Define excess deaths\n(3.41%)',
        'Apply excess deaths\n(3.41%)',
        f'Define weighted distribution\n(new data = {abs(weight_no_treatment_lvo)*100:1.1f}% of start data)',
        f'Apply the weights\n(new data = {abs(weight_no_treatment_lvo)*100:1.1f}% of start data)'
        ],
        [ # Combined group:
        'Sum the two weighted\ndistributions',
        'Sort into increasing mRS bins' 
        ]]

    weight_combo = 0.20
        
    y_bars_top = np.arange(y_gap*len(y_labels[0]),0.0,-y_gap)[1:]
    y_bars_bottom = np.arange(y_gap*len(y_labels[-1]),0.0,-y_gap)[1:]
    if y_bars_top[-1]!=0.0:
        y_bars_top = np.append(y_bars_top,0.0)
    if y_bars_bottom[-1]!=0.0:
        y_bars_bottom = np.append(y_bars_bottom,0.0)
        
    
    bins_noeffect = [pre_stroke_lvo_bins,
                     no_treatment_lvo_bins]
    bins_deaths = [pre_stroke_lvo_bins_ivt_deaths,
                   no_treatment_lvo_bins_ivt_deaths]
    # The "weight" for the combo bin is actually the target value
    # that determined the values of the weights. It doesn't affect
    # any sums but is marked on the final x-axis. 
    weights = [weight_pre_stroke_lvo,  weight_no_treatment_lvo, weight_combo]
    axs = [ax_pre_stroke, ax_no_treatment, ax_combo] 
    hatches = [None, '-']
    combo_hatches=hatches#[None, '---']
    
    for i in range(2):
        ax = axs[i]
        bins_p = bins_noeffect[i]
        bins_d = bins_deaths[i]
        weight = weights[i]
        hatch = hatches[i]
        
        # Draw pre-stroke distribution:
        draw_horizontal_bar(bins_p, y_bars_top[0], bar_height=bh, 
                            ax=ax, hatch_list=[hatch for b in bins_p])
        # if i==1:
        #     # Add legend now to prevent doubling all the labels:
        #     ax.legend(loc='center',ncol=1, title='mRS', 
        #                bbox_to_anchor=[1.2,0.5,0.0,0.0])  
        #     # Legend below axis.
            
        # Connect top and second bars:
        draw_connections(bins_p, 
                         bins_p,
                         bottom_of_top_bar=y_bars_top[0]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[1]+bh*0.5, 
                         ax=ax)
        
        # Draw excess death bars: 
        draw_horizontal_bar_excess(bins_p, 
                                   bins_d,
                                   bar_height=bh, 
                                   y_top=y_bars_top[1], 
                                   y_bottom=y_bars_top[2],
                                   draw_legend=0,
                                   ax=ax,
                                   hatch=hatch)
        
        
        # Connect top and second bars:
        draw_connections(bins_d, 
                         bins_d,
                         bottom_of_top_bar=y_bars_top[2]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[3]+bh*0.5, 
                         ax=ax)
        
        # Draw weighted dist bars: 
        draw_horizontal_bar_weighted(bins_d, weight,
                                     y_top=y_bars_top[3], 
                                     y_bottom=y_bars_top[4],
                                     bar_height=bh, 
                                     draw_legend=0, 
                                     ax=ax,
                                     hatch=hatch)

        # Update the y-axis labels: 
        ax.set_yticks(y_bars_top)
        # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
        ax.set_yticklabels(y_labels[i])#yticklabels)
        
    # Combo axis
    ax = axs[2]
        
    # For the combo axis:
    bins_w1 = pre_stroke_lvo_bins_ivt_deaths * weight_pre_stroke_lvo
    bins_w2 = no_treatment_lvo_bins_ivt_deaths * weight_no_treatment_lvo
    
    # Draw weighted dist bars: 
    draw_horizontal_bar_combo_sum(bins_w1, bins_w2,
                                 y_top=y_bars_bottom[0], 
                                 y_bottom=y_bars_bottom[1],
                                 bar_height=bh, 
                                 draw_legend=0, 
                                 ax=ax, 
                                 hatches=combo_hatches
                             )
    

    # Update the y-axis labels: 
    ax.set_yticks(y_bars_bottom)
    # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
    ax.set_yticklabels(y_labels[2])#yticklabels)


    for i,ax in enumerate(axs):
        # Add general content
        ax.set_xlabel('Probability')
        max_weight = np.max([weight_pre_stroke_lvo, weight_no_treatment_lvo])
        
        if abs(max_weight)<1.0:
            ax.set_xlim(0,1)
            ax.set_xticks(np.sort(np.unique(np.concatenate((
                ax.get_xticks(), [abs(weights[i])])))))
        else:
            ax.set_xlim(0, max_weight)
            ax.set_xticks(np.sort(np.unique(np.concatenate((
                ax.get_xticks(), [abs(max_weight), abs(weights[i])])))))
        ax.tick_params(rotation=55, axis='x')
        # plt.gca().set_aspect(0.8)
        if i<2:
            ax.set_ylim(y_bars_top[-1]-y_gap*0.3, y_bars_top[0]+y_gap*0.3)
        else:
            ax.set_ylim(y_bars_bottom[-1]-y_gap*0.3, y_bars_bottom[0]+y_gap*0.3)
        
    # Draw some fancy arrows because why not 
    # Left-hand to bottom-central plot:
    plt.annotate('', 
                 (0.21,0.33), # tail 
                 (0.30,0.15), # head
                 arrowprops=dict(color='k', 
                                 arrowstyle='<|-,head_length=1,head_width=1', 
                                 linewidth=4, 
                                 connectionstyle='arc3,rad=-0.5'),
                 xycoords='figure fraction',
                 textcoords='figure fraction',
                 ha='center', va='center')
    # Right-hand to bottom-central plot: 
    plt.annotate('', 
             (0.71,0.33), # tail 
             (0.71,0.15), # head
             arrowprops=dict(color='k', 
                             arrowstyle='<|-,head_length=1,head_width=1', 
                             linewidth=4, 
                             connectionstyle='arc3,rad=0.5'),
             xycoords='figure fraction',
             textcoords='figure fraction',
             ha='center', va='center')    
    
    # Legends
    dummies = []
    colour_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_list.append('DarkSlateGray')
    for i in range(7):
        dummy = plt.bar(np.NaN, 0.0, color=colour_list[i], edgecolor='k')
        dummies.append(dummy)
         
    dummy1 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=combo_hatches[0])
    dummy2 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=combo_hatches[1])
    dummy3 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch='////')
    dummy4 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch='//////')
    
    fig.legend([*dummies], range(7), 
              loc='lower left',ncol=1, title='mRS', 
              bbox_to_anchor=[0.7,0.15,0.0,0.0]) 
    fig.legend([dummy3, dummy4], 
              ['Excess deaths', 
               'Weighted proportion'],
               loc='lower left',
             bbox_to_anchor=[0.75,0.2,0.2,0.2])
    fig.legend([dummy1, dummy2], 
              ['Weighted pre-stroke distribution', 
               'Weighted no-effect distribution'],
               loc='lower left',
             bbox_to_anchor=[0.75,0.15,0.2,0.2])
        
    plt.show()


    
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
def plot_lvo_mt_t0_excess(
    pre_stroke_lvo_bins,
    pre_stroke_lvo_bins_mt_deaths, 
    weight_pre_stroke_lvo,
    no_treatment_lvo_bins,
    no_treatment_lvo_bins_mt_deaths, 
    weight_no_treatment_lvo):

    bh = 0.2 # bar height
    y_gap = 2.0*bh
    
    # width_ratios = [(1.0/3.0) for i in range(7)]
    # width_ratios[0] = weight_nlvo_lvo-(2.0/3.0)
    # width_ratios[3] = weight_nlvo_lvo-(2.0/3.0)
    
    height_ratios = [1.0+3.0*(bh+y_gap), 1.0]

    # Set up figure:
    fig = plt.figure(figsize=(15,15))
    gs = gridspec.GridSpec(2,7, wspace=1.0, hspace=0.6,
                           # width_ratios=width_ratios,
                           height_ratios=height_ratios
                          )
    
    ax_pre_stroke = plt.subplot(gs[0,0:3])
    ax_no_treatment = plt.subplot(gs[0,4:7])
    ax_combo = plt.subplot(gs[1,2:5])

    ax_pre_stroke.set_title('LVO, MT: pre-stroke distribution')
    ax_no_treatment.set_title('LVO, MT: treatment at no-effect-time')
    ax_combo.set_title('LVO, MT: treatment at t=0')

    y_labels = [
        [ # pre-stroke LVO IVT:
        'Starting data:\nSAMueL-1 pre-stroke NIHSS>10',
        'Define excess deaths\n(3.6%)',
        'Apply excess deaths\n(3.6%)',
        f'Define weighted distribution\n(new data = {abs(weight_pre_stroke_lvo)*100:1.1f}% of start data)',
        f'Apply the weights\n(new data = {abs(weight_pre_stroke_lvo)*100:1.1f}% of start data)'
        ],
        [ # time-of-no-effect LVO IVT:
        'Starting data:\nGoyal et al. 2016\nuntreated control group',
        'Define excess deaths\n(3.6%)',
        'Apply excess deaths\n(3.6%)',
        f'Define weighted distribution\n(new data = {abs(weight_no_treatment_lvo)*100:1.1f}% of start data)',
        f'Apply the weights\n(new data = {abs(weight_no_treatment_lvo)*100:1.1f}% of start data)'
        ],
        [ # Combined group:
        'Sum the two weighted\ndistributions',
        'Sort into increasing mRS bins' 
        ]]

    weight_combo = 0.0
        
    y_bars_top = np.arange(y_gap*len(y_labels[0]),0.0,-y_gap)[1:]
    y_bars_bottom = np.arange(y_gap*len(y_labels[-1]),0.0,-y_gap)[1:]
    if y_bars_top[-1]!=0.0:
        y_bars_top = np.append(y_bars_top,0.0)
    if y_bars_bottom[-1]!=0.0:
        y_bars_bottom = np.append(y_bars_bottom,0.0)
        
    
    bins_noeffect = [pre_stroke_lvo_bins,
                     no_treatment_lvo_bins]
    bins_deaths = [pre_stroke_lvo_bins_mt_deaths,
                   no_treatment_lvo_bins_mt_deaths]
    # The "weight" for the combo bin is actually the target value
    # that determined the values of the weights. It doesn't affect
    # any sums but is marked on the final x-axis. 
    weights = [weight_pre_stroke_lvo,  weight_no_treatment_lvo, weight_combo]
    axs = [ax_pre_stroke, ax_no_treatment, ax_combo] 
    hatches = [None, '-']
    combo_hatches=hatches#[None, '---']
    
    for i in range(2):
        ax = axs[i]
        bins_p = bins_noeffect[i]
        bins_d = bins_deaths[i]
        weight = weights[i]
        hatch = hatches[i]
        
        # Draw pre-stroke distribution:
        draw_horizontal_bar(bins_p, y_bars_top[0], bar_height=bh, 
                            ax=ax, hatch_list=[hatch for b in bins_p])
        # if i==1:
        #     # Add legend now to prevent doubling all the labels:
        #     ax.legend(loc='center',ncol=1, title='mRS', 
        #                bbox_to_anchor=[1.2,0.5,0.0,0.0])  
        #     # Legend below axis.
            
        # Connect top and second bars:
        draw_connections(bins_p, 
                         bins_p,
                         bottom_of_top_bar=y_bars_top[0]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[1]+bh*0.5, 
                         ax=ax)
        
        # Draw excess death bars: 
        draw_horizontal_bar_excess(bins_p, 
                                   bins_d,
                                   bar_height=bh, 
                                   y_top=y_bars_top[1], 
                                   y_bottom=y_bars_top[2],
                                   draw_legend=0,
                                   ax=ax,
                                   hatch=hatch)
        
        
        # Connect top and second bars:
        draw_connections(bins_d, 
                         bins_d,
                         bottom_of_top_bar=y_bars_top[2]-bh*0.5, 
                         top_of_bottom_bar=y_bars_top[3]+bh*0.5, 
                         ax=ax)
        
        # Draw weighted dist bars: 
        draw_horizontal_bar_weighted(bins_d, weight,
                                     y_top=y_bars_top[3], 
                                     y_bottom=y_bars_top[4],
                                     bar_height=bh, 
                                     draw_legend=0, 
                                     ax=ax,
                                     hatch=hatch)

        # Update the y-axis labels: 
        ax.set_yticks(y_bars_top)
        # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
        ax.set_yticklabels(y_labels[i])#yticklabels)
        
    # Combo axis
    ax = axs[2]
        
    # For the combo axis:
    bins_w1 = pre_stroke_lvo_bins_mt_deaths * weight_pre_stroke_lvo
    bins_w2 = no_treatment_lvo_bins_mt_deaths * weight_no_treatment_lvo
    
    # Draw weighted dist bars: 
    draw_horizontal_bar_combo_sum(bins_w1, bins_w2,
                                 y_top=y_bars_bottom[0], 
                                 y_bottom=y_bars_bottom[1],
                                 bar_height=bh, 
                                 draw_legend=0, 
                                 ax=ax, 
                                 hatches=combo_hatches
                             )
    

    # Update the y-axis labels: 
    ax.set_yticks(y_bars_bottom)
    # yticklabels = y_labels[i] if i<1 else ['' for y in y_bars]
    ax.set_yticklabels(y_labels[2])#yticklabels)


    for i,ax in enumerate(axs):
        # Add general content
        ax.set_xlabel('Probability')
        max_weight = np.max([weight_pre_stroke_lvo, weight_no_treatment_lvo])
        
        if abs(max_weight)<1.0:
            ax.set_xlim(0,1)
            ax.set_xticks(np.sort(np.unique(np.concatenate((
                ax.get_xticks(), [abs(weights[i])])))))
        else:
            ax.set_xlim(0, max_weight)
            ax.set_xticks(np.sort(np.unique(np.concatenate((
                ax.get_xticks(), [abs(max_weight), abs(weights[i])])))))
        ax.tick_params(rotation=55, axis='x')
        # plt.gca().set_aspect(0.8)
        if i<2:
            ax.set_ylim(y_bars_top[-1]-y_gap*0.3, y_bars_top[0]+y_gap*0.3)
        else:
            ax.set_ylim(y_bars_bottom[-1]-y_gap*0.3, y_bars_bottom[0]+y_gap*0.3)
        
    # Draw some fancy arrows because why not 
    # Left-hand to bottom-central plot:
    plt.annotate('', 
                 (0.21,0.33), # tail 
                 (0.30,0.15), # head
                 arrowprops=dict(color='k', 
                                 arrowstyle='<|-,head_length=1,head_width=1', 
                                 linewidth=4, 
                                 connectionstyle='arc3,rad=-0.5'),
                 xycoords='figure fraction',
                 textcoords='figure fraction',
                 ha='center', va='center')
    # Right-hand to bottom-central plot: 
    plt.annotate('', 
             (0.71,0.33), # tail 
             (0.71,0.15), # head
             arrowprops=dict(color='k', 
                             arrowstyle='<|-,head_length=1,head_width=1', 
                             linewidth=4, 
                             connectionstyle='arc3,rad=0.5'),
             xycoords='figure fraction',
             textcoords='figure fraction',
             ha='center', va='center')    
    
    # Legends
    dummies = []
    colour_list = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colour_list.append('DarkSlateGray')
    for i in range(7):
        dummy = plt.bar(np.NaN, 0.0, color=colour_list[i], edgecolor='k')
        dummies.append(dummy)
         
    dummy1 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=combo_hatches[0])
    dummy2 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch=combo_hatches[1])
    dummy3 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch='////')
    dummy4 = plt.bar(np.NaN, 0.0, color='w', edgecolor='k', hatch='//////')
    
    fig.legend([*dummies], range(7), 
              loc='lower left',ncol=1, title='mRS', 
              bbox_to_anchor=[0.7,0.15,0.0,0.0]) 
    fig.legend([dummy3, dummy4], 
              ['Excess deaths', 
               'Weighted proportion'],
               loc='lower left',
             bbox_to_anchor=[0.75,0.2,0.2,0.2])
    fig.legend([dummy1, dummy2], 
              ['Weighted pre-stroke distribution', 
               'Weighted no-effect distribution'],
               loc='lower left',
             bbox_to_anchor=[0.75,0.15,0.2,0.2])
        
    plt.show()    
    
    
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------