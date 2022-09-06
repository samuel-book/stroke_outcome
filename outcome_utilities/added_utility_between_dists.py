"""
Function to compare two mRS probability distributions and find the 
difference in utility across the full distributions. 

e.g. when both probability distributions have mRS=0, the difference
in utility is 0. When one has mRS=0 and the other mRS=1, the difference
is 0.97 - 0.88 = 0.09. 
"""
import numpy as np

def find_added_utility_between_dists(mRS_dist1, mRS_dist2, 
                                     utility_weights=[]):
    """
    Find the difference in utility between two mRS probability 
    distributions.
    
    Inputs:
    mRS_dist1       - np.array. mRS probability distribution 1.
    mRS_dist2       - np.array. mRS probability distribution 2.
    utility_weights - list or np.array. The utility weighting given to
                      each mRS value. If none given, a default is used.
    
    Returns:
    mRS_dist_mix - np.array. Cumulative probability distribution of
                   mRS_dist1 and mRS_dist2 combined and sorted. 
    added_utils  - 
    mRS_diff_mix - np.array. Non-cumulative probability distribution of
                   mRS_dist1 and mRS_dist2 combined and sorted. 
    """
    if len(utility_weights)<1:
        utility_weights = np.array(
            [0.97, 0.88, 0.74, 0.55, 0.20, -0.19, 0.00])
            
    # Combine the two mRS distributions into one ordered list:
    mRS_dist_mix = np.concatenate((mRS_dist1, mRS_dist2))
    # Sort and remove the duplicate 1.0 at the end: 
    mRS_dist_mix = np.sort(mRS_dist_mix)[:-1]
    # Add a 0.0 at the start:
    mRS_dist_mix = np.concatenate(([0.0], mRS_dist_mix))
    
    # Find the size of each bin (not cumulative):
    mRS_diff_mix = np.diff(mRS_dist_mix, prepend=0.0)

    # Store the mRS indices in here:
    x1_list = []
    x2_list = []
    # And store the utility values in here:
    u1_list = []
    u2_list = []
    for i, boundary in enumerate(mRS_dist_mix):
        # Find which mRS bin we're currently in: 
        x1 = np.digitize(boundary, mRS_dist1, right=True)
        x2 = np.digitize(boundary, mRS_dist2, right=True)
        
        # Store values: 
        x1_list.append(x1)
        x2_list.append(x2)
        u1_list.append(utility_weights[x1])
        u2_list.append(utility_weights[x2])
        
    # Find the increase in utility between dists 1 and 2:     
    added_utils = np.array(u1_list) - np.array(u2_list)
    
    # Weight the increases by the proportion of the mRS distribution
    # that they span: 
    weighted_added_utils = np.cumsum(added_utils * mRS_diff_mix)
    
    return mRS_dist_mix, weighted_added_utils