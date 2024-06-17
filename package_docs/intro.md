# Stroke outcome

The stroke outcome model is used in lots of our projects relating to stroke. To make it easier to share the model across so many places, the python code has been placed in a code package.

These chapters provide some basic working examples for the `stroke-outcome` package.

+ __Source code:__ https://github.com/stroke-modelling/stroke-outcome/
+ __PyPI package:__ https://pypi.org/project/stroke-outcome/


## 📦 Package details:
The package includes the following data:
+ mRS cumulative probability distributions as derived in [the online book][jupyterbooks-link].
+ A selection of utility scores for each mRS level.

Optionally, other data can be used instead of these provided files. The required formats are described in the continuous outcome demo.

The package includes the following processes:
+ __Continuous outcomes:__ Each "patient" uses the average mRS across a population mRS probability distribution. The average mRS score may be any number between 0 and 6, for example 1.2.
+ __Discrete outcomes:__ Each patient is given a single mRS score out of the population mRS probability distribution. The score must be a whole number from 0 to 6.

The following images summarise the differences between the methods:

![Summary of continuous method. There is an mRS distribution when treated and an mRS distribution when not treated. The patient's mRS is the mean across the distribution.](https://raw.githubusercontent.com/stroke-modelling/stroke-outcome/main/docs/images/continuous_example.png) ![Summary of discrete method. There is an mRS distribution when treated and an mRS distribution when not treated. The patient's mRS is selected from whichever part of the distribution contains a fixed cumulative probability score.](https://raw.githubusercontent.com/stroke-modelling/stroke-outcome/main/docs/images/discrete_example.png)
