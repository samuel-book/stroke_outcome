"""
Class to hold clinical outcome model.
Predicts probability of good outcome of patient(s) or group(s) of patients.

Call `calculate_outcome_for_all(args)` from outside of the object

Inputs
======

All inputs take np arrays (for multiple groups of patients).

mimic: proportion of patients with stroke mimic

ich: proportion of patients with intracerebral haemorrhage (ICH). 
Or probability of a patient having an ICH, when using for a single patient.

nlvo: proportion of patients with non-large vessel occlusions (nLVO). 
Or probability of a patient having an NLVO, when using for a single patient.

lvo: proportion of patients with large vessel occlusions (LVO). 
Or probability of a patient having a LVO, when using for a single patient.

onset_to_needle: minutes from onset to thrombolysis

onset_to_ouncture: minutes from onset to thrombectomy

nlvo_eligible_for_treatment: proportion of patients with NLVO suitable for 
treatment with thrombolysis. Or probability of a patient with NVLO being 
eligible for treatment.

lvo_eligible_for_treatment: proportion of patients with LVO suitable for 
treatment with thrombolysis and/or thrombectomy. Or probability of a patient 
with LVO being eligible for treatment.

Returns
=======

Probability of good outcome: The probability of having a good outcome (modified
Rankin Scale 0-1) for the patient or group of patients (np array).


References for decay of effect of thrombolysis and thrombectomy
===============================================================

Decay of effect of thrombolysis without image selection of patients taken from:
Emberson, Jonathan, Kennedy R. Lees, Patrick Lyden, Lisa Blackwell, 
Gregory Albers, Erich Bluhmki, Thomas Brott, et al (2014). “Effect of Treatment 
Delay, Age, and Stroke Severity on the Effects of Intravenous Thrombolysis with
Alteplase for Acute Ischaemic Stroke: A Meta-Analysis of Individual Patient
Data from Randomised Trials.” The Lancet 384: 1929–1935.
https://doi.org/10.1016/S0140-6736(14)60584-5.

* Time to no effect = 6.3hrs

Decay of effect of thrombectomy without image selection of patients taken from:
Fransen, Puck S. S., Olvert A. Berkhemer, Hester F. Lingsma, Debbie Beumer, 
Lucie A. van den Berg, Albert J. Yoo, Wouter J. Schonewille, et al. (2016)
“Time to Reperfusion and Treatment Effect for Acute Ischemic Stroke: A 
Randomized Clinical Trial.” JAMA Neurology 73: 190–96. 
https://doi.org/10.1001/jamaneurol.2015.3886.

* Time to no effect = 8hrs
"""

import numpy as np
import pandas as pd


