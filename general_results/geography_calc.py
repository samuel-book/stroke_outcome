"""
Calculate everything to do with travel and outcome grids.
"""
# Import packages
import numpy as np
import pandas as pd
import copy
# For keeping track of files:
import os
from dataclasses import dataclass

# Custom packages:
from stroke_outcome.continuous_outcome import Continuous_outcome


def main(fixed_times, patient_proportions_dict, grid_step=1):
    """
    Run them.
    """
    # Usual care:
    (grid_time_travel_usual_care,
     dict_travel_grid_usual_care,
     dict_dfs_outcomes_usual_care) = build_outcome_grids(
        fixed_times['ivt_x'],
        fixed_times['ivt_y'],
        fixed_times['usual_care_ivt'],
        fixed_times['usual_care_mt'],
        patient_proportions_dict,
        time_travel_max=fixed_times['travel_ivt_to_mt'],
        grid_step=grid_step,
    )
    # Mothership:
    (grid_time_travel_mothership,
     dict_travel_grid_mothership,
     dict_dfs_outcomes_mothership) = build_outcome_grids(
        fixed_times['mt_x'],
        fixed_times['mt_y'],
        fixed_times['mothership_ivt'],
        fixed_times['mothership_mt'],
        patient_proportions_dict,
        time_travel_max=fixed_times['travel_ivt_to_mt'],
        grid_step=grid_step
    )
    # Differences:
    grid_time_travel_diff = (
        grid_time_travel_usual_care -
        grid_time_travel_mothership
        )
    dict_travel_grid_diff = dict()
    for key, value in dict_travel_grid_usual_care.items():
        dict_travel_grid_diff[f'usual_care_{key}'] = value
    for key, value in dict_travel_grid_mothership.items():
        dict_travel_grid_diff[f'mothership_{key}'] = value

    dict_dfs_outcomes_diff = dict()
    for key in list(dict_dfs_outcomes_usual_care.keys()):
        dict_dfs_outcomes_diff[key] = (
            dict_dfs_outcomes_mothership[key] -
            dict_dfs_outcomes_usual_care[key]
            )

    # Gather results:
    dict_grid_time_travel = dict(
        usual_care=grid_time_travel_usual_care,
        mothership=grid_time_travel_mothership,
        diff=grid_time_travel_diff,
    )
    dict_grid_time_travel_info = dict(
        usual_care=dict_travel_grid_usual_care,
        mothership=dict_travel_grid_mothership,
        diff=dict_travel_grid_diff
    )
    dict_outcomes_dicts = dict(
        usual_care=dict_dfs_outcomes_usual_care,
        mothership=dict_dfs_outcomes_mothership,
        diff=dict_dfs_outcomes_diff
    )
    return (
        dict_grid_time_travel,
        dict_grid_time_travel_info,
        dict_outcomes_dicts
        )


def build_outcome_grids(
        unit_x,
        unit_y,
        time_to_ivt_excl_travel_to_first_unit,
        time_to_mt_excl_travel_to_first_unit,
        patient_proportions_dict,
        time_travel_max=None,
        grid_step=None,
    ):
    """
    Run through the functions to make outcome grids.
    """
    outcome_cols = [
        'added_utility', 'mean_mrs', 'mrs_less_equal_2', 'mrs_shift']

    # Usual care:
    grid_time_travel_usual_care, dict_travel_grid_usual_care = (
        build_travel_grid(
            unit_x,
            unit_y,
            time_travel_max,
            grid_step
        ))
    df_times_usual_care = create_df_time_to_treatment(
        time_to_ivt_excl_travel_to_first_unit,
        time_to_mt_excl_travel_to_first_unit,
        grid_time_travel_usual_care
        )
    # Build the inputs for the outcome model for each cohort:
    dict_dfs_outcomes_usual_care = create_outcome_model_inputs(df_times_usual_care)
    # Run the outcome model for each cohort:
    for key, df in dict_dfs_outcomes_usual_care.items():
        dict_dfs_outcomes_usual_care[key] = run_outcome_model(df)
    # Combine cohort outcomes:
    dict_dfs_outcomes_usual_care['mixed'] = combine_outcomes_treated_ischaemic(
        dict_dfs_outcomes_usual_care['nlvo_ivt'],
        dict_dfs_outcomes_usual_care['lvo_ivt_only'],
        dict_dfs_outcomes_usual_care['lvo_ivt_mt'],
        dict_dfs_outcomes_usual_care['lvo_mt_only'],
        patient_proportions_dict,
        outcome_cols
    )
    dict_dfs_outcomes_usual_care['lvo'] = combine_outcomes_lvo(
        dict_dfs_outcomes_usual_care['lvo_ivt_only'],
        dict_dfs_outcomes_usual_care['lvo_ivt_mt'],
        dict_dfs_outcomes_usual_care['lvo_mt_only'],
        patient_proportions_dict,
        outcome_cols,
        )
    return grid_time_travel_usual_care, dict_travel_grid_usual_care, dict_dfs_outcomes_usual_care


