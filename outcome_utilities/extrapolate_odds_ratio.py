import numpy as np

def extrapolate_odds_ratio(t_1,OR_1,t_2,OR_2,p_2,t_e=0):
    """
    Use two odds ratios to extrapolate the straight line fit and find
    the odds ratio at a given time, then convert to probability.

    The three time parameters MUST use the same units, e.g. hours.

    Inputs:
    t_1, t_2   - float. Times for data points 1 and 2.
    OR_1, OR_2 - float. Odds ratios at times t_1 and t_2.
    p_2        - float. Probability at time t_2.
    t_e        - float. Time to extrapolate the line to.

    Returns:
    OR_e - float. Extrapolated odds ratio at time t_e.
    p_e  - float. Extrapolated probability at time t_e.
    a, b - float. Constants for the straight line fit a+bt.
    """
    # Calculate "a", the log(odds ratio) at time t=0:
    a = ((np.log(OR_1) - (t_1/t_2)*np.log(OR_2)) /
         (1.0 - (t_1/t_2)) )

    # Calculate "b", the gradient of the log(odds ratio) straight line.
    b = (np.log(OR_2)-np.log(OR_1)) / (t_2 - t_1)

    # Use these to calculate the odds ratio at time t_e:
    OR_e = np.exp( a + b*t_e )

    # Rearrange odds ratio formula:
    # ORe = {pe/(1-pe)} / {p2/(1-p2)}
    # pe/(1-pe) = ORe * p2/(1-p2)
    # Calculate R, the right-hand-side of this equation:
    R = OR_e * p_2 / (1 - p_2)

    # Rearrange pe/(1-pe)=R to find pe, probability at time t=t_e:
    p_e = R / (1 + R)

    return OR_e, p_e, a, b
