# Import packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from outcome_utilities.probs_with_time import find_mrs_constants

def plot_probs_filled(A,b,times_mins, colour_list=[], 
    ax=None, title=''):
    
    if ax==None:
        ax = plt.subplot()
    # P(mRS<=5)=1.0 at all times, so it has no defined A, a, and b.
    # Instead append to this array a 0.0, which won't be used directly
    # but will allow the "for" loop to go round one extra time.
    A = np.append(A,0.0)
    times_hours = times_mins/60.0

    for i,A_i in enumerate(A):
        if len(colour_list)>0:
            colour = colour_list[i]
        else:
            colour=None
        # Define the probability line, p_i:
        if i<6:
            p_i = 1.0/(1.0 + np.exp(-A_i -b[i]*times_mins)) 
        else:
            # P(mRS<=5)=1.0 at all times:
            p_i = np.full(times_mins.shape,1.0)
            
        # Plot it as before and store the colour used:
        ax.plot(times_hours, p_i, color=colour, label = r'$\leq$'+f'{i}')
            #, linewidth=1)
        
    ax.set_ylabel('Probability')
    ax.set_xlabel('Onset to treatment time (hours)')

    ax.set_ylim(0, 1)
    ax.set_xlim(times_hours[0],times_hours[-1])

    ax.set_xticks(np.arange(times_hours[0],times_hours[-1]+0.01,1))
    ax.set_xticks(np.arange(times_hours[0],times_hours[-1]+0.01,0.25), 
        minor=True)

    ax.set_yticks(np.arange(0,1.01,0.2))
    ax.set_yticks(np.arange(0,1.01,0.05), minor=True)
    ax.tick_params(top=True, bottom=True, left=True, right=True, which='both')

    ax.set_title(title)

# Load mRS distributions from file: 
mrs_dists_cumsum = pd.read_csv('./outcome_utilities/mrs_dist_probs_cumsum.csv', 
    index_col='Stroke type')
mrs_dists_bins = pd.read_csv('./outcome_utilities/mrs_dist_probs_bins.csv', 
    index_col='Stroke type')

t0_treatment_strings = [
    't0_treatment_nlvo_ivt',
    't0_treatment_lvo_ivt',
    't0_treatment_lvo_mt',
]
no_effect_strings = [
    'no_effect_nlvo_ivt_deaths',
    'no_effect_lvo_ivt_deaths',
    'no_effect_lvo_mt_deaths',
]

titles = [
    'nLVO treated with IVT',
    'LVO treated with IVT',
    'LVO treated with MT',
]

# Define maximum treatment times:
time_no_effect_ivt = int(6.3*60)   # minutes
time_no_effect_mt = int(8*60)      # minutes

fig, axs = plt.subplots(1,3, figsize=(15,4), gridspec_kw={'wspace':0.4})

for i in range(3):
    time_no_effect = (
        time_no_effect_mt if 'mt' in t0_treatment_strings[i] 
        else time_no_effect_ivt)
    times_to_plot = np.linspace(0, time_no_effect, 20)

    dist_cumsum_t0_treatment = \
        mrs_dists_cumsum.loc[t0_treatment_strings[i]].values
    dist_cumsum_no_effect = mrs_dists_cumsum.loc[no_effect_strings[i]].values

    a_list, b_list, A_list = find_mrs_constants(
        dist_cumsum_t0_treatment, dist_cumsum_no_effect, time_no_effect)

    plot_probs_filled(A_list, b_list, times_to_plot, ax=axs[i], title=titles[i], 
                      colour_list=['#0072B2', '#009E73', '#D55E00', '#CC79A7', '#F0E442', '#56B4E9',
       'DarkSlateGray'])
    
    axs[i].grid()
    axs[i].set_ylim(0.0, 1.02)
    
    if i<1:
        fig.legend(loc='upper center', bbox_to_anchor=[0.5,0.0], ncol=7, title='mRS')

plt.savefig('images/probs_with_time.jpg', dpi=300, bbox_inches='tight')
plt.show()