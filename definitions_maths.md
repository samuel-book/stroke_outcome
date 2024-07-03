# Definitions for maths

All of the quantities we will define are only valid in the time range covered by our data, which is $0\leq t \leq t_{\mathrm{ne}}$ for the no-effect time $t_{\mathrm{ne}}$.

## Probability

Firstly we will define some probability distributions in terms of $x$, which is a given modified Rankin Scale (mRS), and $t$, the time from onset to treatment.

+ $P(\mathrm{mRS}=x\ |\ t)$, the probability distribution of mRS.
+ $P(\mathrm{mRS}\leq x\ |\ t)$, the cumulative probability.

In all cases, we know that:
+ The probabilities of a condition being met and it not being met sum to 1: $ P(\mathrm{mRS}>x\ |\ t) = 1 - P(\mathrm{mRS}\leq x\ |\ t) $
+ The probability of mRS$\leq6$ is always equal to 1: $P(\mathrm{mRS}\leq6\ |\ t)=1$ at all $t$. 

## Odds

The odds are an alternative way of expressing the likeliness of an event occurring. Odds are expressed in terms of how much more (or less) likely it is that a given outcome will be attained rather than any other outcomes.

+ $\mathrm{odds} =  \frac{\mathrm{probability\ of\ this\ outcome}}{\mathrm{probability\ of\ other\ outcomes}} \phantom{g} \mathrm{(single\ patient)}  \phantom{gap} =  \frac{\mathrm{number\ of\ this\ outcome}}{\mathrm{number\ of\ other\ outcomes}} \phantom{g} \mathrm{(group\ of\ patients)}$

+ $O(\mathrm{mRS}\leq x\ |\ t) = \frac{P(\mathrm{mRS}\leq x\ |\ t)}{P(\mathrm{mRS}>x\ |\ t)}$

Special cases:
+ When only half of the outcomes are good, i.e. probability=0.5, then odds=1 and log(odds)=0. 
+ Odds and log(odds) for $\mathrm{mRS}\leq6$ are not defined for any $t$. This is because $P(\mathrm{mRS}\leq6)=1.0$ at all times, and so:
$$O(\mathrm{mRS}\leq6) = \frac{P(\mathrm{mRS}\leq6)}{1-P(\mathrm{mRS}\leq6)} = \frac{1}{0}$$

Here we will calculate odds directly from probabilities, and so the odds will be given as non-integer positive numbers rather than fractions. 

We will also consider the natural log of odds, i.e. $\log_{e}(\mathrm{odds})$. __Whenever this notebook says "log", it means natural log (base $e$).__