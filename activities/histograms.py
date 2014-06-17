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

*** Read the main function docstring first! ***

'''

def derive_dist_mod_tables(z_lims, n_bins):

    ''' Creates functions approximating mu(z) and z(mu) where z is redshift and
    mu is the distance modulus. Uses the cosmology class and scipy's cubic
    spline interpolation. These functions will serve as reference tables to
    speed up computation of the luminosity function.

    Parameters
    ----------
    z_lims : tuple, float
        Pair of lower and upper limits in redshift sample.
    n_bins : int
        Number of bins in the table.

    Returns
    -------
    mu_z : function
        Distance modulus as a function of redshift.
    z_mu : function
        Redshift as a function of distance modulus.

    '''

def compute_luminosity_function(z, m, M, m_max, archive_file, Nbootstraps=20):

    ''' Compute the luminosity function and archive in the given file. If the
    file exists, then the saved results are returned.

    Parameters
    ----------
    z : array-like
        Redshifts of galaxies.
    m : array-like
        Apparent magnitudes of galaxies.
    M : array-like
        Absolute magnitudes of galaxies.
    m_max : float
        Maximum sensitivity in apparent magnitudes.
    archive_file : str
        Name of file saved for bootstrapping.
    Nbootstraps : int
        Number of bootstraps to perform.

    Returns
    -------
    zbins : array-like
        Redshift bin centers.
    dist_z : array-like
        Redshift count distribution.
    err_z : array-like
        Redshift count errors.
    Mbins : array-like
        Absolute magnitude bin centers.
    dist_M : array-like
        Absolute magnitude count distribution.
    err_M : array-like
        Absolute magnitude count errors.

    '''

    pass # delete line after code is written

def plot_luminosity_function(Mbins, dist_M_list, err_M_list):

    ''' Plots the normalized luminosity functions Phi(M) vs (M) for multiple
    samples. Reproduces the bottom right plot of Figure 4.10.

    Parameters
    ----------
    Mbins : array-like
        Absolute magnitude bin centers.
    dist_M_list : tuple, list
        Tuple of absolute magnitude count distributions.
    err_M_list : tuple, list
        Tuple of absolute magnitude count errors.
    titles : tuple, list
        Tuple of titles for the different distributions.

    Returns
    -------
    None

    '''

    pass # delete line after code is written

def plot_num_density(zbins, dist_z_list, err_z_list):

    ''' Plots the number density of galaxies for multiple samples.
    Specifically, rho(z) / [z/0.08]^2 vs z where rho(z) is the number density
    of galaxies at a given redshift. Reproduces the top right plot of Figure
    4.10.

    Parameters
    ----------
    zbins : array-like
        Absolute redshift bin centers.
    dist_z_list : tuple, list
        Tuple of redshift count distributions.
    err_z_list : tuple, list
        Tuple of redshift count errors.
    titles : tuple, list
        Tuple of titles for the different distributions.

    Returns
    -------
    None

    '''

    pass # delete line after code is written

def main():

    ''' Your goal is to recalculate the luminosity function for the red and
    blue galaxies presented in the lower right of Figure 4.10 using
    reproducible methods for histogram binning. This activity divides the
    script for making these plots into more modular format.

    Figure 4.10 shows how the probability density of galaxies as function of
    redshift and absolute magnitude varies for two different galaxy populations
    selected by color. See the left panels of Figure 4.10 showing the
    probability density function p(M, z) for the two populations as a function
    of absolute magnitude M and redshift z. p(M, z) = Phi(M) * rho(z) where Phi
    is the normalized luminosity function, and rho is the sold angle averaged
    number density of galaxies. The normalization of rho in the figure is
    confusing, the top-right plot shows that the number density of redder
    galaxies, u-r > 2.22, is more dense than blue galaxies at smaller
    redshifts.  The luminosity function plotted in the bottom right show that
    there are fewer faint blue galaxies, u-r < 2.22, than faint red galaxies,
    u-r > 2.22.

    Use the most appropriate binning strategy for the data. To save on time,
    the luminosity function bootstrapping has been pre-computed for the
    Freedman-Diaconis and Scott binning algorithms as the following in the
    'data' directory:
                            Galaxy      Filename
                            Type
                          --------------------------
        Freedman-Diaconis:  blue        lumfunc_blue_freedman.npz
                            red         lumfunc_red_freedman.npz
                    Scott:  blue        lumfunc_blue_scott.npz
                            red         lumfunc_red_scott.npz

    Plot the results on the same scale and with the same limits as the code in
    the example script.

    Does the histogram change how you interpret the results of this data?

    '''

    pass # delete line after code is written

if __name__ == '__main__':
    main()











