import numpy as np

def scale_dist(mrs_prob_bins,p_ref,mRS_ref):
    """
    Scale an existing probability distribution to a new data point.

    Inputs:
    mrs_prob_bins - list or np.array. Prob. dist to be scaled.
    p_ref         - float. Reference probability.
    mRS_ref       - int. The mRS bin of this reference probability.

    Returns:.
    mrs_prob_dist_sc - np.array. Prob. dist after scaling.
    mrs_prob_bins_sc - np.array. Cumulative prob. dist after scaling.
    """
    # Store the scaled bins in mrs_prob_bins_sc:
    mrs_prob_bins_sc = []

    for mRS in range(7):
        if mRS<=mRS_ref:
            # For the points below the new reference p_ref.
            # Find the size ratio of this bin to the mRS<=mRS_ref bin.
            # When mRS=mRS_ref, ratio=1.
            ratio = mrs_prob_bins[mRS] / mrs_prob_bins[mRS_ref]
            # Scale the bins:
            mrs_prob_bins_sc.append(p_ref * ratio)
        else:
            # For the points above the new reference p_ref.
            # Find the size ratio of this bin excluding mRS<=mRS_ref,
            # with size (mrs_prob_bins[mRS]-mrs_prob_bins[mRS_ref]),
            # to the mRS>mRS_ref bin,
            # with size (1-mrs_prob_bins[mRS_ref]).
            ratio = ((mrs_prob_bins[mRS] - mrs_prob_bins[mRS_ref]) /
                     (1 - mrs_prob_bins[mRS_ref]))
            # Scale the bins:
            mrs_prob_bins_sc.append(p_ref + (1-p_ref)*ratio)

    mrs_prob_bins_sc = np.array(mrs_prob_bins_sc)
    # Use bins to obtain distribution
    mrs_prob_dist_sc = np.diff(np.concatenate(([0.0],mrs_prob_bins_sc)))

    return mrs_prob_dist_sc, mrs_prob_bins_sc
