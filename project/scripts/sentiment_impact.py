import numpy as np

def overall_sentiment(data):
    """
    Returns a number from -1.0 to 1.0 representing the overall sentiment.
    It is computed as the mean over the non-outliers.
    If there is very little data, then
    """
    outliers_removed = data[is_outlier(data, thresh=2)]
    if len(outliers_removed) == 0:
        return np.mean(data)
    else:
        return np.mean(outliers_removed)

def is_outlier(data, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        data : A numobservations array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """

    diff = np.abs(data - np.median(data))
    m_dev = np.median(diff)
    modified_z_score = 0.6745 * diff / m_dev if m_dev else 0.
    return modified_z_score > thresh


def measure_impact(timeframe):
    """
    Assuming a symmetric timeframe centered on the conflict date,
    it returns the impact of the conflict in daily average sentiment by
    comparing the changes in sentiment that take place before and
    after a conflict date.

    It uses an auxiliary function to measure the change in
    sentiment before and after the conflict date. Both measures
    take a value in the interval [0.0, 1.0]. Then, the absolute value
    of the difference is returned.

    It does not penalize how long it takes for the average sentiment
    to change (accounting for the fact that the public might take longer
    to learn about and react to certain conflicts, e.g. due to changes
    in timezone.
    """
    def measure_changes(slist, maximum=1.0, minimum=-1.0):
        # Return main change plus if there where posterior changes
        main_change = abs(max(slist) - min(slist))
        # Obtain maximum possible value to normalize (range [0, 1.0])
        maximum_value = maximum - minimum
        return main_change / maximum_value

    # Divide timeframe in two (before and after conflict)
    n_b = int(len(timeframe)/2)
    tf_b = timeframe[:n_b]
    tf_a = timeframe[n_b:]
    if len(timeframe) % 2 == 0:
        # If we have an even number of elements in the timeframe
        # we include the previous day as well
        np.insert(tf_a, 0, tf_b[-1])
    # Measure changes after conflict, compared to right before conflict
    before_impact = measure_changes(tf_b)
    after_impact = measure_changes(tf_a)
    return abs(after_impact - before_impact)
