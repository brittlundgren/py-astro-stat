#!/usr/bin/python

''' Activity to introduce the concept and implementation of the KS test.

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
    Overall instructions will be under the main() function.

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

'''

def test_ks():

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
    p-value : float
        two-tailed p-value

    '''

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

    '''

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
    header : tuple
        Tuple of column headers.
    Data : array-like
        Array of data loaded.

    '''

    with open(filename, 'r') as f:
        header = f.readline() # reads first line
        header = header.split('\t') # split header by tabs

        data = np.genfromtxt(filename, skiprows=1)

    return (header, data)

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

    Perform the KS-test between three different criterion. What can you say
    about the samples derived from these different criterion? Are they drawn
    from the same parent distribution?

    Next, take two random samples of the u-r colors using the random.sample
    function. Perform the KS-test on the two samples. Are they from the same
    distribution?

    '''

    pass

if __name__ == '__main__':
    main()




