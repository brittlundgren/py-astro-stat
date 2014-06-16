#!/usr/bin/python


import matplotlib.pyplot as plt
import astroML.plotting as pltml
import numpy as np
from astroML.density_estimation import scotts_bin_width as scott_bin
from astroML.density_estimation import freedman_bin_width as free_bin






#    https://groups.google.com/forum/#!forum/astroml-general
import os
import numpy as np
from matplotlib import pyplot as plt

from scipy import interpolate, stats

from astroML.lumfunc import binned_Cminus, bootstrap_Cminus
from astroML.cosmology import Cosmology
from astroML.datasets import fetch_sdss_specgals

#----------------------------------------------------------------------
# This function adjusts matplotlib settings for a uniform feel in the textbook.
# Note that with usetex=True, fonts are rendered with LaTeX.  This may
# result in an error if LaTeX is not installed on your system.  In that case,
# you can set usetex to False.
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=False)

#------------------------------------------------------------
# Get the data and perform redshift/magnitude cuts
data = fetch_sdss_specgals()

z_min = 0.08
z_max = 0.12
m_max = 17.7

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

# truncate sample (optional: speeds up computation)
#data_red = data_red[::10]
#data_blue = data_blue[::10]
print data_red.size, "red galaxies"
print data_blue.size, "blue galaxies"

#------------------------------------------------------------
# Distance Modulus calculation:
#  We need functions approximating mu(z) and z(mu)
#  where z is redshift and mu is distance modulus.
#  We'll accomplish this using the cosmology class and
#  scipy's cubic spline interpolation.
cosmo = Cosmology()
z_sample = np.linspace(0.01, 1.5, 100)
mu_sample = [cosmo.mu(z) for z in z_sample]
mu_z = interpolate.interp1d(z_sample, mu_sample)
z_mu = interpolate.interp1d(mu_sample, z_sample)

data = [data_red, data_blue]
titles = ['$u-r > 2.22$', '$u-r < 2.22$']
markers = ['o', '^']
archive_files = ['lumfunc_red_freedman.npz', 'lumfunc_blue_freedman.npz']
archive_files = ['lumfunc_red_scott.npz', 'lumfunc_blue_scott.npz']

def compute_luminosity_function(z, m, M, m_max, archive_file, Nbootstraps=20,
        bin_type='freedman'):
    """Compute the luminosity function and archive in the given file.

    If the file exists, then the saved results are returned.
    """
    Mmax = m_max - (m - M)
    zmax = z_mu(m_max - M)

    if not os.path.exists(archive_file):
        print("- computing bootstrapped luminosity function " + \
               "for %i points" % len(z))

        if bin_type == 'freedman':
            zbin_width, zbins = free_bin(z, return_bins=True)
            Mbin_width, Mbins = free_bin(M, return_bins=True)
        elif bin_type == 'scott':
            zbin_width, zbins = scott_bin(z, return_bins=True)
            Mbin_width, Mbins = scott_bin(M, return_bins=True)

        dist_z, err_z, dist_M, err_M = bootstrap_Cminus(z, M, zmax, Mmax,
                                                        zbins, Mbins,
                                                        Nbootstraps=Nbootstraps,
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

#------------------------------------------------------------
# Perform the computation and plot the results
fig = plt.figure(figsize=(8, 8))

for i in range(2):
    m = data[i]['petroMag_r']
    z = data[i]['z']
    M = m - mu_z(z)

    # compute the luminosity function for the given subsample
    zbins, dist_z, err_z, Mbins, dist_M, err_M = \
        compute_luminosity_function(z, m, M, m_max, archive_files[i],
                bin_type='scott')

    ax1 = fig.add_subplot(1, 2, 1)
    factor = 0.08 ** 2 / (0.5 * (zbins[1:] + zbins[:-1])) ** 2
    ax1.errorbar(0.5 * (zbins[1:] + zbins[:-1]),
                 factor * dist_z, factor * err_z,
                 fmt='-k' + markers[i], ecolor='gray', lw=1, ms=4,
                 label=titles[i])

    #------------------------------------------------------------
    # Third axes: plot the inferred 1D distribution in M
    ax2 = fig.add_subplot(122, yscale='log')

    # truncate the bins so the plot looks better
    Mbins = Mbins[3:-1]
    dist_M = dist_M[3:-1]
    err_M = err_M[3:-1]

    ax2.errorbar(0.5 * (Mbins[1:] + Mbins[:-1]), dist_M, err_M,
                 fmt='-k' + markers[i], ecolor='gray', lw=1, ms=4,
                 label=titles[i])

#------------------------------------------------------------
# set labels and limits
ax1.legend(loc=1)
ax1.xaxis.set_major_locator(plt.MultipleLocator(0.01))
ax1.set_xlabel(r'$z$')
ax1.set_ylabel(r'$\rho(z) / [z / 0.08]^2$')
ax1.set_xlim(0.075, 0.125)
ax1.set_ylim(10, 25)

ax2.legend(loc=3)
ax2.xaxis.set_major_locator(plt.MultipleLocator(1.0))
ax2.set_xlabel(r'$M$')
ax2.set_ylabel(r'$\Phi(M)$')
ax2.set_xlim(-20, -23.5)
ax2.set_ylim(1E-5, 2)

plt.show()




