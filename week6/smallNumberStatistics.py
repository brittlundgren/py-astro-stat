"""
 SmallNumberStatistics.py, July 21, 2012
 Copyright (c) 2012, Tim Haines
 =======================================================================
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see http://www.gnu.org/licenses/.
 =======================================================================
 
 This module is used to compute the single-sided upper and lower limits
 of the binomial and Poisson distributions.
 
 EXPORTS:
     binomialLimits
     poissonLimits
     
 DEPENDENCIES:
     numpy
     scipy.special
     sys
"""

import numpy
from scipy.special import bdtri, ndtr, pdtri
from sys import exit


def binomialLimits(nsuccess, ntotal, cl=None, sigma=False):
    """
 NAME:
       binomialLimits

 AUTHOR:
       Tim Haines, thaines@astro.wisc.edu

 PURPOSE:
       This function computes the single-sided upper and lower
       confidence limits for the binomial distribution.

 CATEGORY:
       Statistics and probability

 CALLING SEQUENCE:
       (u,l) = binomialLimits(nsuccess, ntotal, [, cl [, sigma]])

 INPUTS:
       nsuccess:   A strictly nonnegative integer that specifies the
                   number of successes in ntotal Bernoulli trials.
                   Can be a list or a numpy array.
       
       ntotal:     An integer strictly greater than nsuccess that
                   specifies the number of Bernoulli trials.
                   Can be a list or a numpy array.

 OPTIONAL INPUTS:
       cl:     The confidence level in the interval [0, 1]. The default
               is 0.8413 (i.e., 1 sigma)

 OPTIONS:
       sigma:  If this is true, then cl is assumed to be a
               multiple of sigma, and the actual confidence level
               is computed from the standard normal distribution with
               parameter cl.

 RETURNS:
        Two lists: the first containing the upper limits, and the second
        containing the lower limits. If the inputs are numpy arrays, then
        numpy arrays are returned instead of lists. If the inputs are scalars,
        then scalars are returned.

 REFERENCES:
       N. Gehrels. Confidence limits for small numbers of events in astrophysical
       data. The Astrophysical Journal, 303:336-346, April 1986.

 EXAMPLE:
       I have a mass bin with 100 galaxies (20 reds and 80 blues)
       and I am computing the fraction of reds to blues, then for this
       bin NSUCCESS = 20 and NTOTAL = 100.

       To compute the confidence limits at the 2.5 sigma level, use

           (u,l) = binomialLimits(20, 100, 2.5, sigma=True)
               u = 0.31756
               l = 0.11056

       Since these are the confidence limits, the fraction would be
       reported as

           0.2 (+0.11756, -0.08944)
"""
    if cl is None:
        cl = 1.0
        sigma = True
    
    if sigma:
        cl = ndtr(cl)

    if not type(nsuccess) == type(ntotal):
        exit('nsuccess and ntotal must have the same type')
    
    # Since there isn't any syntactical advantage to using
    # numpy, just convert them to lists and carry on.
    isNumpy = False
    if isinstance(nsuccess,numpy.ndarray):
        nsuccess = nsuccess.tolist()
        ntotal = ntotal.tolist()
        isNumpy = True
    
    # Box single values into a list
    isScalar = False
    if not isinstance(nsuccess,list):
        nsuccess = [nsuccess]
        ntotal = [ntotal]
        isScalar = True
    
    # Must have the same length
    if not len(nsuccess) == len(ntotal):
        exit('nsuccess and total must have same length')
    
    upper = []
    lower = []
    
    for (s,t) in zip(nsuccess,ntotal):
        nfail = t - s
        
        # See Gehrels (1986) for details
        if nfail == 0:
            upper.append(1.0)
        else:
            upper.append(bdtri(s,t,1-cl))
        
        # See Gehrels (1986) for details
        if s == 0:
            lower.append(0.0)
        else:
            lower.append(1 - bdtri(nfail,t,1-cl))
    
    if isNumpy:
        upper = numpy.array(upper)
        lower = numpy.array(lower)

    # Scalar-in/scalar-out
    if isScalar:
        return (upper[0],lower[0])
    
    return (upper,lower)


def poissonLimits(k, cl=None, sigma=False):
    """
 NAME:
       poissonLimits

 AUTHOR:
       Tim Haines, thaines@astro.wisc.edu

 PURPOSE:
       This function computes the single-sided upper and lower
       confidence limits for the Poisson distribution.

 CATEGORY:
       Statistics and probability

 CALLING SEQUENCE:
       (u,l) = poissonLimits(k, [cl [, sigma]])

 INPUTS:
       k:      A strictly nonnegative integer that specifies the
               number of observed events. Can be a list or numpy array.
        
 OPTIONAL INPUTS:
       cl:     The confidence level in the interval [0, 1). The default
               is 0.8413 (i.e., 1 sigma)

 OPTIONS:
       sigma:  If this is true, then cl is assumed to be a
               multiple of sigma, and the actual confidence level
               is computed from the standard normal distribution with
               parameter cl.

 RETURNS:
        Two lists: the first containing the upper limits, and the second
        containing the lower limits. If the input is a numpy array, then
        numpy arrays are returned instead of lists. If the input is a scalar,
        then scalars are returned.

 REFERENCES:
       N. Gehrels. Confidence limits for small numbers of events in astrophysical
       data. The Astrophysical Journal, 303:336-346, April 1986.

 EXAMPLE:
       Compute the confidence limits of seeing 20 events in 8
       seconds at the 2.5 sigma.

           (u,l) = poissonLimits(20, 2.5, sigma=True)
               u = 34.1875
               l = 10.5711

       However, recall that the Poisson parameter is defined as the
       average rate, so it is necessary to divide these values by
       the time (or space) interval over which they were observed.

       Since these are the confidence limits, the fraction would be
       reported as

           2.5 (+4.273, -1.321) observations per second
"""
    if cl is None:
        cl = 1.0
        sigma = True
    
    if sigma:
        cl = ndtr(cl)

    # Since there isn't any syntactical advantage to using
    # numpy, just convert it to a list and carry on.
    isNumpy = False
    if isinstance(k,numpy.ndarray):
        k = k.tolist()
        isNumpy = True
        
    # Box single values into a list
    isScalar = False
    if not isinstance(k,list):
        k = [k]
        isScalar = True
    
    upper = []
    lower = []
    
    for x in k:
        upper.append(pdtri(x,1-cl))
        
        # See Gehrels (1986) for details
        if x == 0:
            lower.append(0.0)
        else:
            lower.append(pdtri(x-1,cl))
    
    if isNumpy:
        upper = numpy.array(upper)
        lower = numpy.array(lower)
    
    # Scalar-in/scalar-out
    if isScalar:
        return (upper[0], lower[0])
    
    return (upper,lower)

