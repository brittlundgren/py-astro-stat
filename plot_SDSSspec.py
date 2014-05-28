# Britt Lundgren
# May 26, 2014
#
# Script to make a plot of every FITS-formatted individual SDSS spectrum in a directory

import os, sys
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
mpl.interactive(True)
from matplotlib import pyplot as pl
import astropy.io.fits as fits
import glob


if __name__ == '__main__':

    # name directory to wherever the spectra are located
    # ---MODIFY THIS---
    dir = 'SDSS_spectra'

    if not os.path.exists(dir):
        print "Directory %s not found" % (dir)
    else:
        # make a directory to place the plots
        plot_dir = dir+'_plots'
        print plot_dir
        if not os.path.exists(plot_dir):
            os.system('mkdir %s' % plot_dir)

        # make a list of every file in the directory
        spectra = glob.glob(dir+'/*')
        print "%i spectra found in directory %s" % (len(spectra), dir)

        for spec in spectra:

            
            hdu = fits.open(spec)
            data, header = hdu[1].data, hdu[1].header

            flux = data.field('flux')
            wl = 10**(data.field('loglam'))
            flux_err = []
            for i in data.field('ivar'): # inverse variance array
                if i==0:
                    flux_err.append(0.)
                else:
                    flux_err.append(1./i)

            # start a new plot
            pl.clf()

            # plot data
            pl.plot(wl, flux, 'k-')
            pl.plot(wl, flux_err, 'r-')
            pl.axis([min(wl), max(wl), 0, max(flux)]) # force plot limits
            
            # add axis labels and title
            pl.ylabel(r'F$_{\lambda}$ [10$^{-17}$ erg s$^{-1}$ cm$^{-2} \AA^{-1}$]')
            pl.xlabel(r'Wavelength ($\AA$)')
            specname = spec.split('/')[-1].split('.')[0].strip('spec')
            plate, mjd, fiber = specname.split('-')[1:4]
            pl.title('Plate = %s, Fiber = %s, MJD = %s' % (plate, fiber, mjd)) 
            
            # name the output plots
            specfig = plot_dir+'/'+spec.split('/')[-1].split('.')[0]+'.pdf' # strips the directory strucutre and fits suffix, defines anew
            pl.savefig(specfig, dpi=200) # force the dpi resolution
