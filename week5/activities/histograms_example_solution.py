#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import scipy
import os
from scipy import interpolate, stats

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

    from astroML.cosmology import Cosmology

    cosmo = Cosmology()
    z_sample = np.linspace(z_lims[0], z_lims[1], n_bins)
    mu_sample = [cosmo.mu(z) for z in z_sample]
    mu_z = interpolate.interp1d(z_sample, mu_sample)
    z_mu = interpolate.interp1d(mu_sample, z_sample)

    return mu_z, z_mu

def compute_luminosity_function(z, m, M, m_max, archive_file, Nbootstraps=20,
        bin_type='freedman', z_mu=None):

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
    bin_type : str
        Type of binning method to use. Options are 'freedman' or 'scott'
    z_mu : func
        Distance modulus as a function of redshift.

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

    from astroML.density_estimation import scotts_bin_width as scott_bin
    from astroML.density_estimation import freedman_bin_width as free_bin
    from astroML.lumfunc import binned_Cminus, bootstrap_Cminus

    Mmax = m_max - (m - M)
    zmax = z_mu(m_max - M)

    if not os.path.exists(archive_file):
        print ("- computing bootstrapped luminosity function ",
               "for %i points" % len(z))

        if bin_type == 'freedman':
            zbin_width, zbins = free_bin(z, return_bins=True)
            Mbin_width, Mbins = free_bin(M, return_bins=True)
        elif bin_type == 'scott':
            zbin_width, zbins = scott_bin(z, return_bins=True)
            Mbin_width, Mbins = scott_bin(M, return_bins=True)

        dist_z, err_z, dist_M, err_M = bootstrap_Cminus(z, M, zmax, Mmax,
                                                        zbins, Mbins,
                                                        Nbootstraps=20,
                                                        normalize=True)
        np.savez(archive_file,
                 zbins=zbins, dist_z=dist_z, err_z=err_z,
                 Mbins=Mbins, dist_M=dist_M, err_M=err_M)
    else:
        print "- using precomputed bootstrapped luminosity function results"
        archive = np.load(archive_file)
        zbins = archive['zbins']
        dist_z = archive['dist_z']
        err_z = archive['err_z']
        Mbins = archive['Mbins']
        dist_M = archive['dist_M']
        err_M = archive['err_M']

    return zbins, dist_z, err_z, Mbins, dist_M, err_M

def cut_data(data, z_min, z_max, m_max):

    ''' Performs redshift/magnitude cuts on the data.

    Parameters
    ----------
    data : array-like
        Dictionary of sdss galaxies
    z_min : float
        Lower redshift limit
    z_max : float
        Higher redshift limit
    m_max : float
        Upper apparent magnitude limit

    Returns
    -------
    data_red : array-like
        Cut data including red galaxies
    data_blue : array-like
        Cut data including blue galaxies

    '''


    # redshift and magnitude cuts
    data = data[data['z'] > z_min]
    data = data[data['z'] < z_max]
    data = data[data['petroMag_r'] < m_max]

    # divide red sample and blue sample based on u-r color
    ur = data['modelMag_u'] - data['modelMag_r']
    flag_red = (ur > 2.22)
    flag_blue = ~flag_red # tilde means inverse

    data_red = data[flag_red]
    data_blue = data[flag_blue]

    return data_red, data_blue

def plot_luminosity_function(Mbins_list, dist_M_list, err_M_list, titles=None,
        markers=None):

    ''' Plots the normalized luminosity functions Phi(M) vs (M) for multiple
    samples. Reproduces the bottom right plot of Figure 4.10.

    Parameters
    ----------
    Mbins_list : array-like
        Tuple of absolute magnitude bin centers.
    dist_M_list : tuple, list
        Tuple of absolute magnitude count distributions.
    err_M_list : tuple, list
        Tuple of absolute magnitude count errors.
    titles : tuple, list
        Tuple of titles for the different distributions.
    markers : tuple, list
        Tuple of markers for the different distributions.

    Returns
    -------
    None

    '''

    from astroML.plotting import setup_text_plots
    setup_text_plots(fontsize=8, usetex=False)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, yscale='log')

    # truncate the bins so the plot looks better
    for i in xrange(len(dist_M_list)):
        Mbins = Mbins_list[i][3:-1]
        dist_M = dist_M_list[i][3:-1]
        err_M = err_M_list[i][3:-1]

        ax.errorbar(0.5 * (Mbins[1:] + Mbins[:-1]), dist_M, err_M,
                    fmt='-k' + markers[i], ecolor='gray', lw=1, ms=4,
                    label=titles[i])

    ax.legend(loc=3)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
    ax.set_xlabel(r'$M$')
    ax.set_ylabel(r'$\Phi(M)$')
    ax.set_xlim(-20, -23.5)
    ax.set_ylim(1E-5, 2)

    plt.show()

