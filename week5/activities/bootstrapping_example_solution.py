#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import random

def bootstrap(data, num_samples):

    ''' Bootstraps data to determine errors. Resamples the data num_samples
    times. Returns errors of a bootstrap simulation at the 100.*(1 - alpha)
    confidence interval.

    Parameters
    ----------
    data : array-like
        Array of data in the form of an numpy.ndarray
    num_samples : int
        Number of times to resample the data.

    Returns
    -------
    conf_int : tuple, float
        Lower error and upper error at 100*(1-alpha) confidence of the data.
    samples : array-like
        Array of each resampled data. Will have one extra dimension than the
        data of length num_samples, representing each simulation.

    Notes
    -----
    -> arrays can be initialized with numpy.empty
    -> random samples can be retrieved from an array with random.sample

    Examples
    --------
    >>> import scipy
    >>> import numpy as np
    >>> data = scipy.random.f(1, 2, 100)
    >>> data.shape
    (100,)
    >>> samples = bootstrap(data, 50)
    >>> samples.shape
    (50, 100,)
    '''

    samples = np.empty((num_samples, data.size))

    for i in range(num_samples):
        samples[i,:] = random.sample(data, data.size)

    return samples

def calc_bootstrap_error(samples, alpha):

    ''' Returns errors of a bootstrap simulation at the 100.*(1 - alpha)
    confidence interval. Errors are computed by deriving a cumulative
    distribution function of the means of the sampled data and determining the
    distance between the mean and the value including alpha/2 % of the data,
    and the value including alpha/2 % of the data.

    Parameters
    ----------
    samples : array-like
        Array of each resampled data.

    Returns
    -------
    conf_int : tuple, float
        Mean of the data, the lower error and the upper error at 100*(1-alpha)
        confidence of the data.

    Notes
    -----
    -> To find the index in an array closest to a given value, use the
    numpy.argmin function to find the index of the minimum value in an array.
    For example to find the value closest to 11.1 in an array of 10, 11, and 12:
        >>> import numpy as np
        >>> a = np.array([10, 11, 12])
        >>> print(np.argmin(np.abs(a - 11.1)))
        1

    Examples
    --------
    >>> import scipy
    >>> import numpy as np
    >>> data = scipy.random.f(1, 2, 100)
    >>> samples = bootstrap(data, 50)
    >>> errors = calc_bootstrap_error(samples, 0.05)

    '''

    means, cdf = calc_cdf(samples)
    mean = means[np.argmin(np.abs(cdf - 0.5))]
    error_low = means[np.argmin(np.abs(cdf - alpha/2.))]
    error_high = means[np.argmin(np.abs(cdf - (1 - alpha/2.)))]

    return (mean, mean - error_low, error_high - mean)

def calc_cdf(samples):

    ''' Calculates a cumulative distribution function of the means of each
    instance of resampled data.

    Parameters
    ----------
    samples : array-like
        Array of each resampled data.

    Returns
    -------
    means : array-like
        Array containing mean values for the cdf.
    cdf : array-like
        Array containing fraction of data below value x.

    Notes
    -----
    -> numpy.sort can be used to sort the means.
    -> numpy.cumsum can be used to calculate a cumulative sum, which should be
        normalized

    '''

    means = np.sort(np.mean(samples, axis=0))
    cdf = np.cumsum(means) / np.sum(means)

    return means, cdf

def plot_cdf(x, cdf, conf_int=None):

    ''' Plots the cumulative distribution function of the means of each
    instance of the resampled data. If errors are supplied, then vertical lines
    will be plotted at each error.

    Parameters
    ----------
    x : array-like
        Array containing mean values for the cdf.
    cdf : array-like
        Array containing fraction of data below value x.
    conf_int : tuple, float, optional
        Mean of the data, the lower error and the upper error at 100*(1-alpha)
        confidence of the data.

    Returns
    -------
    None

    Notes
    -----


    '''

    # Set up figure
    ax = plt.figure().add_subplot(111)
    ax.set_xlabel('Mean')
    ax.set_ylabel('CDF')

    # Plot CDF of bootstrap means
    ax.plot(x, cdf)

    # check for vertical error lines
    if conf_int is not None:
        ax.axvline(x=conf_int[0] - conf_int[1], ls=':', alpha=0.7, color='b')
        ax.axvline(x=conf_int[0] + conf_int[2], ls='-', alpha=0.7, color='b')

    ax.figure.show()

def load_data(file_name):

    ''' Loads the example distribution in numpy binary format (extension .npy).
    Loads file using numpy.load.

    Parameters
    ----------
    file_name : str
        Name of file to load.

    Returns
    -------
    data : array-like
        Array of data with an unknown distribution.

    '''

    data = np.load(file_name)

    return data

def main():

    ''' Your goal is to write a bootstrap function for determining errors in a
    distribution.

    The general way to bootstrap is to randomly resample a distribution many
    times, allowing the same point to be drawn more than once. The means of
    each of these resamples are calculated and stored. A cumulative
    distribution function (CDF) of the means are calculated, from which
    confidence intervals can be calculated. Remember an error at 95% confidence
    means gives the value of the mean where the CDF is below 2.5% for the lower
    error and above 97.5% for the higher error.

    Load the example distribution './data/boostrap_distribution.npy' and
    calculate the error on the distribution at a given confidence level. Make a
    plot of the CDF of the bootstrap means. Include vertical lines marking
    the errors at a given confidence level.

    '''

    file_name = 'data/bootstrap_distribution.npy'

    data = load_data(file_name)

    samples = bootstrap(data, 100)

    conf_int = calc_bootstrap_error(samples, 0.05)

    print conf_int

    x, cdf = calc_cdf(samples)

    plot_cdf(x, cdf, conf_int=conf_int)

if __name__ == '__main__':
    main()



