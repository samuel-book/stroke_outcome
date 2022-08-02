"""
Store the mRS probability distributions in here.
Where data are calculated instead of taken directly from the sources,
the calculations are described in the mRS_datasets.ipynb notebook.
Each distribution ending `_mrs6` includes the probability(mRS=6) data
when applicable, else P(mRS=6) is set to zero.
Invalid or missing data is set to a probability of minus 1.
Each dictionary contains:
+ 'dist_mrs6' -
+ 'dist'      -
+ 'bins'      -
List of dictionaries defined here:
dict_pre_stroke, dict_pre_stroke_nlvo, dict_pre_stroke_lvo,
dict_t0_treatment_ich,      dict_no_treatment_ich,
dict_t0_treatment_nlvo_lvo, dict_no_treatment_nlvo_lvo,
dict_t0_treatment_lvo,      dict_no_treatment_lvo,
dict_t0_treatment_lvo_ivt,  dict_no_treatment_lvo_ivt,
dict_t0_treatment_lvo_mt,  dict_no_treatment_lvo_mt,
dict_t0_treatment_nlvo,     dict_no_treatment_nlvo,
dict_t0_treatment_nlvo_ivt, dict_no_treatment_nlvo_ivt
"""

prop_ischaemnic_stroke_lvo = 0.23

# ###############################
# ########### IMPORTS ###########
# ###############################
import numpy as np

# Chnage local import depending on whether code is being run as __main__
if __name__ == '__main__':
    from scale_dist import scale_dist
    from extrapolate_odds_ratio import extrapolate_odds_ratio
else:
    from .scale_dist import scale_dist
    from .extrapolate_odds_ratio import extrapolate_odds_ratio

# ###############################
# ########## FUNCTIONS ##########
# ###############################

def make_cumulative_probability(dist):
    """Make cumulative probability from a probability distribution."""
    return np.cumsum(dist)

def fill_dict(dict):
    """
    Populate the dictionary with cumulative probability distribution.
    """
    # Cumulative probability distribution:
    dict['bins'] = make_cumulative_probability(dict['dist_mrs6'])
    return dict

def make_weighted_dist(dists, weights):
    """Make a new distribution by summing weighted distributions."""
    weighted_dist = np.sum(weights * dists, axis=0)

    # Change the dtype because the input weights array had the dtype
    # 'object' and we needn't retain it.
    #weighted_dist = weighted_dist.astype(float)
    return weighted_dist

# ###############################
# ########## DATA SETS ##########
# ###############################

# Not Applicable dictionary - contains junk data.
dict_na = dict()
# Distribution including mRS=6:
dict_na['dist_mrs6'] = np.array([-1]*7)
dict_na['bins'] = dict_na['dist_mrs6']

# ########## Pre-stroke ##########
# Source: SAMueL-1 dataset.
# By definition, probability(mRS=6)=0 here.

# All ischaemic patients
dict_pre_stroke = dict()
# Distribution including mRS=6:
dict_pre_stroke['dist_mrs6'] = np.array([
    0.534923, 0.157958, 0.108075,
    0.119199, 0.062649, 0.017196, 0.0
    ])
dict_pre_stroke = fill_dict(dict_pre_stroke)

# NIHSS 0-10 (surrogate for nLVO)
dict_pre_stroke_nlvo = dict()
dict_pre_stroke_nlvo['dist_mrs6'] = np.array([
    0.582881, 0.162538, 0.103440,
    0.102223, 0.041973, 0.006945, 0.0
    ])
dict_pre_stroke_nlvo = fill_dict(dict_pre_stroke_nlvo)

# NIHSS 11+ (surrogate for LVO)
dict_pre_stroke_lvo = dict()
dict_pre_stroke_lvo['dist_mrs6'] = np.array([
    0.417894, 0.142959, 0.118430,
    0.164211, 0.113775, 0.042731, 0.0
    ])
dict_pre_stroke_lvo = fill_dict(dict_pre_stroke_lvo)

# ########## Haemorrhagic ##########
# ---------- t=0 treatment ----------
# N/A
dict_t0_treatment_ich = dict_na

