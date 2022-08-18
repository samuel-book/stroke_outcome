import numpy as np
import pandas as pd

class Clinical_outcome:
    def __init__(self, mrs_dists):
        """Constructor for clinical outcome model
        """
        self.name = "Clinical outcome model"

        # Set replicates of mRS distribution to perform
        self.mrs_replicates = 1000

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

    def calculate_outcomes(self, time_to_ivt, time_to_mt):

        # Set up results dictionary
        results = dict()

        # Get treatment results
        lvo_ivt_outcomes = self.calculate_outcomes_for_lvo_ivt(time_to_ivt)
        lvo_mt_outcomes = self.calculate_outcomes_for_lvo_mt(time_to_mt)
        nlvo_ivt_outcomes = self.calculate_outcomes_for_nlvo_ivt(time_to_ivt)

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

    def calculate_outcomes_for_lvo_ivt(self, time_to_ivt):
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
        x = np.linspace(0.001, 0.999, self.mrs_replicates)
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

    def calculate_outcomes_for_lvo_mt(self, time_to_mt):
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
        x = np.linspace(0.001, 0.999, self.mrs_replicates)
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

    def calculate_outcomes_for_nlvo_ivt(self, time_to_ivt):
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
        x = np.linspace(0.001, 0.999, self.mrs_replicates)
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
