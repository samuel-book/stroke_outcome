# Predicting granular disability outcomes after treatment of stroke with thrombolysis (IVT) or thrombectomy (MT)

This notebook describes the basic methodology for estimating disability outcomes, depending on time to treatment woth intravenous thrombolysis (IVT) or mechanical thrombectomy (MT).

Detailed methodology and code are found in the notebooks on [derivation of mRS distributions at time of stroke onset and time when effect has decayed away](./mRS_datasets_full.ipynb) and [deacy of effect over time](./mRS_outcomes_maths).

## modified Rankin Scale

Disability levels may be measured in various ways. In this project we are using the modified Rankin Scale (mRS). It is a commonly used scale for measuring the degree of disability or dependence in the daily activities of people who have suffered a stroke.

The scale runs from 0-6, running from perfect health without symptoms to death:

| Score | Description |
|---|---|
| 0 | No symptoms. |
| 1 | No significant disability. Able to carry out all usual activities, despite some symptoms. |
| 2 | Slight disability. Able to look after own affairs without assistance, but unable to carry out all previous activities. |
| 3 | Moderate disability. Requires some help, but able to walk unassisted. |
| 4 | Moderately severe disability. Unable to attend to own bodily needs without assistance, and unable to walk unassisted. |
| 5 | Severe disability. Requires constant nursing care and attention, bedridden, incontinent. |
| 6 | Dead. |

## Descriptions of the mRS data sets derived, and basic methodology

**Pre-stroke mRS distributions**: Pre-stroke mRS distributions give the best possible outcome (i.e. 100% effective treatment). These distributions come from the SAMueL data set, and may be stratified by haemorrgage vs. infarction (ischaemic), and by NIHSS on arrival where, for ischaemic stroke, NIHSS 0-10 is taken as a surrogate for nLVO, and NIHSS 11+ is taken as a surrogate for LVO.

**nLVO baseline (no treatment effect)**: The weighted combination of the untreated control group of combined nLVO/LVO data from Lees et al. 2010 (100%) and the untreated control group of LVO-only data from Goyal et al. 2016. Weightings are chosen to match the P(mRS <= 1) of 46% (from the control group in Emberson with NIHSS of 0-10). This distribution is then corrected for the excess deaths due to treatment with IVT.

**nLVO t=0 treatment with IVT**: The weighted combination of pre-stroke mRS for patients with NIHSS 0-10 (87%) and untreated control group of nLVO (13%) distributions, where weights are chosen to match the P(mRS <= 1, t=0)=0.63. 63% is estimated from Emberson et al. 2014, where 46% of untreated patients with NIHSS 0-10 had mRS 0-1, and the odds ratio of mRS 0-1 extrapolates back to 2.0 at t=0. Pre-stroke mRS is for ischaemic stroke with NIHSS 0-10 (from the SAMueL data set). This distribution is then corrected for the excess deaths due to treatment with IVT,

**LVO baseline (no treatment effect)**: The control population from Goyal et al. 2016. This distribution is then corrected for the deaths due to treatment with IVT,

**LVO t=0 treatment with IVT**: Weighted combination of the no treatment LVO data from Goyal et al. 2016 and the pre-stroke mRS distribution (for ischaemic stroke with NIHSS 11+, from the SAMueL data set). The weights are chosen to match P(mRS <= 1) of 0.20 which is set as a target by extrapolating the control group mRS for patients with NIHSS 11+ from Emberson et al. 2014 back to a predicted odds ratio of mRS 0-1 of 2.0 at t=0. This distribution is then corrected for the excess deaths due to treatment with IVT.

**LVO t=0 treatment with MT**: The weighted combination of pre-stroke (75%) and untreated LVO at no-effect-time (25%). Hui et al. 2020 reported 75% successful recanalisation with thrombectomy. We assume that recanalisation at t=0 restores all pre-stroke function*. Pre-stroke mRS is for ischaemic stroke with NIHSS 11+ (from the SAMueL data set). This distribution is then corrected for the excess deaths due to treatment with MT.

*Extrapolating results of good outcome, when recanalisation has been achieved with thrombectomy, from Fransen et al. 2016 back to t=0, assuming 75% recanalisation, gives the same proportion of patients with mRS <= 2 as the pre-stroke mRS in the SAMueL data (therefore this extrapolation would suggest full recovery of all health with thrombectomy theoretically carried out at t=0).

### Excess deaths due to treatment

#### IVT deaths due to fatal intracranial haemorrhage (Emberson et al., 2014): 

