# Britt Lundgren
# July 29, 2014
#
# Script to create spec*dat files from spPlate data for SEQUELS quasars
#

import os, sys
import pyfits
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

from sklearn.qda import QDA

#from astroML.datasets import fetch_rrlyrae_combined
from astroML.utils import split_samples
from astroML.utils import completeness_contamination

if __name__ == '__main__':

    # read in the CSV data and convert to FITS
    Name = []
    Country = []
    Age = []
    Height = []
    Weight = []
    Sex = []
    #DOB = []
    #POB = []
    Gold = []
    Silver = []
    Bronze = []
    Medals_tot = []
    Sport = []
    Event = []
    X = []
    i=-1
    for line in open('London2012.dat').readlines():
        cols = line.split(',')
        if not line.startswith('#'):
            #print line.strip()
            if (len(cols[3])>0. and len(cols[4])>0. and len(cols[2])>0. and int(cols[2])>10.):
                i+=1
                # Name,Country,Age,Height_cm,Weight_kg,Sex,Date of birth,Place of birth,Gold,Silver,Bronze,Total,Sport,Event
                Name.append(str(cols[0]))
                Country.append(str(cols[1]))
                Age.append(float(cols[2]))
                Height.append(float(cols[3]))
                Weight.append(float(cols[4]))
                Sex.append(str(cols[5]))
                #DOB.append(str(cols[6]))
                #POB.append(str(cols[7]))
                Gold.append(int(cols[8]))
                Silver.append(int(cols[9]))
                Bronze.append(int(cols[10]))
                Medals_tot.append(int(cols[11]))
                Sport.append(str(cols[12]))
                Event.append(str(cols[13]))
    
    fout = 'London_2012.fits'
    c1 =  pyfits.Column(name='Name', format="30A", array=Name)
    c2 =  pyfits.Column(name='Country', format="30A", array=Country)
    c3 =  pyfits.Column(name='Age', format="D", array=Age)
    c4 =  pyfits.Column(name='Height', format="D", array=Height)
    c5 =  pyfits.Column(name='Weight', format="D", array=Weight)
    c6 =  pyfits.Column(name='Sex', format="30A", array=Sex)
    #c7 =  pyfits.Column(name='DOB', format="10A", array=DOB)
    #c8 =  pyfits.Column(name='POB', format="30A", array=POB)
    c9 =  pyfits.Column(name='Gold', format="D", array=Gold)
    c10 =  pyfits.Column(name='Silver', format="D", array=Silver)
    c11 =  pyfits.Column(name='Bronze', format="D", array=Bronze)
    c12 =  pyfits.Column(name='Medals_tot', format="D", array=Medals_tot)
    c13 =  pyfits.Column(name='Sport', format="30A", array=Sport)
    c14 =  pyfits.Column(name='Event', format="30A", array=Event)
            
    
    print len(Sport)
    print "writing out to FITS"
    cols = pyfits.ColDefs([c1,c2,c3,c4,c5,c6,c9,c10,c11,c12,c13,c14])

    tbhdu = pyfits.new_table(cols)
    n = np.arange(100)
    hdu = pyfits.PrimaryHDU(n)
    thdulist = pyfits.HDUList([hdu,tbhdu])
    thdulist.writeto(fout)


    # read in tabular FITS data
    f = pyfits.open(fout)
    tbdata = f[1].data
    women=tbdata[tbdata.field('Sex')=='F']
    women_rowers = women[women.field('Sport')=='Rowing']
    X=[women_rowers.field('Height'),women_rowers.field('Age'), women_rowers.field('Weight')]
    y=[]
    for m in range(0,len(women_rowers)):
        if women_rowers.field('Medals_tot')[m]==0:
            y.append(0.)
        else:
            y.append(1.)
    print len(women_rowers[1]), len(y)

    
    medal_winners_age = women_rowers[women_rowers.field('Medals_tot')>0].field('Age')
    medal_winners_height = women_rowers[women_rowers.field('Medals_tot')>0].field('Height')
    nonmedal_winners_age = women_rowers[women_rowers.field('Medals_tot')==0].field('Age')
    nonmedal_winners_height = women_rowers[women_rowers.field('Medals_tot')==0].field('Height')
    print nonmedal_winners_age

    plt.clf()
    plt.plot(nonmedal_winners_age, nonmedal_winners_height, 'k.', label = 'Non-Medalists', alpha=0.3)
    plt.plot(medal_winners_age, medal_winners_height, 'ro', label = 'Medalists', alpha=0.3)
    plt.xlabel('Age')
    plt.ylabel('Height')
    plt.title('London 2012 - Female Rowing Olympians')
    plt.legend(numpoints=1)
    plt.axis([0,100,0,250])
    plt.savefig('olympian_phys.png')
    
            
    plt.clf()
    from astroML.plotting import setup_text_plots
    setup_text_plots(fontsize=8, usetex=True)

    
    #----------------------------------------------------------------------
    # get data and split into training & testing sets
    #X, y = fetch_rrlyrae_combined()
    # X = X[:, [1, 0, 2, 3]]  # rearrange columns for better 1-color results
    (X_train, X_test), (y_train, y_test) = split_samples(X, y, [0.75, 0.25],random_state=0)

    N_tot = len(y)
    N_st = np.sum(y == 0)
    N_rr = N_tot - N_st
    N_train = len(y_train)
    N_test = len(y_test)
    N_plot = 5000 + N_rr

    #----------------------------------------------------------------------
    # perform QDA
    classifiers = []
    predictions = []
    Ncolors = np.arange(1, X.shape[1] + 1)

    for nc in Ncolors:
        clf = QDA()
        clf.fit(X_train[:, :nc], y_train)
        y_pred = clf.predict(X_test[:, :nc])

        classifiers.append(clf)
        predictions.append(y_pred)

    predictions = np.array(predictions)

    completeness, contamination = completeness_contamination(predictions, y_test)

    print "completeness", completeness
    print "contamination", contamination

    #------------------------------------------------------------
    # Compute the decision boundary
    clf = classifiers[1]
    xlim = (0.7, 1.35)
    ylim = (-0.15, 0.4)
    
    xx, yy = np.meshgrid(np.linspace(xlim[0], xlim[1], 71),np.linspace(ylim[0], ylim[1], 81))

    Z = clf.predict_proba(np.c_[yy.ravel(), xx.ravel()])
    Z = Z[:, 1].reshape(xx.shape)

    #----------------------------------------------------------------------
    # plot the results
    fig = plt.figure(figsize=(5, 2.5))
    fig.subplots_adjust(bottom=0.15, top=0.95, hspace=0.0,left=0.1, right=0.95, wspace=0.2)

    # left plot: data and decision boundary
    ax = fig.add_subplot(121)
    im = ax.scatter(X[-N_plot:, 1], X[-N_plot:, 0], c=y[-N_plot:],s=4, lw=0, cmap=plt.cm.binary, zorder=2)
    im.set_clim(-0.5, 1)

    im = ax.imshow(Z, origin='lower', aspect='auto',cmap=plt.cm.binary, zorder=1,extent=xlim + ylim)
    im.set_clim(0, 1.5)

    ax.contour(xx, yy, Z, [0.5], colors='k')

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    ax.set_xlabel('$u-g$')
    ax.set_ylabel('$g-r$')

    # plot completeness vs Ncolors
    ax = fig.add_subplot(222)
    ax.plot(Ncolors, completeness, 'o-k', c='k', ms=6, label='unweighted')

    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.2))
    ax.xaxis.set_major_formatter(plt.NullFormatter())

    ax.set_ylabel('completeness')
    ax.set_xlim(0.5, 4.5)
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True)

    # plot contamination vs Ncolors
    ax = fig.add_subplot(224)
    ax.plot(Ncolors, contamination, 'o-k', c='k', ms=6, label='unweighted')

    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.2))
    ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%i'))
    
    ax.set_xlabel('N colors')
    ax.set_ylabel('contamination')
    
    ax.set_xlim(0.5, 4.5)
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True)

    plt.show()