def plot_num_density(zbins_list, dist_z_list, err_z_list, titles=None,
        markers=None):

    ''' Plots the number density of galaxies for multiple samples.
    Specifically, rho(z) / [z/0.08]^2 vs z where rho(z) is the number density
    of galaxies at a given redshift. Reproduces the top right plot of Figure
    4.10.

    Parameters
    ----------
    zbins_list : array-like
        Tuple of absolute redshift bin centers.
    dist_z_list : tuple, list
        Tuple of redshift count distributions.
    err_z_list : tuple, list
        Tuple of redshift count errors.
    titles : tuple, list
        Tuple of titles for the different distributions.
    markers : tuple, list
        Tuple of markers for the different distributions.

    Returns
    -------
    None

    '''

    from astroML.plotting import setup_text_plots
    setup_text_plots(fontsize=8, usetex=False)

    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(1, 1, 1)
    for i in xrange(len(dist_z_list)):
        factor = 0.08 ** 2 / (0.5 * (zbins_list[i][1:] + \
                zbins_list[i][:-1])) ** 2

        ax.errorbar(0.5 * (zbins_list[i][1:] + zbins_list[i][:-1]),
                    factor * dist_z_list[i], factor * err_z_list[i],
                    fmt='-k' + markers[i], ecolor='gray', lw=1, ms=4,
                    label=titles[i])

    ax.legend(loc=1)
    ax.xaxis.set_major_locator(plt.MultipleLocator(0.01))
    ax.set_xlabel(r'$z$')
    ax.set_ylabel(r'$\rho(z) / [z / 0.08]^2$')
    ax.set_xlim(0.075, 0.125)
    ax.set_ylim(10, 25)

    plt.show()

def main():

    ''' Your goal is to recalculate the luminosity function for the red and
    blue galaxies presented in the lower right of Figure 4.10 using
    reproducible methods for histogram binning. This activity divides the
    script for making these plots into more modular format. The above functions
    are only suggestions for how to divide the script, feel free to modularize
    the script in a different fashion.

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
    there are fewer bright blue galaxies, u-r < 2.22, than bright red galaxies,
    u-r > 2.22.

    Read through the script
    http://www.astroml.org/book_figures/chapter4/fig_lyndenbell_gals.html
    to understand the steps the authors take to calculate the luminosity and
    volume number density functions for red and blue galaxies from the SDSS
    archive.

    *** Truncate the sample to 1/10 the size as commented in line 48 and 49 ***
    *** Else computation time exorbitant ***

    The author create redshift and absolute magnitude bins to compute the
    luminosity function. Find where these bins are initialized, and change the
    binning method to either Freedman-Diaconis or Scott. Use the most
    appropriate binning strategy for the data.

    Plot the results on the same scale and with the same limits as the code in
    the example script.

    Does the histogram change how you interpret the results of this data? Are
    these binning methods sensitive to outliers?

    Notes
    -----
    -> The Freedman-Diaconis and Scott binning methods can imported as
    functions in the following way:
        from astroML.density_estimation import scotts_bin_width as scott_bin
        from astroML.density_estimation import freedman_bin_width as free_bin

    '''

    from astroML.datasets import fetch_sdss_specgals

    data = fetch_sdss_specgals()

    z_min = 0.08
    z_max = 0.12
    m_max = 17.7

    data_red, data_blue = cut_data(data, z_min, z_max, m_max)
    data_red = data_red[::10]
    data_blue = data_blue[::10]
    data_samples = (data_red, data_blue)

    mu_z, z_mu = derive_dist_mod_tables((0.01, 1.5), 100)

    # Initialize data lists to contain blue and red data
    Mbins_list = []
    zbins_list = []
    dist_M_list = []
    err_M_list = []
    dist_z_list = []
    err_z_list = []

    archive_files = ['lumfunc_red.npz', 'lumfunc_blue.npz']

    # calculate luminosity function for blue and red galaxies
    for i in xrange(2):
        m = data_samples[i]['petroMag_r']
        z = data_samples[i]['z']
        M = m - mu_z(z)

        zbins, dist_z, err_z, Mbins, dist_M, err_M = \
                compute_luminosity_function(z, m, M, m_max, archive_files[i],
                    Nbootstraps=20, bin_type='freedman', z_mu=z_mu)

        Mbins_list.append(Mbins)
        zbins_list.append(zbins)
        dist_M_list.append(dist_M)
        err_M_list.append(err_M)
        dist_z_list.append(dist_z)
        err_z_list.append(err_z)

    # Plot the volume number density and the luminosity function
    titles = (r'u-r > 2.22', r'u-r < 2.22')
    markers = ['o', '^']

    plot_num_density(zbins_list, dist_z_list, err_z_list, titles=titles,
            markers=markers)

    plot_luminosity_function(Mbins_list, dist_M_list, err_M_list,
            titles=titles, markers=markers)

if __name__ == '__main__':
    main()


