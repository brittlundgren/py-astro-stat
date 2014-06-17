#!/usr/bin/python

import numpy as np
import random

def test_ks(sample1, sample2):

    ''' Performs the Kolmogorov - Smirnov test on two distributions. This
    test determines whether or not two samples are drawn from the same
    distribution. See the scipy.stats.ks_2samp.

    Paramters
    ---------
    sample1 : array-like
        First sample to compare.
    sample2 : array-like
        Second sample to compare,

    Returns
    -------
    D : float
        KS statistic
    p : float
        two-tailed p-value

    '''

    from scipy.stats import ks_2samp

    D, p = ks_2samp(sample1, sample2)

    return D, p

def write_data_dict(data, header):

    ''' Writes numpy data array into a dictionary where each of the keys
    is a column name, and each key value consists of a column of data values.

    Parameters
    ----------
    data : array-like
        Array of values

    Returns
    -------
    data_dict : dict
        Dictionary of data.

    Notes
    -----
    -> To initialize a dictionary:
        >>> data_dict = {}

    -> To write a new key in a dictionary:
        >>> data_dict['new key'] = (0,1)

    -> To access this key later:
        >>> print(data_dict['new key'])
        (0, 1)

    '''

    data_dict = {}

    for i, key in enumerate(header):
        data_dict[key] = data[:, i]

    return data_dict

def read_sdss_data(filename):

    ''' Reads in SDSS data as a numpy array. First, load the headers into a
    list or a tuple. Second, load the columns as a numpy.array using
    numpy.loadtxt skipping the header row.

    Parameters
    ----------
    filename : str
        Location of file to load.

    Returns
    -------
    data : array-like
        Array of data loaded.
    header : tuple
        Tuple of column headers.

    '''

    with open(filename, 'r') as f:
        header = f.readline() # reads first line
        header = header.split('\t') # split header by tabs

        data = np.genfromtxt(filename, skiprows=1)

    return (data, header)

def main():

    ''' Load in the SDSS spectroscopic data from data/sdss_quasars.txt as a
    dictionary where each column of the data is represented by a different key
    in the dictionary. Calculate the u-r band colors of each source in this
    catalog.  Compare the colors of sources selected by different criterion.
    Many sources are flagged [0/1] by the following criterion:

    Flag    Description
    Lz      Low-z Quasar, color selection only, target flag
    Hz      High-z Quasar, color selection only, target flag
    fR      FIRST target flag
    fX      ROSAT target flag
    fS      Serendipity target flag
    f*      Star target flag
    fG      Galaxy target flag

    Perform the KS-test between three different flagged samples.  What can you
    say about the samples derived from these different samples?  Are they drawn
    from the same parent distribution?

    Next, take two random samples of the u-r colors using the random.sample
    function. Perform the KS-test on the two samples. Are they from the same
    distribution? What do these results say about selective over blind surveys?

    Notes
    -----
    -> To get the indices of which elements are equal to a value use booleans:
        >>> import numpy as np
        >>> a = np.array([4, 5, 6])
        >>> print(a == 5)
        array([False,  True, False], dtype=bool)
        >>> b = np.array([7, 8, 9])
        >>> print(b[a == 5])
        [8]

    -> To randomly sample an array uniquely use random.sample


    '''

    # Load the data
    data, header = read_sdss_data('data/sdss_quasars.txt')

    data_dict = write_data_dict(data, header)

    # Write a new key to the dictionary
    data_dict['u-r'] = data_dict['umag'] - data_dict['rmag']

    # Grab the colors of different flagged samples
    sample_fstar = data_dict['u-r'][data_dict['f*'] == 1]
    sample_fX = data_dict['u-r'][data_dict['fX'] == 1]
    sample_fR = data_dict['u-r'][data_dict['fR'] == 1]

    # Grab two random samples from the data
    sample_rand1 = random.sample(data_dict['u-r'], 10000)
    sample_rand2 = random.sample(data_dict['u-r'], 10000)

    print('Sample1, Sample2, KS statistic, p-value')
    print('fstar, fX: ' + str(test_ks(sample_fstar, sample_fX)))
    print('fX, fR: ' + str(test_ks(sample_fX, sample_fR)))
    print('2 random samples:' + str(test_ks(sample_rand1, sample_rand2)))

if __name__ == '__main__':
    main()


