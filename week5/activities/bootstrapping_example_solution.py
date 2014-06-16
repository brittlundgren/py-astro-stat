#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

def bootstrap(data, num_samples, alpha, return_samples=False):

    ''' Bootstraps data to determine errors. Resamples the data num_samples
    times. Returns errors of a bootstrap simulation at the 100.*(1 - alpha)
    confidence interval.

    Parameters
    ----------
    data : array-like
        Array of data in the form of an numpy.ndarray
    num_samples : int
        Number of times to resample the data.
    alpha : float
        Confidence level = 100.*(1 - alpha)
    return_samples : bool
        Optional. Return the bootstrapped samples? Useful for calculating
        multiple confidence intervals without rerunning bootstraps.

    Returns
    -------
    conf_int : tuple, float
        Lower error and upper error at 100*(1-alpha) confidence of the data.
    samples : array-like
        Array of each resampled data. Will have one extra dimension than the
        data of length num_samples, representing each simulation.

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
        idx = np.random.randint(0, data.size, data.size)
        samples[i,:] = data[idx]

    errors = calc_bootstrap_error(samples, alpha)

    if return_samples:
        return errors, samples
    else:
    	return errors

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
        Lower error and upper error at 100*(1-alpha) confidence of the data.

    Examples
    --------
    >>> import scipy
    >>> import numpy as np
    >>> data = scipy.random.f(1, 2, 100)
    >>> samples = bootstrap(data, 50)
    >>> errors = calc_bootstrap_error(samples, 0.05)

    '''

    means,cdf = calc_cdf(samples)
    cdf_vals = [0.5-(alpha/2.0), 0.5, 0.5+(alpha/2.)]
    mean_ret = np.interp(cdf_vals,cdf,means)
    mean_vals=[mean_ret[1],mean_ret[2]-mean_ret[1],mean_ret[1]-mean_ret[0]]

    return np.array(mean_vals)

def calc_cdf(samples):

    ''' Calculates a cumulative distribution function of the means of each
    instance of resampled data.

    Parameters
    ----------
    samples : array-like
        Array of each resampled data.

    Returns
    -------
    cdf : array-like
        Array containing fraction of data below value x.
    x : array-like
        Array containing mean values for the cdf.

    '''

    means = np.sort(np.mean(samples,axis=1))
    cdf = np.cumsum(means)/np.sum(means)

    return means,cdf

def plot_cdf(x, cdf, errors=None):

    ''' Plots the cumulative distribution function of the means of each
    instance of the resampled data. If errors are supplied, then vertical lines
    will be plotted at each error.

    Parameters
    ----------
    x : array-like
        Array containing mean values for the cdf.
    cdf : array-like
        Array containing fraction of data below value x.
    errors : tuple, float
        Pair of errors on the mean to be plotted as vertical lines.

    Returns
    -------
    None

    Notes
    -----


    '''

    ax = plt.figure().add_subplot(111)
    ax.plot(x, cdf)

    # check for vertical error lines
    if errors is not None:
        ax.axvline(x=errors[0], ls=':', alpha=0.7, color='b')
        ax.axvline(x=errors[1], ls='-', alpha=0.7, color='b')
    ax.set_xlabel('Mean')
    ax.set_ylabel('CDF')
    ax.figure.show()

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

    errors = bootstrap(data, 10, 0.05)

    print errors

if __name__ == '__main__':
    main()



