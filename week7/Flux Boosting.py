# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Chapter 5

# <codecell>

import matplotlib.pyplot as plt
import numpy as np

# <codecell>

# The Likelihood function 
# ------------------------
# P(Data|Model) = P(obs flux| true flux)
# We assume Gaussian-distributed homoscedastic uncertainties
# of magnitude "rms"

def likelihood(obs, true, rms):
    return np.exp(-(obs-true)**2 / 2. / rms**2)

# <codecell>

# The a priori distribution (The prior)
# -------------------------------------
# P(Model) = P(true flux)
# Given a randomly-selected source from the sky,
# the (relative) probability of obtaining a source with 
# true flux of S is given simply by the observed
# differential number counts.
#
# For the number counts function, we assume a power-law 
# distribution with power-law index alpha, 
# so that dN/dS = (S/S_0)^(-alpha).
#                  ~propto~ S^(-alpha)

def prior(S, alpha):
    return S**(-alpha)



# <codecell>

# The posterior probability distribution
# P(Model|Data) = P(True flux | obs flux)
#
# Bayes Theorem tells us that:
#        P(M|D) = P(D|M) * P(M) / P(D)
#                ~ Likelihood * Prior
#
# Therefore, let's construct the posterior distribution
# function.
#
# inputs:
#          S_obs = Observed flux density
#          S_true = True flux density
#          alpha = Number counts power-law index
#          rms = observational Gaussian noise intensity
# Returns:
#          Relative probability of true flux density
#          (For input array, returns PDF of true flux density)

def posterior(S_obs, S_true, alpha, rms):
    return likelihood(S_obs, S_true, rms) * prior(S_true, alpha)


# <codecell>

# Let's try it out!
# Here are some examples.

# Initialize an x-grid of "true" flux densities
x = np.arange(0.01,10,1E-3)

# Choose Observed flux, RMS noise, and number counts index
S_obs = 5.5
rms = 0.9
alpha = 2.1

# Create PDFs
L = likelihood(S_obs, x, rms)
PR = prior(x, alpha)
PO = posterior(S_obs, x, alpha, rms)

# Rescale data for easy viewing
L = L / np.max(L)
PO = PO / PO[np.argmax(L)]
PR = PR / PR[np.argmax(L)] / 2.

plt.plot(x, L, label='Likelihood')
plt.plot(x, PR,label='Prior')
plt.plot(x, PO,label='Posterior')
#plt.yscale('log')
#plt.xscale('log')
plt.ylim(1E-2,2)
plt.legend(loc=0)
plt.xlabel('True Flux density [Jy]')
plt.ylabel('Relative probability')
plt.show()


# <headingcell level=1>

# Chapter 6

# <codecell>

import matplotlib.pyplot as plt
import numpy as np

# Example data
data = [1.1,2.3,3.1,2.8,3,4.4,3,
        4.5,3.6,4.2,3.9,2.4,3.3,
        6.9,5.1,7.5,8.9,7.3,8.3,
        9.3,6.6,5.2,4.1,5.7,0.3]

# Density function range
x = np.arange(0,10,0.05)

# Define distance
def dist(x1, x2):
    return np.abs(x1 - x2)

# Plotting convenience function
def show_data(data):
    for dat in data:
        plt.plot([dat,dat],[0,0.01],'-k')


        ###########
        # Kernels #
        ###########
        
def gauss_kernel(sigma):
    return lambda x: np.exp(-x**2/2./sigma**2) / sigma / np.sqrt(2 * 3.141592)

def tophat_kernel(width):
    return lambda x: 1./width if x < width / 2. else 0.

def your_kernel():
    return lambda x: 1E-2



# Kernel Density Estimator
def estimator(location, data, kernel, distance):
    pdf = np.zeros(location.shape) # output                                             
    for i, loc in enumerate(location):
        for j, dat in enumerate(data):
            pdf[i] = pdf[i] + kernel(dist(loc, dat))
    return pdf / len(data)



# Example usage:
pdf_gaussian = estimator(x, data, gauss_kernel(0.2),dist)
pdf_tophat = estimator(x, data, tophat_kernel(0.5), dist)
pdf_yourkernel = estimator(x, data, your_kernel(), dist)


plt.plot(x,pdf_gaussian, label='Gaussian kernel')
plt.plot(x,pdf_tophat, label='Tophat kernel')
plt.plot(x,pdf_yourkernel, label='Your kernel')

plt.xlabel('Data value')
plt.ylabel('Probability Density')
plt.legend(loc=0)
show_data(data)
plt.show()

# <codecell>


