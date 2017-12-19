import numpy as np

def overall_sentiment(data):
    """
    Returns a number from -1.0 to 1.0 representing the overall sentiment.
    It is computed as the mean over the non-outliers.
    """
    outliers_removed = data[is_outlier(data, thresh=2)]
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

def measure_impact(data):
    """Returns a number from 0 to 2 representing the sentiment impact."""
    return max(data) - min(data)