| NIHSS | Treated | Control | Excess |
|-------|---------|---------|--------|
| 0-10  | 1.41%   | 0.32%   | 1.10%  |
| 11+   | 3.85%   | 0.45%   | 3.41%  |
| All   | 2.68%   | 0.39%   | 2.29%  |

Excess deaths due to IVT are assumed to occur independently of time. Differing risks of death are applied according to whether the patient in assumed nLVO (NIHSS 0-10 as a surrogate for nLVO) or LVO (NIHSS 11+, as a surrogate for LVO).

#### MT deaths (Goyal et al., 2016):

| Treated | Control | Excess |
|---------|---------|--------|
| 18.9%   | 15.3%   | 3.6%   |

The control group in Goyal et al. do not receive MT, but do receive other interventions such as IVT (used in 83% of patients). No additional IVT-related deaths need to be considered when modelling use of MT as the control group (used to estimate the effect of MT at a time MT is no longer effective) already includes IVT-related excess deaths. 

#### Derived distributions

Distributions for the effect of IVT and MT as described above, given either at time of stroke onset or time when the effect of treatment has decayed to zero, are shown in {numref}`figure {number} <nLVO_IVT_dist>` to {numref}`figure {number} <LVO_MT_dist>`. 

:::{figure-md} nLVO_IVT_dist
<img src="./images/nLVO-IVT.jpg" width="600">

Expected mRS distribution for nLVO strokes if IVT given at time of stroke onset (*t=0hr*), or if IVT given at time when there effect has decayed to zero (*No effect time*, at this point there are still IVT-related excess deaths due to fatal intracranial haemorrhage).
:::

:::{figure-md} LVO_IVT_dist
<img src="./images/LVO-IVT.jpg" width="600">

Expected mRS distribution for LVO strokes if IVT given at time of stroke onset (*t=0hr*), or if IVT given at time when there effect has decayed to zero (*No effect time*, at this point there are still IVT-related excess deaths due to fatal intracranial haemorrhage).
:::

:::{figure-md} LVO_MT_dist
<img src="./images/LVO-MT.jpg" width="600">

Expected mRS distribution for LVO strokes if MT given at time of stroke onset (*t=0hr*), or if MT given at time when there effect has decayed to zero (*No effect time*, at this point there are still MT-related excess deaths).
:::

## Relationship between time to treatment and effect

Modelling of the effect of IVT or MT after any given treatment time assumes that the log odds decay uniformly over time between stroke onset and the time to no effect (as modelled by Emberson et al. for IVT, and Fransen et al. for MT). The time to no-effect treatment is take as 6.3 hours for IVT (Emberson et al.) and 8 hours for MT (Fransen et al). Note: the time to no effect from Fransen et al. did not incldue those patients who may be selected for late treatment based on advanced imaging. In this method we do not include late-presenting patients in our outcome modelling.

The modelled decay of effects of IVT and MT are shown in {numref}`figure {number} <nLVO_IVT_time>` to {numref}`figure {number} <LVO_MT_time>`. 


:::{figure-md} nLVO_IVT_time
<img src="./images/prob_with_time_nlvo_ivt.jpg" width="600">

Expected mRS distribution for nLVO strokes depending on time to treatment with IVT.
:::

:::{figure-md} LVO_IVT_time
<img src="./images/prob_with_time_lvo_ivt.jpg" width="600">

Expected mRS distribution for LVO strokes depending on time to treatment with IVT.
:::

:::{figure-md} LVO_MT_time
<img src="./images/prob_with_time_lvo_mt.jpg" width="600">

Expected mRS distribution for nLVO strokes depending on time to treatment with MT.
:::

### Proportion of ischaemic patients with LVO


The proportion of ischaemic patients with LVO may be estimated in various ways. Estimates are likely to be swayed by the population being studied (e.g. treatment trial results may under-estimate nLVO as very low severity patients may not be selected for the trial). Below are various estimated of the  relative occurrence of LVO and nLVO.

#### Analysis of SAMueL data

Data from SAMueL using NIHSS 11+ as a surrogate for LVO:

| Admission type                       | All arrivals | Arrival within 6 hrs known onset | Arrival within 4 hrs known onset |
|--------------------------------------|--------------|----------------------------------|----------------------------------|
| Proportion all admissions            | 1.0          | 42.9                             | 37.1                             |
| Proportion haemorrhagic              | 11.5         | 13.6                             | 14.1                             |
| Proportion ischaemic                 | 88.5         | 86.4                             | 85.9                             |
| Proportion ischaemic with NIHSS 0-10 | 74.9         | 67.4                             | 65.7                             |
| Proportion ischaemic with NIHSS 11+  | 25.1         | 32.6                             | 34.3                             |