class Clinical_outcome:
    def __init__(self):
        """Constructor for clinical outcome model
        """
        self.name = "Clinical outcome model"
        self.thrombectomy_time_no_effect = 8 * 60
        self.thrombolysis_time_no_effect = 6.3 * 60
        self.maximum_permitted_time_to_thrombectomy = 360
        self.maximum_permitted_time_to_thrombolysis = 270

    def calculate_outcome_for_all(self,
                                  mimic,
                                  ich,
                                  nlvo,
                                  lvo,
                                  onset_to_needle,
                                  onset_to_puncture,
                                  nlvo_eligible_for_treatment,
                                  lvo_eligible_for_treatment,
                                  prop_thrombolysed_lvo_receiving_thrombectomy):
        """
        Calculates the probability of good outcome for all patients admitted
        with acute stroke. 

        Based on:
        Holodinsky JK, Williamson TS, Demchuk AM, et al. Modeling Stroke Patient
        Transport for All Patients With Suspected Large-Vessel Occlusion. JAMA 
        Neurol. 2018;75(12):1477-1486. doi:10.1001/jamaneurol.2018.2424
        
        Sums outcomes for:

        1) mimics
        2) ICH
        3) non-LVO
        4) LVO treated with thrombolysis
        5) LVO treated with thrombectomy (if thrombolysis not successful in a
            drip and ship configuration)

        arguments
        ---------

        np arrays (each row is a given geographic area with different 
        characteristics)

        mimic: proportion of patients with stroke mimic
        ich: proportion of patients with ICH
        nlvo: proportion of patients with non-lvo
        lvo: proportion of patients with lvo
        onset_to_needle: minutes from onset to thrombolysis
        onset_to_ounctureL minutes from onset to thrombectomy
        nlvo_eligible_for_treatment: proportion of nlvo suitable for treatment
        lvo_eligible_for_treatment: proportion of lvo suitable for treatment

        returns
        -------

        probability of good outcome for all (np array)
        """
        
        # Get outcomes
        # ------------
        
        outcomes = pd.DataFrame()

        # Calculate good outcomes for mimics
        outcomes['mimic'] = self._calculate_outcome_for_stroke_mimics(
            mimic.shape)

        # Calculate good outcomes for ich   
        outcomes['ich']  = self._calculate_outcome_for_ICH(mimic.shape)

        # Calculate good outcomes for nlvo without treatment
        outcomes['nlvo_base'] = \
            np.full(nlvo.shape, 0.4622)
            
        # Calculate good outcomes for nlvo with thrombolysis
        outcomes['nlvo_add_ivt'] = \
            self._calculate_thrombolysis_outcome_for_nlvo(onset_to_needle)

        # Calculate good outcomes for lvo without treatment
        outcomes['lvo_base'] = \
            np.full(nlvo.shape, 0.1328)
        
        # Calculate good outcomes for lvo with thrombolysis
        outcomes['lvo_add_ivt'] = \
            self._calculate_thrombolysis_outcome_for_lvo(onset_to_needle)

        # Calculate good outcomes for lvo with thrombolysis
        outcomes['lvo_add_et'] = \
            self._calculate_thrombectomy_outcome_for_lvo(onset_to_puncture)

        
        # Weight outcome results by proportion of patients
        # ------------------------------------------------
        
        # 'Results' are good outcomes
        results = pd.DataFrame()
        
        # Results for mimic
        results['mimic'] = outcomes['mimic']  * mimic
        
        # Results for ich
        results['ich'] = outcomes['ich']  * ich
        
        # Results for nlvo
        results['nlvo_base'] = nlvo * outcomes['nlvo_base']
        
        results['nlvo_ivt'] = \
            nlvo * outcomes['nlvo_add_ivt'] * nlvo_eligible_for_treatment
        
        # Results for lvo
        results['lvo_base'] = lvo * outcomes['lvo_base']
        
        results['lvo_ivt'] = \
            lvo * outcomes['lvo_add_ivt'] * lvo_eligible_for_treatment
                
        # Adjust thrombectomy/thrombolysis ratio for LVO   
        # Reduce thrombectomy treatment by LVO responding to IVT
        lvo_receiving_et = ((lvo * lvo_eligible_for_treatment * 
            prop_thrombolysed_lvo_receiving_thrombectomy) - 
            results['lvo_ivt'])

        results['lvo_et'] = lvo_receiving_et * outcomes['lvo_add_et']

        p_good = results.sum(axis=1).values

        return p_good

    @staticmethod
    def _calculate_outcome_for_ICH(array_shape):
        """
        Calculates the probability of good outcome for patients with intra-
        cranial haemorrhage (ICH).

        Sets all values to 0.24 

        Based on Holodinsky et al. (2018) Drip-and-Ship vs. Mothership: 
        Modelling Stroke Patient Transport for All Suspected Large Vessel
        Occlusion Patients. JAMA Neuro (in press)

        arguments
        ---------

        array size

        returns
        -------

        probability of good outcome for ICH (np array)
        """

        # Create an array of required length and set all values to 0.24
        p_good = np.zeros(array_shape)
        p_good[:] = 0.24

        return p_good        

    @staticmethod
    def _calculate_outcome_for_stroke_mimics(array_shape):
        """
        Calculates the probability of good outcome for patients with stroke
        mimic

        Sets all values to 1

        Based on Holodinsky et al. (2018) Drip-and-Ship vs. Mothership: 
        Modelling Stroke Patient Transport for All Suspected Large Vessel
        Occlusion Patients. JAMA Neuro (in press)

        arguments
        ---------

        array size

        returns
        -------

        probability of good outcome for stroke mimiccs (np array)
        """

        # Create an array of required length and set all values to 0.9
        p_good = np.zeros(array_shape)
        p_good[:] = 1

        return p_good
    
    def _calculate_thrombectomy_outcome_for_lvo(self, onset_to_puncture):
        """
        Calculates the probability of additional good outcome for LVO patients
        receiving thrombectomy.

        arguments
        ---------

        onset_to_puncture : np array in minutes

        returns
        -------

        probability of additional good outcome if given thrombectomy (np array)
        """

        p_good_max = 0.5208
        p_good_min = 0.1328
        
        # Convert probability to odds
        odds_good_max = p_good_max / (1 - p_good_max)
        odds_good_min = p_good_min / (1 - p_good_min)
        
        # Calculate fraction of effective time used
        fraction_max_effect_time_used = \
            onset_to_puncture / self.thrombectomy_time_no_effect
        
        # Calculate odds of good outcome with treatment
        odds_good = np.exp(np.log(odds_good_max) - 
            ((np.log(odds_good_max) - np.log(odds_good_min)) 
            * fraction_max_effect_time_used))
        
        # Convert odds to probability
        prob_good = odds_good / (1 + odds_good)
        prob_good[prob_good < p_good_min] = p_good_min
        
        # Calculate probability of additional good outcome
        p_good_add = prob_good - p_good_min
        
        # Set additional good outcomes to zero if past permitted treatment time
        mask = onset_to_puncture > self.maximum_permitted_time_to_thrombectomy
        p_good_add[mask] = 0   
        
        # Ensure no negative outcomes
        mask = p_good_add < 0
        p_good_add[mask] = 0  

        return p_good_add        

    def _calculate_thrombolysis_outcome_for_lvo(self, onset_to_needle):
        """
        Calculates the probability of additional good outcome for LVO patients
        receiving thrombolysis. Does not include baseline untreated good
        comes.

        arguments
        ---------
        
        onset_to_needle : np array in minutes


        returns
        -------

        probability of additional good outcome if given thrombolysis 
        (np array)
        """
        
        p_good_max = 0.2441
        p_good_min = 0.1328
        
        # Convert probability to odds
        odds_good_max = p_good_max / (1 - p_good_max)
        odds_good_min = p_good_min / (1 - p_good_min)
        
        # Calculate fraction of effective time used        
        fraction_max_effect_time_used = \
            onset_to_needle / self.thrombolysis_time_no_effect

        # Calculate odds of good outcome with treatment
        odds_good = np.exp(np.log(odds_good_max) - 
            ((np.log(odds_good_max) - np.log(odds_good_min)) 
            * fraction_max_effect_time_used))

        # Convert odds to probability
        prob_good = odds_good / (1 + odds_good)
        prob_good[prob_good < p_good_min] = p_good_min
        
        # Calculate probability of additional good outcome
        p_good_add = prob_good - p_good_min
        
        # Set additional good outcomes to zero if past permitted treatment time
        mask = onset_to_needle> self.maximum_permitted_time_to_thrombolysis
        p_good_add[mask] = 0   
        
        # Ensure no negative outcomes
        mask = p_good_add < 0
        p_good_add[mask] = 0  

        # return outcome and proportion of treated who respond
        return p_good_add

    def _calculate_thrombolysis_outcome_for_nlvo(self, onset_to_needle):
        """
        Calculates the probability of good outcome for non-LVO patients
        receiving thrombolysis.

        arguments
        ---------

        onset_to_needle : np array in minutes

        returns
        -------

        probability of good outcome if given thrombolysis (np array)
        """

        p_good_max = 0.6444
        p_good_min = 0.4622
        
        # Convert probability to odds
        odds_good_max = p_good_max / (1 - p_good_max)
        odds_good_min = p_good_min / (1 - p_good_min)
        
        # Calculate fraction of effective time used 
        fraction_max_effect_time_used = (onset_to_needle / 
                                         self.thrombolysis_time_no_effect)
        
        # Calculate odds of good outcome with treatment
        odds_good = np.exp(np.log(odds_good_max) - 
            ((np.log(odds_good_max) - np.log(odds_good_min)) 
            * fraction_max_effect_time_used))
        
        # Convert odds to probability
        prob_good = odds_good / (1 + odds_good)
        prob_good[prob_good < p_good_min] = p_good_min
        
        # Calculate probability of additional good outcome
        p_good_add = prob_good - p_good_min
        
        mask = onset_to_needle> self.maximum_permitted_time_to_thrombolysis
        p_good_add[mask] = 0   
        
        # Ensure no negative outcomes
        mask = p_good_add < 0
        p_good_add[mask] = 0  

        # return outcome and proportion of treated who respond
        return p_good_add