# ---------- no treatment ----------
dict_no_treatment_ich = dict_na



# ########## nLVO and LVO combined no treatment ##########

# Source: Lees et al. 2010.
dict_no_treatment_nlvo_lvo = dict()
dict_no_treatment_nlvo_lvo['dist_mrs6'] = np.array([
    0.14861582, 0.2022106, 0.12525408,
    0.13965201, 0.1806092, 0.08612256, 0.11753573
    ])
dict_no_treatment_nlvo_lvo = fill_dict(dict_no_treatment_nlvo_lvo)
# This is above t=0 because it is used to calculate the t=0 dist.

# ---------- t=0 treatment  ----------
# Not currently used
dict_t0_treatment_nlvo_lvo = dict_na

# ########## LVO - untreated ##########
# ---------- no treatment ----------
# Source: Goyal et al. 2016, Figure 1 (A Overall, Control population).
dict_no_treatment_lvo = dict()
# Distribution including mRS=6:
dict_no_treatment_lvo['dist_mrs6'] = np.array([
    0.050, 0.079, 0.136,
    0.164, 0.247, 0.135, 0.189
    ])
dict_no_treatment_lvo = fill_dict(dict_no_treatment_lvo)
# Set t=o treatment as same as untreated
dict_t0_treatment_lvo = dict_no_treatment_lvo


# ########## LVO - thrombolysis only ##########
# ---------- t=0 treatment ----------
# Distribution is a weighted combination of pre_stroke and
# no_treatment_lvo excluding their mRS=6 entries.
# Sources: SAMueL-1 dataset (pre-stroke distribution),
#          Goyal et al. 2016 (LVO no treatment distribution).
dict_t0_treatment_lvo_ivt = dict()
# Define the weights:
weight_pre_stroke_lvo_ivt   = 0.18
weight_no_treatment_lvo_ivt = 0.82
# Distribution including mRS=6:
dict_t0_treatment_lvo_ivt['dist_mrs6'] = make_weighted_dist(
    np.array([dict_pre_stroke_lvo['dist_mrs6'],
              dict_no_treatment_lvo['dist_mrs6']]),
    np.array([[weight_pre_stroke_lvo_ivt],
              [weight_no_treatment_lvo_ivt]], dtype=object)
    )
dict_t0_treatment_lvo_ivt = fill_dict(dict_t0_treatment_lvo_ivt)

# ---------- no treatment ----------
# Use the general LVO distribution.
dict_no_treatment_lvo_ivt = dict_no_treatment_lvo

# ########## LVO - thrombectomy ##########

# ---------- no treatment ----------
# Use the general LVO distribution.
dict_no_treatment_lvo_mt = dict_no_treatment_lvo

# ---------- t=0 treatment ----------
# Distribution is a weighted combination of pre_stroke and
# no_treatment_lvo  their mRS=6 entries.
# Hui et al. reported 75% successful recanalisation with thrombectomy.
# Fransen et al reported on mRS 0-2 outcomes for those successfuly reperfused
# by thrombectomy. When extrapolting this back to t=0 this gives 68% mRS <= 2,
# exactly the same as out pre-stroke mRS distribution, giving strength to the
# vire that reperufion at t=0 would restore pre-stroke disabilty level.

dict_t0_treatment_lvo_etc = dict()
# Find the mRS<=1 values:
p_mrsleq1_pre_stroke           = dict_pre_stroke_lvo['bins'][2]
p_mrsleq1_no_treatment_lvo_etc = dict_no_treatment_lvo_mt['bins'][2]
# Define the weights:
weight_pre_stroke_lvo_etc = 0.75
    
weight_no_treatment_lvo_etc = 1.0 - weight_pre_stroke_lvo_etc
# Distribution including mRS=6:
dict_t0_treatment_lvo_etc['dist_mrs6'] = make_weighted_dist(
    np.array([dict_pre_stroke_lvo['dist_mrs6'],
              dict_no_treatment_lvo_mt['dist_mrs6']]),
    np.array([[weight_pre_stroke_lvo_etc],
              [weight_no_treatment_lvo_etc]], dtype=object)
    )
