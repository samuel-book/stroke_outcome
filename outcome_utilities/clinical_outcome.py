import numpy as np
import pandas as pd

class Clinical_outcome:
    """
    Predicts modified Rankin Scale (mRS) distributions for ischaemic stroke
    patients depending on time to treatment with intravenous thrombolysis (IVT)
    or mechanical thrombectomy (MT). Results are broken down for large vessel
    occulusions (LVO) and non large vessel occlusions (nLVO).

    Inputs
    ------

    A Pandas DataFrame object of mRS distributions for:
    1) Untreated nLVO
    2) nLVO treated at t=0 (time of stroke onset) with IVT
    3) nLVO treated at time of no-effect (includes treatment deaths)
    4) Untreated LVO
    5) LVO treated at t=0 (time of stroke onset) with IVT
    6) LVO treated with IVT at time of no-effect (includes treatment deaths)
    7) LVO treated at t=0 (time of stroke onset) with IVT
    8) LVO treated with IVT at time of no-effect (includes treatment deaths)

    Time of IVT and MT.

    Outputs
    -------

    mRS distributions (bins & cumulative), changes in dists, and mean mRS, for:
    1) LVO untreated
    2) nLVO untreated
    3) LVO treated with IVT
    4) LVO treated with MT
    5) nLVO treated with IVT

    mRS mean shift (compared with untreated) and proportion of patients with
    improved mRS for:
    1) LVO treated with IVT
    2) LVO treated with MT
    3) nLVO treated with IVT

    Utility-weighted mRS
    --------------------

    In addition to mRS we may calculate utility-weighted mRS. Utility is an
    estimated quality of life (0=dead, 1=full quality of life, neagtive numbers
    indicate a 'worse than death' outcome).

    mRS Utility scores are based on a pooled Analysis of 20 000+ Patients. From
    Wang X, Moullaali TJ, Li Q, Berge E, Robinson TG, Lindley R, et al. 
    Utility-Weighted Modified Rankin Scale Scores for the Assessment of Stroke
    Outcome. Stroke. 2020 Aug 1;51(8):2411-7. 

    | mRS Score | 0    | 1    | 2    | 3    | 4    | 5     | 6    |
    |-----------|------|------|------|------|------|-------|------|
    | Utility   | 0.97 | 0.88 | 0.74 | 0.55 | 0.20 | -0.19 | 0.00 |

    General methodology
    -------------------

    The model assumes that log odds of mRS <= x declines uniformally with time.
    The imported distribution give mRS <= x probabilities at t=0 (time of
    stroke onset) and time of no effect. These two distributions are converted
    to log odds and weighted according to the fraction of time, in relation to
    when the treatment no longer has an effect, that has passed. The weighted
    log odds distribution is converted back to probability of mRS <= x. mRS
    are also converted to a utility-weighted mRS.

    The time to no-effect is taken as:
    1) 6.3 hours for IVT
      (from Emberson et al, https://doi.org/10.1016/S0140-6736(14)60584-5.)
    2) 8 hours for MT
      (from Fransen et al; https://doi.org/10.1001/jamaneurol.2015.3886.
      this analysis did not include late-presenting patients selected by
      advanced imaging).

    1,000 (default #) patients are then sampled from the untreated and treated
    distributions (samples may be taken randomly or evenly spaced).
    This gives sampled mRS distributions. The shift in mRS for each patient
    between untreated and treated distribution is also calculated. A negative
    shift is indicative of improvement (lower MRS disability score).
    """

    def __init__(self, mrs_dists):
        """
        Constructor for clinical outcome model.

        Input: 
        ------

        mRS distributions for untreated, t=0 treatment, and treatment at
        time of no effect (which also includes treatment-related excess deaths).



        """
        self.name = "Clinical outcome model"

        # Store modified Rankin Scale distributions as arrays in dictionary
        self.mrs_distribution_probs = dict()
        self.mrs_distribution_logodds = dict()
        for index, row in mrs_dists.iterrows():
            p = np.array([row[str(x)] for x in range(7)])
            self.mrs_distribution_probs[index] = p
            # Convert to log odds
            o = p / (1 - p)
            self.mrs_distribution_logodds[index] = np.log(o)

        # Set general model parameters
        self.ivt_time_no_effect = 6.3 * 60
        self.mt_time_no_effect = 8 * 60

        # Store utility weightings for mRS 0-6
        self.utility_weights = \
                np.array([0.97, 0.88, 0.74, 0.55, 0.20, -0.19, 0.00])
                
    def calculate_outcomes(
        self, time_to_ivt, time_to_mt, patients=1000, random_spacing=False):
        """
        Calls methods to model mRS populations for:
        1) LVO untreated
        2) nLVO untreated
        3) LVO treated with IVT
        4) LVO treated with MT
        5) nLVO treated with IVT

        These are converted into cumulative probabilties, mean mRS, mRS shift,
        and proportion of patients with improved mRS.

        Returns:
        --------

        A results dictionary with:

        mRS distributions (bins & cumulative), changes in dists, and mean mRS
        for:
            1) LVO untreated
            2) nLVO untreated
            3) LVO treated with IVT
            4) LVO treated with MT
            5) nLVO treated with IVT

        mRS mean shift (compared with untreated) and proportion of patients with
        improved mRS for:
            1) LVO treated with IVT
            2) LVO treated with MT
            3) nLVO treated with IVT

        """

        # Set up results dictionary
        results = dict()
        
        # Get sample patient probabilities
        if random_spacing:
            x = np.random.rand(patients)
        else:
            x = np.linspace(0.00001, 0.99999, patients)

        # Get treatment results
        lvo_ivt_outcomes = self.calculate_outcomes_for_lvo_ivt(time_to_ivt, x)
        lvo_mt_outcomes = self.calculate_outcomes_for_lvo_mt(time_to_mt, x)
        nlvo_ivt_outcomes = self.calculate_outcomes_for_nlvo_ivt(time_to_ivt, x)

        # Get counts by mRS (histograms)
        lvo_untreated_hist = np.histogram(
            lvo_ivt_outcomes['untreated_mrs'], bins=range(8))[0]
        nlvo_untreated_hist = np.histogram(
            nlvo_ivt_outcomes['untreated_mrs'], bins=range(8))[0]
        lvo_ivt_hist = np.histogram(
            lvo_ivt_outcomes['treated_mrs'], bins=range(8))[0]
        lvo_mt_hist = np.histogram(
            lvo_mt_outcomes['treated_mrs'], bins=range(8))[0]
        nlvo_ivt_hist = np.histogram(
            nlvo_ivt_outcomes['treated_mrs'], bins=range(8))[0]
        
        # Convert to probabilities and store
        results['lvo_untreated_probs']  = \
                lvo_untreated_hist / lvo_untreated_hist.sum()
        results['nlvo_untreated_probs'] = \
            nlvo_untreated_hist / nlvo_untreated_hist.sum()
        results['lvo_ivt_probs'] = lvo_ivt_hist / lvo_ivt_hist.sum()
        results['lvo_mt_probs'] = lvo_mt_hist / lvo_mt_hist.sum()
        results['nlvo_ivt_probs'] = nlvo_ivt_hist / nlvo_ivt_hist.sum()

        # Convert to utility-weighted_mRS and store
        results['lvo_untreated_mean_utility'] = \
            np.sum(results['lvo_untreated_probs'] * self.utility_weights)
        results['nlvo_untreated_mean_utility'] = \
            np.sum(results['nlvo_untreated_probs'] * self.utility_weights)
        results['lvo_ivt_mean_utility'] = \
            np.sum(results['lvo_ivt_probs'] * self.utility_weights)
        results['lvo_mt_mean_utility'] = \
            np.sum(results['lvo_mt_probs'] * self.utility_weights)
        results['nlvo_ivt_mean_utility'] = \
            np.sum(results['nlvo_ivt_probs'] * self.utility_weights)
        
        # Calculate added utility and store
        results['lvo_ivt_added_utility'] = (results['lvo_ivt_mean_utility'] - 
            results['lvo_untreated_mean_utility'])
        results['lvo_mt_added_utility'] = (results['lvo_mt_mean_utility'] - 
            results['lvo_untreated_mean_utility'])
        results['nlvo_ivt_added_utility'] = (results['nlvo_ivt_mean_utility'] - 
            results['nlvo_untreated_mean_utility'])

        # Get cumulative probabilities and store in results
        results['lvo_untreated_cum_probs']  = \
            np.cumsum(lvo_untreated_hist) / lvo_untreated_hist.sum()
        results['nlvo_untreated_cum_probs'] = \
            np.cumsum(nlvo_untreated_hist) / nlvo_untreated_hist.sum()
        results['lvo_ivt_cum_probs'] = \
            np.cumsum(lvo_ivt_hist) / lvo_ivt_hist.sum()
        results['lvo_mt_cum_probs'] = \
            np.cumsum(lvo_mt_hist) / lvo_mt_hist.sum()
        results['nlvo_ivt_cum_probs'] = \
            np.cumsum(nlvo_ivt_hist) / nlvo_ivt_hist.sum()
        
        # Get shift in mRS probs and store
        results['lvo_ivt_shift'] = \
            results['lvo_ivt_probs'] - results['lvo_untreated_probs']
        results['lvo_mt_shift'] = \
            results['lvo_mt_probs'] - results['lvo_untreated_probs']
        results['nlvo_ivt_shift'] = \
            results['nlvo_ivt_probs'] - results['nlvo_untreated_probs']

        # Get average mRS store in results
        results['lvo_untreated_mean_mRS'] = \
            np.mean(lvo_ivt_outcomes['untreated_mrs'])
        results['nlvo_untreated_mean_mRS'] = \
            np.mean(nlvo_ivt_outcomes['untreated_mrs'])
        results['lvo_ivt_mean_mRS'] = \
            np.mean(lvo_ivt_outcomes['treated_mrs'])
        results['lvo_mt_mean_mRS'] = \
            np.mean(lvo_mt_outcomes['treated_mrs'])
        results['nlvo_ivt_mean_mRS'] = \
            np.mean(nlvo_ivt_outcomes['treated_mrs'])

        # Get average shifts and store in results
        results['lvo_ivt_mean_shift'] = lvo_ivt_outcomes['shift'].mean()
        results['lvo_mt_mean_shift'] = lvo_mt_outcomes['shift'].mean()
        results['nlvo_ivt_mean_shift'] = nlvo_ivt_outcomes['shift'].mean()

        # Get average improved mRS proportion
        results['lvo_ivt_improved'] = np.mean(lvo_ivt_outcomes['shift'] < 0)
        results['lvo_mt_improved'] = np.mean(lvo_mt_outcomes['shift'] < 0)
        results['nlvo_ivt_improved'] = np.mean(nlvo_ivt_outcomes['shift'] < 0)

        return results

    def calculate_outcomes_for_lvo_ivt(self, time_to_ivt, x):
        """
        Models populations of patients for:
        1) Untreated LVO
        2) LVO treated with IVT at given time
        3) Shift in mRS between untreated and treated

        Inputs:
        Time to IVT

        Outputs:
        A dictionary of patient population mRS as described above.
        """

        # Get relevant distributions
        untreated_probs = self.mrs_distribution_probs['no_treatment_lvo']
        no_effect_logodds = self.mrs_distribution_logodds[
            'no_effect_lvo_ivt_deaths']
        t0_logodds = self.mrs_distribution_logodds['t0_treatment_lvo_ivt']
        # Calculate fraction of time to no effect passed
        frac_to_no_effect = time_to_ivt / self.ivt_time_no_effect
        # Combine t=0 and nop effect distributions based on time past
        treated_logodds = ((frac_to_no_effect * no_effect_logodds) +
                           ((1 - frac_to_no_effect) * t0_logodds))
        # Convert to odds and probabilties
        treated_odds = np.exp(treated_logodds)
        treated_probs = treated_odds / (1 + treated_odds)
        # Get mRS distributions for 50 patients
        untreated_mrs = np.digitize(x, untreated_probs)
        treated_mrs = np.digitize(x, treated_probs)
        # Calculate shift in mRS
        shift = treated_mrs - untreated_mrs
        # Put results in dictionary
        results = dict()
        results['untreated_mrs'] = untreated_mrs
        results['treated_mrs'] = treated_mrs
        results['shift'] = shift

        return results

    def calculate_outcomes_for_lvo_mt(self, time_to_mt, x):
        """
        Models populations of patients for:
        1) Untreated LVO
        2) LVO treated with MT at given time
        3) Shift in mRS between untreated and treated

        Inputs:
        Time to MT

        Outputs:
        A dictionary of patient population mRS as described above.
        """

        # Get relevant distributions
        untreated_probs = self.mrs_distribution_probs['no_treatment_lvo']
        no_effect_logodds = self.mrs_distribution_logodds[
            'no_effect_lvo_mt_deaths']
        t0_logodds = self.mrs_distribution_logodds['t0_treatment_lvo_mt']
        # Calculate fraction of time to no effect passed
        frac_to_no_effect = time_to_mt / self.mt_time_no_effect
        # Combine t=0 and nop effect distributions based on time past
        treated_logodds = ((frac_to_no_effect * no_effect_logodds) +
                           ((1 - frac_to_no_effect) * t0_logodds))
        # Convert to odds and probabilties
        treated_odds = np.exp(treated_logodds)
        treated_probs = treated_odds / (1 + treated_odds)
        # Get mRS distributions for 50 patients
        untreated_mrs = np.digitize(x, untreated_probs)
        treated_mrs = np.digitize(x, treated_probs)
        # Calculate shift in mRS
        shift = treated_mrs - untreated_mrs
        # Put results in dictionary
        results = dict()
        results['untreated_mrs'] = untreated_mrs
        results['treated_mrs'] = treated_mrs
        results['shift'] = shift

        return results

    def calculate_outcomes_for_nlvo_ivt(self, time_to_ivt, x):
        """
        Models populations of patients for:
        1) Untreated nLVO
        2) LVO treated with IVT at given time
        3) Shift in mRS between untreated and treated

        Inputs:
        Time to IVT

        Outputs:
        A dictionary of patient population mRS as described above.
        """

        # Get relevant distributions
        untreated_probs = self.mrs_distribution_probs['no_treatment_nlvo']
        no_effect_logodds = self.mrs_distribution_logodds[
            'no_effect_nlvo_ivt_deaths']
        t0_logodds = self.mrs_distribution_logodds['t0_treatment_nlvo_ivt']
        # Calculate fraction of time to no effect passed
        frac_to_no_effect = time_to_ivt / self.ivt_time_no_effect
        # Combine t=0 and nop effect distributions based on time past
        treated_logodds = ((frac_to_no_effect * no_effect_logodds) +
                           ((1 - frac_to_no_effect) * t0_logodds))
        # Convert to odds and probabilties
        treated_odds = np.exp(treated_logodds)
        treated_probs = treated_odds / (1 + treated_odds)
        # Get mRS distributions for 50 patients
        untreated_mrs = np.digitize(x, untreated_probs)
        treated_mrs = np.digitize(x, treated_probs)
        # Calculate shift in mRS
        shift = treated_mrs - untreated_mrs
        # Put results in dictionary
        results = dict()
        results['untreated_mrs'] = untreated_mrs
        results['treated_mrs'] = treated_mrs
        results['shift'] = shift

        return results
