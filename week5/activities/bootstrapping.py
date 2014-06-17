#!/usr/bin/python

''' Activity to introduce the concept and implementation of bootstrapping.

This activity is meant to help you practice Pythonic programming. Pythonic
programming means to code for humans, not for computers. One of the clearest
and most efficient ways to write your programs is to write their purpose and
their functionalities first. The code below consists of the first steps of
efficient programming.

Modular coding is key to success! The coder in this case has recognized what
the separate tasks are in their problem and wrote them into individual
functions. You will notice that there is no code written though! The coder has
designed their code before writing it. You will notice each function has a
number of arguments and a docstring (documentation) describing the arguments of
the function.

Your job is to finish the code.

Perform the activity in the following way:
    1. Read each of the functions, their arguments, and their docstrings.

    2. Discuss with your group how to implement the design to solve the problem
    at hand.

    3. Implement the code in pairs or as a single group.

    4. Perform any additional analysis on your results to test their validity.

    5. Choose an individual presenter. Prepare a short presentation < 3 min to
    present to the class on how you solved the problem and what your results
    are. Discuss with the class what were the weaknesses of the design and what
    you would change.

The function at the bottom, main(), is where you will write your script. Python
sets the __name__ variable to be equal to '__main__' in this case, thus the
script will execute the main() function. This is a common and composed way to
write scripts in Python.

*** Read the main function docstring first! ***

'''

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

    -> numpy.random.randit can be used to draw random non-unique indices

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

    pass # delete line after code is written

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

    pass # delete after function code written

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
    conf_int : tuple, float, optional
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

    pass # delete after function code written

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

    pass # delete after function code written

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

def main():

    ''' Your goal is to write a bootstrap function for determining errors in a
    distribution.

    The general way to bootstrap is to randomly resample a distribution many
    times, allowing the same point to be drawn more than once. The means of
    each of these resamples are calculated and stored. A cumulative
    distribution function (CDF) of the means are calculated, from which
    confidence intervals can be calculated. Remember errors at 95% confidence
    gives the value of the mean where the CDF is below 2.5% for the lower
    error and above 97.5% for the higher error.

    Load the example distribution './data/bootstrap_distribution.npy' and
    calculate the error about the mean of the distribution at a given
    confidence level. Make a plot of the CDF of the bootstrap means. Include
    vertical lines marking the errors at a given confidence level.

    '''

    pass # delete after function code written

if __name__ == '__main__':
    main()



