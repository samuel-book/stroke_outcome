import numpy as np

def fudge_sum_one(dist, dp=3):
    """
    Force sum of a distribution to be exactly 1.

    Add up all of the numbers to the given precision. The sum should
    be less than 1 exactly, but this function also works with the sum
    is greater than 1 exactly. Go through the numbers in turn and
    nudge the smallest fractions down or the largest fractions up as
    required until the sum is 1 exactly.
    
    Convert the numbers to large integers with a target value
    much larger than 1 because integers are easier to deal with.
    
    Inputs:
    -------
    dist - np.array. mRS distribution (non-cumulative).
    dp   - int. Number of decimal places that the final dist
           will be rounded to.

    Returns:
    -------
    dist_fudged - np.array. The distribution, rounded to the given
                  precision so that it sums to 1.
    """
    if np.round(np.sum(np.round(dist, dp)), dp) == 1.0:
        # Nothing to see here.
        return np.round(dist, dp)

    # Add or subtract from the mRS proportions until the sum is 1.
    # Start by adding to numbers with large fractional parts
    # or subtracting from numbers with small fractional parts.

    # Store the integer part of each value,
    # the fractional part of each value,
    # and values to track how many times the integer part
    # has been fudged upwards and downwards.
    
    # Split the values into the rounded and non-rounded parts:
    success = False
    while success == False:
        # Convert to integers.
        dist = dist * 10**dp
        dist_int = dist.astype(int)
        dist_frac = dist % dist.astype(int)
        target = 10 ** dp
        if np.all(dist_frac == 0.0):
            # If the dist is already rounded to the requested dp,
            # try the next digit up.
            dist = dist / 10**dp
            dp -= 1
        else:
            # Use this precision.
            success = True

    # Make a grid with four columns.
    arr = np.zeros((len(dist), 4), dtype=int)
    arr[:, 0] = dist_int
    arr[:, 1] = (dist_frac * 1000).astype(int)

    # Cut off this process after 20 loops.
    loops = 0
    sum_dist = np.sum(arr[:, 0])

    while loops < 20:
        if sum_dist < target:
            # Pick out the values that have been added to
            # the fewest times.
            min_change = np.min(arr[:, 2])
            inds_min_change = np.where(arr[:, 2] == min_change)
            # Of these, pick out the value with the largest
            # fractional part.
            largest_frac = np.max(arr[inds_min_change, 1])
            ind_largest_frac = np.where(
                (arr[:, 2] == min_change) &
                (arr[:, 1] == largest_frac)
            )
            if len(ind_largest_frac[0]) > 1:
                # Arbitrarily pick the lowest mRS if multiple options.
                ind_largest_frac = ind_largest_frac[0][0]
            # Add one to the final digit of this mRS proportion
            # and record the change in column 2.
            arr[ind_largest_frac, 0] += 1
            arr[ind_largest_frac, 2] += 1
        elif sum_dist > target:
            # Pick out the values that have been subtracted from
            # the fewest times.
            min_change = np.min(arr[:, 3])
            inds_min_change = np.where(arr[:, 3] == min_change)
            # Of these, pick out the value with the smallest
            # fractional part.
            smallest_frac = np.min(arr[inds_min_change, 1])
            ind_smallest_frac = np.where(
                (arr[:, 3] == min_change) &
                (arr[:, 1] == smallest_frac)
            )
            if len(ind_smallest_frac[0]) > 1:
                # Arbitrarily pick the lowest mRS if multiple options.
                ind_smallest_frac = ind_smallest_frac[0][0]
            # Subtract one from the final digit of this mRS proportion
            # and record the change in column 3.
            arr[ind_smallest_frac, 0] -= 1
            arr[ind_smallest_frac, 3] += 1

        # Have we finished?
        sum_dist = np.sum(arr[:, 0])
        if sum_dist == target:
            # Finish.
            loops = 20
        else:
            # Keep going round the "while" loop.
            loops += 1

    # Take the new fudged distribution.
    # Divide so that it now sums to 1 instead of the large target.
    dist_fudged = arr[:, 0] / 10**dp

    return dist_fudged