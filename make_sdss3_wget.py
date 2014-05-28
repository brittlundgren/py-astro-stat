# Britt Lundgren
# May 14, 2014
#
# Script to fetch reduced SDSS/BOSS optical spectra, using the CSV output from the SAS
#
# To fetch other data, see: http://dr10.sdss3.org/documentation

import os, sys

if __name__ == '__main__':



    # Name the directory where you'd like to put the catalog files
    # ---OPTIONAL TO MODIFY---
    specpath = 'SDSS_spectra'

    # Name the file containing a CSV list of DR10 objects you want to download,
    # output from the SAS bulk search (http://dr10.sdss3.org/bulkSpectra)
    # ---MODIFY THIS---
    repeatcatname = 'RM_targets_sas_results.dat'


    # Create a new directory, if it wasn't made in a previous run of this script
    if not os.path.exists(specpath):
        os.system("mkdir %s" % (specpath))
        
    # Read in the CSV formatted list of objects you want to download
    for line in open(repeatcatname).readlines():
        cols = line.split(',')
        # ignore the header line
        if not line.startswith('Name'):

            # read in the survey designator, convert to lower case
            detector=str(cols[1]).lower()
            surveys = ['sdss','boss']
            if detector not in surveys:
                print "detector %s not recognized!" % (str(cols[1]))

            # read in the plate, fiber, mjd unique identifiers
            plate=(int(cols[2]))
            fiber=(int(cols[4]))
            mjd=(int(cols[3]))

            # change integer values to strings
            mjdstr = str(mjd)
            # add leading zeros to plate number, if less than 1000
            if int(plate)<1000:
                platestr='0'+str(plate)
            else:
                platestr = str(plate)
            # add leading zeros to fiber number, if necessary
            if fiber<10:
                fiberstr='000'+str(fiber)
            elif fiber<100:
                fiberstr='00'+str(fiber)
            elif fiber<1000:
                fiberstr='0'+str(fiber)
            else:
                fiberstr=str(fiber)
 
            specid = 'spec-'+platestr+'-'+mjdstr+'-'+fiberstr+'.fits'

            # location of the spectrum in SAS
            specloc = 'http://data.sdss3.org/sas/dr10/'+detector+'/spectro/redux/26/spectra/'+platestr+'/spec-'+platestr+'-'+mjdstr+'-'+fiberstr+'.fits'

            # fetch each spectrum
            os.system("wget %s" % (specloc))
            

            # move file to previously specified directory
            os.system("mv %s %s" % (specid,specpath))
