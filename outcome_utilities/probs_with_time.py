"""
Helper functions for setting up probability variation with time.

find_mrs_constants - find a,b,A constants.
find_mrs_bins_t    - find bins at time t.
"""
# ###############################
# ########### IMPORTS ###########
# ###############################
import numpy as np


# ###############################
# ########## FUNCTIONS ##########
# ###############################
def find_mrs_constants(mrs_prob_bins_t0_treatment, 
    mrs_prob_bins_no_treatment, t_ne):
    """
    Find constants a,b,A for calculating probability with time.

    Inputs:
    mrs_prob_bins_t0_treatment - list or np.array. Cumulative probability 
                                 bins at t=0.
    mrs_prob_bins_no_treatment - list or np.array. Cumulative probability 
                                 bins at the no-effect time.
    t_ne                       - int or float. The no-effect time.

    Returns:
    a, b, A - arrays of five values, one for each mRS<=0,1,2,3,4. 
              See the mathematics notebook for usage.
    """
    # Use the [:-1] slice to exclude mRS<=5.
    G_t0  = np.log(      mrs_prob_bins_t0_treatment[:-1])
    B_t0  = np.log(1.0 - mrs_prob_bins_t0_treatment[:-1])
    G_tne = np.log(      mrs_prob_bins_no_treatment[:-1])
    B_tne = np.log(1.0 - mrs_prob_bins_no_treatment[:-1])

    a = (G_t0 - B_t0) - (G_tne - B_tne)
    b = -a/t_ne
    A = a + (G_tne - B_tne)

    return a, b, A


def find_mrs_bins_t(A, b, treatment_time):
    """
    Find the cumulative probability bins at a given time. 

    Inputs:
    A,b            - list or np.array. Contain constants for 
                     calculating probability.
    treatment_time - int or float. Time from onset to treatment. 

    Returns:
    mrs_prob_bins_t_treatment - np.array. Cumulative probabilities
                                of the mRS bins at the treatment time.
    """
    mrs_prob_bins_t_treatment = []
    for i,A_i in enumerate(A):
        p_i = 1.0/(1.0 + np.exp(-A_i -b[i]*treatment_time)) 
        mrs_prob_bins_t_treatment.append(p_i)

    return np.array(mrs_prob_bins_t_treatment)