def build_travel_grid(
        unit_x,
        unit_y,
        time_travel_max=None,
        grid_step=None
        ):

    if time_travel_max is None:
        # Use either a default value of 60 minutes or the greater
        # of that value and the distance from the grid centre to the
        # stroke unit.
        time_travel_max = max([np.sqrt(unit_x**2.0 + unit_y**2.0), 60.0])
    if grid_step is None:
        grid_step = 1

    # Keep a copy of the useful parameters in a dictionary that can
    # be saved and reloaded for future use.
    dict_travel_grid = dict(
        unit_x=unit_x,
        unit_y=unit_y,
        # Only calculate travel times up to this x or y displacement:
        time_travel_max=time_travel_max,
        # Change how granular the grid is.
        grid_step=grid_step,  # minutes
    )
    # Make the grid a bit larger than the max travel time:
    dict_travel_grid['grid_xy_max'] = (
        dict_travel_grid['time_travel_max'] +
        dict_travel_grid['grid_step'] * 2
    )

    # Build the grids:
    grid_time_travel = make_time_grid(
        dict_travel_grid['grid_xy_max'],
        dict_travel_grid['grid_step'],
        x_offset=dict_travel_grid['unit_x'],
        y_offset=dict_travel_grid['unit_y']
    )
    # Round the times to three decimal places (should be plenty):
    grid_time_travel = np.round(grid_time_travel, 3)

    return grid_time_travel, dict_travel_grid


def make_time_grid(
        xy_max,
        step,
        x_offset=0,
        y_offset=0
        ):
    """
    Define a helper function to build the time grid:
    """
    # Times for each row....
    x_times = np.arange(-xy_max, xy_max + step, step) - x_offset
    # ... and each column.
    y_times = np.arange(-xy_max, xy_max + step, step) - y_offset
    # The offsets shift the position of (0,0) from the grid centre 
    # to (x_offset, y_offset). Distances will be calculated from the
    # latter point.

    # Mesh to create new grids by stacking rows (xx) and columns (yy):
    xx, yy = np.meshgrid(x_times, y_times)

    # Then combine the two temporary grids to find distances:
    radial_times = np.sqrt(xx**2.0 + yy**2.0)
    return radial_times


def create_df_time_to_treatment(
        time_to_ivt_excl_travel_to_first_unit,
        time_to_mt_excl_travel_to_first_unit,
        grid_time_travel_directly
        ):
    # Treatment times:
    df = pd.DataFrame()
    df['onset_to_needle_mins'] = (
        time_to_ivt_excl_travel_to_first_unit +
        grid_time_travel_directly.flatten()
    )
    df['onset_to_puncture_mins'] = (
        time_to_mt_excl_travel_to_first_unit +
        grid_time_travel_directly.flatten()
    )
    return df


def create_outcome_model_inputs(
        df=None
        ):
    ## Create outcome model inputs

    if df is None:
        # Create an empty DataFrame.
        # When the patient info is put in, there will only
        # be one patient in total.
        df = pd.DataFrame()

    # Assign three cohorts to these treatment times.
    # nLVO with IVT:
    df_nlvo_ivt = df.copy()
    df_nlvo_ivt['stroke_type_code'] = 1
    df_nlvo_ivt['ivt_chosen_bool'] = 1
    df_nlvo_ivt['mt_chosen_bool'] = 0

    # LVO with IVT only:
    df_lvo_ivt = df.copy()
    df_lvo_ivt['stroke_type_code'] = 2
    df_lvo_ivt['ivt_chosen_bool'] = 1
    df_lvo_ivt['mt_chosen_bool'] = 0

    # LVO with both IVT and MT:
    df_lvo_ivt_mt = df.copy()
    df_lvo_ivt_mt['stroke_type_code'] = 2
    df_lvo_ivt_mt['ivt_chosen_bool'] = 1
    df_lvo_ivt_mt['mt_chosen_bool'] = 1

    # LVO with MT only:
    df_lvo_mt = df.copy()
    df_lvo_mt['stroke_type_code'] = 2
    df_lvo_mt['ivt_chosen_bool'] = 0
    df_lvo_mt['mt_chosen_bool'] = 1

    # Gather results:
    dict_dfs_outcome_inputs = {
        'nlvo_ivt': df_nlvo_ivt,
        'lvo_ivt_only': df_lvo_ivt,
        'lvo_ivt_mt': df_lvo_ivt_mt,
        'lvo_mt_only': df_lvo_mt,
    }

    return dict_dfs_outcome_inputs