For original analysis see: https://samuel-book.github.io/samuel-1/descriptive_stats/10_using_nihss_10_for_lvo.html

#### RACECAT pre-hospital diagnosis of LVO

A breakdown on stroke type from , 20the design of the RACE test for pre-hopsital diagnosis of LVO (de la Ossa Herrero et al., 2013). Note - there appears to be some discrepancies between reporting of the results between the text and the detailed breakdown by RACE score in figure 2 of the paper.

* Trial recruited from patients who presented at the emergency department within 6 hours from symptoms onset.

* In the text: Of 357 patients in the analysis, the stroke subtype was ischemic stroke in 240 (67.2%), hemorrhagic stroke in 52 (14.6%), transient ischemic attack in 20 (5.6%), and stroke mimic in 45 (12.6%). LVO was detected in 76 patients (31.7% of ischaemic strokes).

* In figure 2: Of 357 patients in the analysis, the stroke subtype was ischemic stroke in 260 (72.8), hemorrhagic stroke in 52 (14.6%), and stroke mimic in 45 (12.6%). LVO was detected in 99 patients (38.1% of ischaemic strokes). It appears that TIAs may be counted in with ischaemic strokes in this analysis.

#### Estimating the number of UK stroke patients eligible for endovascular thrombectomy (review/analysis)

McMeekin et al. (2017) review the evdidence for estimating the number of UK stroke patients eligible for endovascular thrombectomy. They estimate:

* 40% of ischaemic stroke patients have LVO; 80% of which have NIHSS >=6 and say be suitable for thrombectomy. This is equivalent to 32% of admitted patients having LVO suitable for thrombectomy.

#### Proportion LVO calculated in these notebooks

Two of the methods we use here to produce the mRS distributions estimate the proportion of LVO as part of their calculations. 

nLVO baseline (no treatment effect): 33.0% 
nLVO t=0 treatment with IVT: 38.7% 


## References used in modelling

de la Ossa Herrero N, Carrera D, Gorchs M, Querol M, Millán M, Gomis M, et al. Design and Validation of a Prehospital Stroke Scale to Predict Large Arterial Occlusion The Rapid Arterial Occlusion Evaluation Scale. Stroke; a journal of cerebral circulation. 2013 Nov 26;45. 

Emberson J, Lees KR, Lyden P, et al. _Effect of treatment delay, age, and stroke severity on the effects of intravenous thrombolysis with alteplase for acute ischaemic stroke: A meta-analysis of individual patient data from randomised trials._ The Lancet 2014;384:1929–35. doi:10.1016/S0140-6736(14)60584-5

Fransen, P., Berkhemer, O., Lingsma, H. et al. Time to Reperfusion and Treatment Effect for Acute Ischemic Stroke: A Randomized Clinical Trial. JAMA Neurol. 2016 Feb 1;73(2):190–6. DOI: 10.1001/jamaneurol.2015.3886

Goyal M, Menon BK, van Zwam WH, et al. _Endovascular thrombectomy after large-vessel ischaemic stroke: a meta-analysis of individual patient data from five randomised trials._ The Lancet 2016;387:1723-1731. doi:10.1016/S0140-6736(16)00163-X

Hui W, Wu C, Zhao W, Sun H, Hao J, Liang H, et al. Efficacy and Safety of Recanalization Therapy for Acute Ischemic Stroke With Large Vessel Occlusion. Stroke. 2020 Jul;51(7):2026–35. 

Lees KR, Bluhmki E, von Kummer R, et al. _Time to treatment with intravenous alteplase and outcome in stroke: an updated pooled analysis of ECASS, ATLANTIS, NINDS, and EPITHET trials_. The Lancet 2010;375:1695-703. doi:10.1016/S0140-6736(10)60491-6

McMeekin P, White P, James MA, Price CI, Flynn D, Ford GA. Estimating the number of UK stroke patients eligible for endovascular thrombectomy. European Stroke Journal. 2017;2:319–26. 

SAMueL-1 data on mRS before stroke (DOI: 10.5281/zenodo.6896710): https://samuel-book.github.io/samuel-1/descriptive_stats/08_prestroke_mrs.html


## Notes