dict_t0_treatment_lvo_mt = fill_dict(dict_t0_treatment_lvo_etc)

# ########## nLVO - untreated ##########

# Distribution is a weighted difference of (nLVO and LVO) and
# (just LVO) at the no-treatment time, excluding their mRS=6 entries.
# Then the distribution is scaled to match the
# P(mRS<=1, t=no-effect-time) data from Holodinsky et al. 2018.
# Assume 38% ischaemic strokes are LVO
# Sources: Lees et al. 2010,
#          Goyal et al. 2016, Figure 1 (A Overall, Control population),
#          Holodinsky et al. 2018 (probability P(mRS<=1, t=t_ne)=0.46).
# 

dict_no_treatment_nlvo = dict()
# Define the weights:
weight_no_treatment_nlvo_lvo = 1.0
weight_no_treatment_lvo      = -prop_ischaemnic_stroke_lvo
# Distribution including mRS=6:
dict_no_treatment_nlvo['dist_mrs6'] = make_weighted_dist(
    np.array([dict_no_treatment_nlvo_lvo['dist_mrs6'],
              dict_no_treatment_lvo['dist_mrs6']]),
    np.array([[weight_no_treatment_nlvo_lvo],
              [weight_no_treatment_lvo]], dtype=object)
    )
# Normalise
dict_no_treatment_nlvo['dist_mrs6'] =  (dict_no_treatment_nlvo['dist_mrs6'] / 
    np.sum(dict_no_treatment_nlvo['dist_mrs6']))

dict_no_treatment_nlvo = fill_dict(dict_no_treatment_nlvo)

# Further scaling to match known data point:
p_mrsleq1_tne = 0.46
dict_no_treatment_nlvo['dist_mrs6'], dict_no_treatment_nlvo['bins'] = (
    scale_dist(dict_no_treatment_nlvo['bins'], p_mrsleq1_tne, mRS_ref=1))

# Set t=0 same as no tretament
dict_t0_treatment_nlvo = dict_no_treatment_nlvo

# ########## nLVO - thrombolysis only ##########
# ---------- no treatment ----------
# Use the general nLVO distribution.
dict_no_treatment_nlvo_ivt = dict_no_treatment_nlvo
# This is above t=0 because it is used in the t=0 calculation.

# ---------- t=0 treatment ----------
# Distribution is a weighted combination of pre_stroke and
# no_treatment_nlvo excluding their mRS=6 entries.
# The weights are chosen to match a known data point, probability
# P(mRS<=1, t=0)=0.63 (from Holodinsky et al. 2018).
# Sources: SAMueL-1 dataset (pre-stroke distribution),
#          Goyal et al. 2016 (LVO no treatment distribution),
#          Holodinsky et al. 2018 (probability P(mRS<=1, t=0)=0.63).
dict_t0_treatment_nlvo_ivt = dict()
# Find the mRS<=1 values:
p_mrsleq1_pre_stroke            = dict_pre_stroke_nlvo['bins'][1]
p_mrsleq1_no_treatment_nlvo_ivt = dict_no_treatment_nlvo_ivt['bins'][1]
# Define the weights:
weight_pre_stroke_nlvo_ivt   = (
    (0.63 - p_mrsleq1_no_treatment_nlvo_ivt) /
    (p_mrsleq1_pre_stroke - p_mrsleq1_no_treatment_nlvo_ivt)
    )
weight_no_treatment_nlvo_ivt = 1.0 - weight_pre_stroke_nlvo_ivt
# Distribution including mRS=6:
dict_t0_treatment_nlvo_ivt['dist_mrs6'] = make_weighted_dist(
    np.array([dict_pre_stroke_nlvo['dist_mrs6'],
              dict_no_treatment_nlvo_ivt['dist_mrs6']]),
    np.array([[weight_pre_stroke_nlvo_ivt],
              [weight_no_treatment_nlvo_ivt]], dtype=object)
    )
dict_t0_treatment_nlvo_ivt = fill_dict(dict_t0_treatment_nlvo_ivt)