def run_outcome_model(df):
    ## Calculate outcomes

    # Set up outcome model
    outcome_model = Continuous_outcome()

    outcome_model.assign_patients_to_trial(df)

    # Calculate outcomes:
    patient_data_dict, outcomes_by_stroke_type, full_cohort_outcomes = (
        outcome_model.calculate_outcomes())

    # Make a copy of the results:
    outcomes_by_stroke_type = copy.copy(outcomes_by_stroke_type)
    full_cohort_outcomes = copy.copy(full_cohort_outcomes)

    # Place the relevant results into the starting dataframe:
    df['added_utility'] = full_cohort_outcomes['each_patient_utility_shift']
    df['mean_mrs'] = full_cohort_outcomes['each_patient_mrs_post_stroke']
    df['mrs_less_equal_2'] = full_cohort_outcomes['each_patient_mrs_dist_post_stroke'][:, 2]
    df['mrs_shift'] = full_cohort_outcomes['each_patient_mrs_shift']

    return df


def combine_outcomes_treated_ischaemic(
        df_nlvo_ivt,
        df_lvo_ivt,
        df_lvo_ivt_mt,
        df_lvo_mt,
        patient_proportions,
        outcome_cols=[]
    ):
    """
    ## Combine outcomes

    Combine the data in these columns:


    ### Combine outcomes for treated ischaemic population

    The following function combines the data from multiple dataframes, one for each cohort, in the proportions requested:
    """
    if len(outcome_cols) == 0:
        outcome_cols = ['added_utility', 'mean_mrs', 'mrs_less_equal_2', 'mrs_shift']
    # Combine the outcomes:
    df_mixed = pd.DataFrame(
        np.sum((
            patient_proportions['nlvo_ivt'] * df_nlvo_ivt[outcome_cols],
            patient_proportions['lvo_ivt_only'] * df_lvo_ivt[outcome_cols],
            patient_proportions['lvo_ivt_mt'] * df_lvo_ivt_mt[outcome_cols],
            patient_proportions['lvo_mt_only'] * df_lvo_mt[outcome_cols],
        ), axis=0),
        columns=outcome_cols
    )

    prop_ischaemic_treated = np.sum((
        patient_proportions['nlvo_ivt'],
        patient_proportions['lvo_ivt_only'],
        patient_proportions['lvo_ivt_mt'],
        patient_proportions['lvo_mt_only'],
    ))

    # Adjust outcomes for just the treated population:
    df_mixed = df_mixed / prop_ischaemic_treated

    # Copy over the treatment times.
    # They're the same times in all three dataframes so just pick the nLVO IVT df:
    df_mixed['onset_to_needle_mins'] = df_nlvo_ivt['onset_to_needle_mins']
    df_mixed['onset_to_puncture_mins'] = df_nlvo_ivt['onset_to_puncture_mins']
    return df_mixed


def combine_outcomes_lvo(
        df_lvo_ivt,
        df_lvo_ivt_mt,
        df_lvo_mt,
        patient_proportions,
        outcome_cols,
        ):
    """
    ### Combine outcomes for LVO with various treatments

    The following function combines the data from multiple dataframes, one for each cohort, in the proportions requested:
    """
    if len(outcome_cols) == 0:
        outcome_cols = ['added_utility', 'mean_mrs', 'mrs_less_equal_2', 'mrs_shift']

    # Combine the outcomes:
    df_lvo = pd.DataFrame(
        np.sum((
            patient_proportions['lvo_ivt_only'] * df_lvo_ivt[outcome_cols],
            patient_proportions['lvo_ivt_mt'] * df_lvo_ivt_mt[outcome_cols],
            patient_proportions['lvo_mt_only'] * df_lvo_mt[outcome_cols],
        ), axis=0),
        columns=outcome_cols
    )

    prop_lvo_treated = np.sum((
        patient_proportions['lvo_ivt_only'],
        patient_proportions['lvo_ivt_mt'],
        patient_proportions['lvo_mt_only'],
    ))

    # Adjust outcomes for just the treated population:
    df_lvo = df_lvo / prop_lvo_treated

    # Copy over the treatment times.
    # They're the same times in all three dataframes so just pick the LVO IVT df:
    df_lvo['onset_to_needle_mins'] = df_lvo_ivt['onset_to_needle_mins']
    df_lvo['onset_to_puncture_mins'] = df_lvo_ivt['onset_to_puncture_mins']
    return df_lvo
